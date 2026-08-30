import logging
from typing import List, Dict, Any, Optional
from uuid import UUID
from sqlalchemy.orm import Session
from fastapi import HTTPException

from app.models.mastery import MasteryAttempt, MasteryAnswer
from app.models.learning_path import LearningPath
from app.repositories.learner_repository import learner_repo
from app.services.learning_path_service import learning_path_service
from app.services.mastery_question_service import mastery_question_service
from app.agents.mastery_agent import mastery_agent
from app.schemas.mastery import (
    MasteryStartResponse,
    MasterySubmitRequest,
    MasteryResult,
    MasteryReviewResponse,
    MasteryReviewItem,
    MasteryQuestionOption,
    MasteryAttemptHistoryItem,
)

logger = logging.getLogger(__name__)

class MasteryService:
    def start_assessment(self, db: Session, user_id: str, phase_id: str) -> MasteryStartResponse:
        logger.info(f"Initiating mastery assessment for user {user_id} and phase {phase_id}")

        # 1. Validate learner exists
        learner = learner_repo.get_by_id(db, user_id=user_id)
        if not learner:
            raise HTTPException(status_code=404, detail="Learner profile not found")

        # 2. Validate learning path exists
        latest_path = (
            db.query(LearningPath)
            .filter(LearningPath.user_id == user_id)
            .order_by(LearningPath.created_at.desc())
            .first()
        )
        if not latest_path:
            raise HTTPException(status_code=404, detail="Learning path not found for learner")

        # 3. Validate phase belongs to learner
        path_data = latest_path.path_json
        phase_info = learning_path_service.get_phase_info(path_data, phase_id)
        if not phase_info:
            raise HTTPException(status_code=404, detail=f"Phase '{phase_id}' not found in learning path")

        # 4. Validate phase is available / in_progress (reject locked phases)
        phase_status = phase_info.get("status", "locked")
        if phase_status == "locked":
            raise HTTPException(
                status_code=400,
                detail=f"Phase '{phase_id}' is currently locked. Complete prior prerequisite phases first."
            )

        # 5. Check if an active in-progress attempt already exists
        active_attempt = (
            db.query(MasteryAttempt)
            .filter(
                MasteryAttempt.user_id == user_id,
                MasteryAttempt.phase_id == phase_id,
                MasteryAttempt.status == "in_progress"
            )
            .first()
        )

        if active_attempt:
            logger.info(f"Found active in-progress attempt {active_attempt.id} for user {user_id} phase {phase_id}")
            # Load raw questions from question bank for the selected IDs
            raw_questions = []
            domain = latest_path.domain
            for qid in active_attempt.selected_question_ids:
                q = mastery_question_service.get_question_by_id(domain, qid)
                if q:
                    raw_questions.append(q)
            public_questions = mastery_question_service.format_public_questions(raw_questions)
            return MasteryStartResponse(
                mastery_attempt_id=UUID(active_attempt.id),
                user_id=UUID(user_id),
                phase_id=phase_id,
                attempt_number=active_attempt.attempt_number,
                total_questions=len(public_questions),
                questions=public_questions,
            )

        # 6. Retrieve previous attempts to compute attempt_number and weak topics
        prior_attempts = (
            db.query(MasteryAttempt)
            .filter(
                MasteryAttempt.user_id == user_id,
                MasteryAttempt.phase_id == phase_id
            )
            .order_by(MasteryAttempt.attempt_number.asc())
            .all()
        )

        attempt_number = len(prior_attempts) + 1
        previous_question_ids = []
        weak_topics = []

        if prior_attempts:
            latest_prior = prior_attempts[-1]
            if latest_prior.result_json and not latest_prior.passed:
                # Extract weak topics from previous attempt
                res_data = latest_prior.result_json
                weak_topics = [wt.get("topic") for wt in res_data.get("weak_topics", []) if wt.get("topic")]
            for a in prior_attempts:
                previous_question_ids.extend(a.selected_question_ids or [])

        # 7. Select questions for phase
        phase_skills = phase_info.get("skills") or phase_info.get("target_skills") or []
        phase_topics = phase_info.get("resource_topics") or phase_info.get("topics") or []
        if not phase_topics and phase_skills:
            phase_topics = list(phase_skills)

        selected_questions = mastery_question_service.select_questions_for_phase(
            domain=latest_path.domain,
            phase_skills=phase_skills,
            phase_topics=phase_topics,
            weak_topics=weak_topics if weak_topics else None,
            previous_question_ids=previous_question_ids,
            target_count=10
        )

        selected_question_ids = [q["id"] for q in selected_questions]

        # 8. Create new MasteryAttempt
        new_attempt = MasteryAttempt(
            user_id=user_id,
            learning_path_id=latest_path.id,
            phase_id=phase_id,
            status="in_progress",
            selected_question_ids=selected_question_ids,
            attempt_number=attempt_number,
        )

        db.add(new_attempt)
        db.commit()
        db.refresh(new_attempt)
        logger.info(f"mastery_attempt_created attempt={new_attempt.id} user={user_id} phase={phase_id} attempt_num={attempt_number}")

        # 9. Format public questions (no answers exposed)
        public_questions = mastery_question_service.format_public_questions(selected_questions)

        return MasteryStartResponse(
            mastery_attempt_id=UUID(new_attempt.id),
            user_id=UUID(user_id),
            phase_id=phase_id,
            attempt_number=attempt_number,
            total_questions=len(public_questions),
            questions=public_questions,
        )

    async def submit_assessment(
        self, db: Session, attempt_id: str, submission: MasterySubmitRequest
    ) -> MasteryResult:
        logger.info(f"Submitting mastery assessment attempt {attempt_id}")

        attempt = db.query(MasteryAttempt).filter(MasteryAttempt.id == attempt_id).first()
        if not attempt:
            raise HTTPException(status_code=404, detail="Mastery attempt not found")

        if attempt.status == "submitted":
            raise HTTPException(
                status_code=409, detail="Mastery assessment has already been submitted and scored"
            )

        assigned_ids = list(attempt.selected_question_ids or [])
        submitted_ids = [ans.question_id for ans in submission.answers]

        # Validation: Check duplicates
        if len(submitted_ids) != len(set(submitted_ids)):
            raise HTTPException(status_code=400, detail="Duplicate question IDs submitted in answers")

        # Validation: Check all assigned answered
        if set(submitted_ids) != set(assigned_ids):
            missing = set(assigned_ids) - set(submitted_ids)
            extra = set(submitted_ids) - set(assigned_ids)
            detail_msg = []
            if missing:
                detail_msg.append(f"Missing answers for questions: {list(missing)}")
            if extra:
                detail_msg.append(f"Unexpected answers for unassigned questions: {list(extra)}")
            raise HTTPException(status_code=400, detail="; ".join(detail_msg))

        # Retrieve LearningPath to get metadata
        db_path = learning_path_service.get_path_model(db, attempt.learning_path_id)
        if not db_path:
            raise HTTPException(status_code=404, detail="Associated learning path not found")

        path_data = db_path.path_json
        phase_info = learning_path_service.get_phase_info(path_data, attempt.phase_id)
        phase_title = phase_info.get("title", f"Phase {attempt.phase_id}") if phase_info else f"Phase {attempt.phase_id}"
        is_final = learning_path_service.is_final_phase(path_data, attempt.phase_id)

        # Retrieve question metadata from bank
        questions_metadata = {}
        for qid in assigned_ids:
            q = mastery_question_service.get_question_by_id(db_path.domain, qid)
            if not q:
                raise HTTPException(status_code=500, detail=f"Question definition {qid} missing from question bank")
            questions_metadata[qid] = q

        # Evaluate via Mastery Agent
        result, scored_answers = await mastery_agent.evaluate_assessment(
            mastery_attempt_id=UUID(attempt.id),
            user_id=UUID(attempt.user_id),
            learning_path_id=UUID(attempt.learning_path_id),
            phase_id=attempt.phase_id,
            phase_title=phase_title,
            attempt_number=attempt.attempt_number,
            is_final_phase=is_final,
            submitted_answers=submission.answers,
            questions_metadata=questions_metadata,
            remediation_previously_completed=attempt.remediation_completed,
        )

        # Atomic database transaction
        try:
            # 1. Save answers
            for ans in scored_answers:
                db_ans = MasteryAnswer(
                    mastery_attempt_id=attempt.id,
                    question_id=ans["question_id"],
                    selected_option_id=ans["selected_option_id"],
                    is_correct=ans["is_correct"],
                )
                db.add(db_ans)

            # 2. Update attempt status & score
            attempt.status = "submitted"
            attempt.submitted_at = result.submitted_at
            attempt.score = result.score
            attempt.passed = result.passed
            attempt.result_json = result.model_dump(mode="json")

            # 3. If passed: complete current phase and unlock next phase
            if result.passed:
                learning_path_service.complete_phase(db, attempt.learning_path_id, attempt.phase_id)
                learning_path_service.unlock_next_phase(db, attempt.learning_path_id, attempt.phase_id)

            db.commit()
            db.refresh(attempt)
            logger.info(f"mastery_assessment_persisted attempt={attempt.id} score={result.score}% passed={result.passed}")
        except Exception as e:
            db.rollback()
            logger.error(f"Failed to persist mastery submission: {e}")
            raise HTTPException(status_code=500, detail="Failed to save mastery assessment result")

        return result

    def get_result(self, db: Session, attempt_id: str) -> MasteryResult:
        attempt = db.query(MasteryAttempt).filter(MasteryAttempt.id == attempt_id).first()
        if not attempt:
            raise HTTPException(status_code=404, detail="Mastery attempt not found")

        if attempt.status != "submitted" or not attempt.result_json:
            raise HTTPException(
                status_code=409, detail="Mastery assessment is still in progress and has not been submitted"
            )

        return MasteryResult(**attempt.result_json)

    def get_history(self, db: Session, user_id: str, phase_id: str) -> List[MasteryAttemptHistoryItem]:
        attempts = (
            db.query(MasteryAttempt)
            .filter(MasteryAttempt.user_id == user_id, MasteryAttempt.phase_id == phase_id)
            .order_by(MasteryAttempt.attempt_number.asc())
            .all()
        )

        history = []
        for a in attempts:
            weak_topics_list = []
            if a.result_json and "weak_topics" in a.result_json:
                weak_topics_list = [wt.get("topic") for wt in a.result_json.get("weak_topics", []) if wt.get("topic")]
            history.append(
                MasteryAttemptHistoryItem(
                    mastery_attempt_id=UUID(a.id),
                    attempt_number=a.attempt_number,
                    score=a.score,
                    passed=a.passed,
                    weak_topics=weak_topics_list,
                    submitted_at=a.submitted_at,
                )
            )
        return history

    def complete_remediation(self, db: Session, attempt_id: str) -> Dict[str, Any]:
        attempt = db.query(MasteryAttempt).filter(MasteryAttempt.id == attempt_id).first()
        if not attempt:
            raise HTTPException(status_code=404, detail="Mastery attempt not found")

        attempt.remediation_completed = True
        db.commit()
        db.refresh(attempt)
        logger.info(f"remediation_completed attempt={attempt_id} user={attempt.user_id} phase={attempt.phase_id}")

        return {
            "message": "Remediation marked as complete. Learner is eligible to retest.",
            "attempt_id": attempt_id,
            "phase_id": attempt.phase_id,
            "next_action": "retest_required",
        }

    def get_review(self, db: Session, attempt_id: str) -> MasteryReviewResponse:
        attempt = db.query(MasteryAttempt).filter(MasteryAttempt.id == attempt_id).first()
        if not attempt:
            raise HTTPException(status_code=404, detail="Mastery attempt not found")

        if attempt.status != "submitted":
            raise HTTPException(
                status_code=409, detail="Review is only available after submitting the assessment"
            )

        db_path = learning_path_service.get_path_model(db, attempt.learning_path_id)
        domain = db_path.domain if db_path else "general"

        answers = db.query(MasteryAnswer).filter(MasteryAnswer.mastery_attempt_id == attempt_id).all()
        answers_map = {ans.question_id: ans for ans in answers}

        review_items = []
        for qid in (attempt.selected_question_ids or []):
            q_meta = mastery_question_service.get_question_by_id(domain, qid) or {}
            ans = answers_map.get(qid)

            options = [
                MasteryQuestionOption(id=opt["id"], text=opt["text"])
                for opt in q_meta.get("options", [])
            ]

            review_items.append(
                MasteryReviewItem(
                    question_id=qid,
                    topic=q_meta.get("topic", ""),
                    difficulty=q_meta.get("difficulty", "medium"),
                    question=q_meta.get("question", ""),
                    options=options,
                    selected_option_id=ans.selected_option_id if ans else "",
                    correct_option_id=q_meta.get("correct_option_id", ""),
                    is_correct=ans.is_correct if ans else False,
                    explanation=q_meta.get("explanation", ""),
                )
            )

        return MasteryReviewResponse(
            mastery_attempt_id=UUID(attempt.id),
            score=attempt.score or 0.0,
            passed=attempt.passed or False,
            questions=review_items,
        )

mastery_service = MasteryService()
