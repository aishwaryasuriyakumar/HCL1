from sqlalchemy.orm import Session
from fastapi import HTTPException
from datetime import datetime
import uuid
from typing import List

from app.models.assessment import AssessmentAttempt, AssessmentAnswer, SkillAssessmentResult
from app.repositories.assessment_repository import assessment_repo
from app.repositories.learner_repository import learner_repo
from app.services.question_bank_service import question_bank_service
from app.services.scoring_service import scoring_service
from app.schemas.assessment import (
    AssessmentStartResponse, QuestionPublic, OptionPublic,
    AssessmentResult, OverallResult, SkillResult,
    ReviewAnswerDetail, AssessmentHistoryResponse, AssessmentHistoryItem
)

class AssessmentService:
    def start_assessment(self, db: Session, user_id: str) -> AssessmentStartResponse:
        # 1. Validate learner existence
        learner = learner_repo.get_by_id(db, user_id=user_id)
        if not learner:
            raise HTTPException(status_code=404, detail="Learner profile not found")
            
        domain = learner.selected_domain
        
        # 2. Check for an active in-progress attempt for this domain
        active_attempt = assessment_repo.get_active_attempt(db, user_id=user_id, domain=domain)
        if active_attempt:
            return self._map_to_start_response(active_attempt)
            
        # 3. Balanced question selection
        try:
            selected_qs = question_bank_service.select_balanced_questions(domain)
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))
            
        question_ids = [q["id"] for q in selected_qs]
        
        # 4. Create attempt
        attempt = AssessmentAttempt(
            user_id=user_id,
            domain=domain,
            status="in_progress",
            selected_question_ids=question_ids,
            total_questions=15
        )
        saved_attempt = assessment_repo.create_attempt(db, attempt)
        return self._map_to_start_response(saved_attempt)

    def get_attempt(self, db: Session, attempt_id: str) -> AssessmentStartResponse:
        attempt = assessment_repo.get_attempt(db, attempt_id)
        if not attempt:
            raise HTTPException(status_code=404, detail="Assessment attempt not found")
            
        if attempt.status != "in_progress":
            raise HTTPException(status_code=400, detail="Assessment attempt has already been submitted")
            
        return self._map_to_start_response(attempt)

    def submit_assessment(self, db: Session, attempt_id: str, submission) -> AssessmentResult:
        attempt = assessment_repo.get_attempt(db, attempt_id)
        if not attempt:
            raise HTTPException(status_code=404, detail="Assessment attempt not found")
            
        if attempt.status == "submitted":
            raise HTTPException(status_code=409, detail="Assessment has already been submitted")
            
        # Validation checks
        answers_in = submission.answers
        if len(answers_in) != 15:
            raise HTTPException(status_code=422, detail=f"Expected exactly 15 answers, found {len(answers_in)}")
            
        submitted_question_ids = [ans.question_id for ans in answers_in]
        if len(set(submitted_question_ids)) != 15:
            raise HTTPException(status_code=422, detail="Duplicate question answers are not allowed")
            
        assigned_ids = set(attempt.selected_question_ids)
        for ans in answers_in:
            if ans.question_id not in assigned_ids:
                raise HTTPException(
                    status_code=422,
                    detail=f"Question '{ans.question_id}' does not belong to this assessment attempt"
                )
                
            q_detail = question_bank_service.get_question(ans.question_id)
            if not q_detail:
                raise HTTPException(status_code=422, detail=f"Question '{ans.question_id}' not found in bank")
                
            option_ids = [opt["id"] for opt in q_detail["options"]]
            if ans.selected_option_id not in option_ids:
                raise HTTPException(
                    status_code=422,
                    detail=f"Option '{ans.selected_option_id}' is invalid for question '{ans.question_id}'"
                )
                
        # Score answers and calculate results
        answers_to_save = []
        correct_count = 0
        
        # Track statistics by skill
        skill_stats = {}
        
        for ans in answers_in:
            q_detail = question_bank_service.get_question(ans.question_id)
            is_correct = (ans.selected_option_id == q_detail["correct_option_id"])
            if is_correct:
                correct_count += 1
                
            db_answer = AssessmentAnswer(
                attempt_id=attempt.id,
                question_id=ans.question_id,
                selected_option_id=ans.selected_option_id,
                is_correct=is_correct
            )
            answers_to_save.append(db_answer)
            
            # Map stats
            skill = q_detail["skill"]
            if skill not in skill_stats:
                skill_stats[skill] = {"attempted": 0, "correct": 0}
            skill_stats[skill]["attempted"] += 1
            if is_correct:
                skill_stats[skill]["correct"] += 1

        overall_score = scoring_service.calculate_percentage(correct_count, 15)
        overall_proficiency = scoring_service.classify_proficiency(overall_score)
        
        attempt.correct_answers = correct_count
        attempt.overall_score = overall_score
        attempt.overall_proficiency = overall_proficiency
        
        # Construct skill results objects
        skills_to_save = []
        for skill_name, stats in skill_stats.items():
            score = scoring_service.calculate_percentage(stats["correct"], stats["attempted"])
            prof = scoring_service.classify_proficiency(score)
            conf = scoring_service.calculate_confidence(stats["attempted"])
            
            db_skill = SkillAssessmentResult(
                attempt_id=attempt.id,
                skill=skill_name,
                questions_attempted=stats["attempted"],
                correct_answers=stats["correct"],
                score_percentage=score,
                proficiency_level=prof,
                confidence=conf
            )
            skills_to_save.append(db_skill)
            
        # Persist atomic transaction
        updated_attempt = assessment_repo.save_answers_and_results(db, attempt, answers_to_save, skills_to_save)
        return self._map_to_result_response(updated_attempt)

    def get_result(self, db: Session, attempt_id: str) -> AssessmentResult:
        attempt = assessment_repo.get_attempt(db, attempt_id)
        if not attempt:
            raise HTTPException(status_code=404, detail="Assessment attempt not found")
            
        if attempt.status != "submitted":
            raise HTTPException(status_code=409, detail="Assessment has not been submitted yet")
            
        return self._map_to_result_response(attempt)

    def get_review(self, db: Session, attempt_id: str) -> List[ReviewAnswerDetail]:
        attempt = assessment_repo.get_attempt(db, attempt_id)
        if not attempt:
            raise HTTPException(status_code=404, detail="Assessment attempt not found")
            
        if attempt.status != "submitted":
            raise HTTPException(status_code=409, detail="Assessment has not been submitted yet")
            
        answers_map = {ans.question_id: ans for ans in attempt.answers}
        
        review_details = []
        for q_id in attempt.selected_question_ids:
            q_detail = question_bank_service.get_question(q_id)
            user_ans = answers_map.get(q_id)
            
            selected_opt = None
            if user_ans:
                selected_opt_dict = next((opt for opt in q_detail["options"] if opt["id"] == user_ans.selected_option_id), None)
                if selected_opt_dict:
                    selected_opt = OptionPublic(id=selected_opt_dict["id"], text=selected_opt_dict["text"])
                    
            correct_opt_dict = next((opt for opt in q_detail["options"] if opt["id"] == q_detail["correct_option_id"]), None)
            correct_opt = OptionPublic(id=correct_opt_dict["id"], text=correct_opt_dict["text"])
            
            review_details.append(ReviewAnswerDetail(
                question_id=q_id,
                skill=q_detail["skill"],
                difficulty=q_detail["difficulty"],
                question=q_detail["question"],
                selected_answer=selected_opt,
                correct_answer=correct_opt,
                is_correct=user_ans.is_correct if user_ans else False,
                explanation=q_detail["explanation"]
            ))
            
        return review_details

    def get_user_history(self, db: Session, user_id: str) -> AssessmentHistoryResponse:
        learner = learner_repo.get_by_id(db, user_id=user_id)
        if not learner:
            raise HTTPException(status_code=404, detail="Learner profile not found")
            
        attempts = assessment_repo.get_attempts_by_user(db, user_id=user_id)
        history_items = []
        for att in attempts:
            history_items.append(AssessmentHistoryItem(
                attempt_id=att.id,
                domain=att.domain,
                status=att.status,
                score=att.overall_score,
                proficiency=att.overall_proficiency,
                started_at=att.started_at,
                submitted_at=att.submitted_at
            ))
            
        return AssessmentHistoryResponse(user_id=user_id, attempts=history_items)

    def _map_to_start_response(self, attempt: AssessmentAttempt) -> AssessmentStartResponse:
        questions = []
        for q_id in attempt.selected_question_ids:
            q_detail = question_bank_service.get_question(q_id)
            pub_q = question_bank_service.serialize_public_question(q_detail)
            questions.append(QuestionPublic(**pub_q))
            
        return AssessmentStartResponse(
            attempt_id=attempt.id,
            user_id=attempt.user_id,
            domain=attempt.domain,
            status=attempt.status,
            total_questions=attempt.total_questions,
            questions=questions,
            started_at=attempt.started_at
        )

    def _map_to_result_response(self, attempt: AssessmentAttempt) -> AssessmentResult:
        # Sort skill results by name to ensure consistent outputs
        skill_res_sorted = sorted(attempt.skill_results, key=lambda x: x.skill)
        
        skill_results = [
            SkillResult(
                skill=sr.skill,
                questions_attempted=sr.questions_attempted,
                correct_answers=sr.correct_answers,
                score=sr.score_percentage,
                proficiency=sr.proficiency_level,
                confidence=sr.confidence
            )
            for sr in skill_res_sorted
        ]
        
        overall = OverallResult(
            total_questions=attempt.total_questions,
            correct_answers=attempt.correct_answers or 0,
            incorrect_answers=attempt.total_questions - (attempt.correct_answers or 0),
            score=attempt.overall_score or 0.0,
            proficiency=attempt.overall_proficiency or "Novice"
        )
        
        return AssessmentResult(
            attempt_id=attempt.id,
            user_id=attempt.user_id,
            domain=attempt.domain,
            status=attempt.status,
            overall=overall,
            skill_results=skill_results,
            started_at=attempt.started_at,
            submitted_at=attempt.submitted_at or datetime.utcnow()
        )

assessment_service = AssessmentService()
