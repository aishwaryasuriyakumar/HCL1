import logging
from typing import Dict, List, Any, Optional
from datetime import datetime
from uuid import UUID

from app.agents.base_agent import BaseAgent
from app.core.constants import (
    MASTERY_PASS_THRESHOLD,
    TOPIC_MASTERY_THRESHOLD,
    ACTION_UNLOCK_NEXT_PHASE,
    ACTION_REMEDIATION_REQUIRED,
    ACTION_RETEST_REQUIRED,
    ACTION_LEARNING_PATH_COMPLETED,
    TOPIC_STATUS_MASTERED,
    TOPIC_STATUS_NEEDS_IMPROVEMENT,
)
from app.schemas.mastery import (
    MasteryResult,
    MasteryTopicResult,
    WeakTopicInfo,
    MasteryAnswerSubmission,
)

logger = logging.getLogger(__name__)

class MasteryAgent(BaseAgent):
    """
    Mastery Agent:
    Evaluates learner performance on phase mastery assessments.
    Computes deterministic scores, topic-level mastery, weak topics, and next actions.
    Communicates strictly via typed Pydantic models.
    """

    async def evaluate_assessment(
        self,
        mastery_attempt_id: UUID,
        user_id: UUID,
        learning_path_id: UUID,
        phase_id: str,
        phase_title: str,
        attempt_number: int,
        is_final_phase: bool,
        submitted_answers: List[MasteryAnswerSubmission],
        questions_metadata: Dict[str, Dict[str, Any]],
        remediation_previously_completed: bool = False,
    ) -> tuple[MasteryResult, List[Dict[str, Any]]]:
        """
        Pure backend scoring and evaluation.
        Returns: (MasteryResult, scored_answers_list)
        """
        total_questions = len(submitted_answers)
        if total_questions == 0:
            raise ValueError("Cannot evaluate assessment with zero submitted answers.")

        scored_answers = []
        topic_stats: Dict[str, Dict[str, int]] = {}

        total_correct = 0

        for ans in submitted_answers:
            q_id = ans.question_id
            q_meta = questions_metadata.get(q_id)
            if not q_meta:
                raise ValueError(f"Question metadata not found for question ID: {q_id}")

            correct_option_id = str(q_meta.get("correct_option_id", "")).strip().upper()
            selected_option_id = str(ans.selected_option_id).strip().upper()

            is_correct = (selected_option_id == correct_option_id)
            if is_correct:
                total_correct += 1

            topic = q_meta.get("topic", "General")
            if topic not in topic_stats:
                topic_stats[topic] = {"attempted": 0, "correct": 0}
            topic_stats[topic]["attempted"] += 1
            if is_correct:
                topic_stats[topic]["correct"] += 1

            scored_answers.append({
                "question_id": q_id,
                "selected_option_id": selected_option_id,
                "is_correct": is_correct,
            })

        # Calculate overall score percentage
        score = round((total_correct / total_questions) * 100.0, 2)
        passed = (score >= MASTERY_PASS_THRESHOLD)

        # Calculate topic-level results
        topic_results: List[MasteryTopicResult] = []
        weak_topics: List[WeakTopicInfo] = []

        for topic, stats in topic_stats.items():
            attempted = stats["attempted"]
            correct = stats["correct"]
            topic_score = round((correct / attempted) * 100.0, 2) if attempted > 0 else 0.0

            is_topic_mastered = (topic_score >= TOPIC_MASTERY_THRESHOLD)
            status = TOPIC_STATUS_MASTERED if is_topic_mastered else TOPIC_STATUS_NEEDS_IMPROVEMENT

            topic_results.append(
                MasteryTopicResult(
                    topic=topic,
                    questions_attempted=attempted,
                    correct_answers=correct,
                    score=topic_score,
                    status=status,
                )
            )

            if not is_topic_mastered:
                weak_topics.append(
                    WeakTopicInfo(
                        topic=topic,
                        score=topic_score,
                        reason=f"The learner answered {correct} of {attempted} {topic}-related questions correctly ({topic_score}%).",
                    )
                )

        # Determine next action
        if passed:
            if is_final_phase:
                next_action = ACTION_LEARNING_PATH_COMPLETED
            else:
                next_action = ACTION_UNLOCK_NEXT_PHASE
        else:
            next_action = ACTION_REMEDIATION_REQUIRED

        # Generate deterministic explanation
        explanation = self._generate_explanation(
            score=score,
            passed=passed,
            pass_threshold=MASTERY_PASS_THRESHOLD,
            topic_threshold=TOPIC_MASTERY_THRESHOLD,
            topic_results=topic_results,
            weak_topics=weak_topics,
        )

        result = MasteryResult(
            mastery_attempt_id=mastery_attempt_id,
            user_id=user_id,
            learning_path_id=learning_path_id,
            phase_id=phase_id,
            phase_title=phase_title,
            score=score,
            pass_threshold=MASTERY_PASS_THRESHOLD,
            passed=passed,
            topic_results=topic_results,
            weak_topics=weak_topics,
            next_action=next_action,
            attempt_number=attempt_number,
            submitted_at=datetime.utcnow(),
            explanation=explanation,
        )

        logger.info(
            f"mastery_evaluated attempt={mastery_attempt_id} user={user_id} "
            f"score={score}% passed={passed} next_action={next_action}"
        )

        return result, scored_answers

    def _generate_explanation(
        self,
        score: float,
        passed: bool,
        pass_threshold: float,
        topic_threshold: float,
        topic_results: List[MasteryTopicResult],
        weak_topics: List[WeakTopicInfo],
    ) -> str:
        if passed:
            mastered_topics = [tr.topic for tr in topic_results if tr.status == TOPIC_STATUS_MASTERED]
            if mastered_topics:
                topics_str = ", ".join(mastered_topics)
                return (
                    f"Congratulations! You scored {score:.1f}%, exceeding the required {pass_threshold}% mastery threshold. "
                    f"You demonstrated strong proficiency across {topics_str}."
                )
            return f"Congratulations! You scored {score:.1f}%, exceeding the required {pass_threshold}% mastery threshold."
        else:
            if weak_topics:
                weak_names = [wt.topic for wt in weak_topics]
                weak_str = " and ".join(weak_names) if len(weak_names) <= 2 else ", ".join(weak_names[:-1]) + f", and {weak_names[-1]}"
                return (
                    f"You scored {score:.1f}%, below the required {pass_threshold}% mastery threshold. "
                    f"{weak_str} scored below the {topic_threshold}% topic mastery threshold and require additional practice before reattempting this phase."
                )
            return (
                f"You scored {score:.1f}%, below the required {pass_threshold}% mastery threshold. "
                f"Please review the phase learning materials before reattempting the assessment."
            )

    async def run(self, input_data: Any) -> Any:
        raise NotImplementedError("Use evaluate_assessment directly with typed contracts.")

mastery_agent = MasteryAgent()
