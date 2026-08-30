import pytest
from uuid import uuid4
from app.agents.mastery_agent import MasteryAgent
from app.services.mastery_question_service import MasteryQuestionService
from app.schemas.mastery import MasteryAnswerSubmission
from app.core.constants import (
    MASTERY_PASS_THRESHOLD,
    TOPIC_MASTERY_THRESHOLD,
    ACTION_UNLOCK_NEXT_PHASE,
    ACTION_REMEDIATION_REQUIRED,
    ACTION_LEARNING_PATH_COMPLETED,
    TOPIC_STATUS_MASTERED,
    TOPIC_STATUS_NEEDS_IMPROVEMENT,
)

@pytest.mark.asyncio
async def test_mastery_agent_passing_score():
    agent = MasteryAgent()
    attempt_id = uuid4()
    user_id = uuid4()
    path_id = uuid4()

    # 10 questions, 8 correct = 80%
    questions_meta = {
        f"q_{i}": {
            "id": f"q_{i}",
            "topic": "Chunking" if i < 5 else "Retrieval",
            "correct_option_id": "B"
        }
        for i in range(10)
    }

    # Answer 8 correctly (0..7 correct B, 8..9 wrong A)
    submitted = [
        MasteryAnswerSubmission(question_id=f"q_{i}", selected_option_id="B" if i < 8 else "A")
        for i in range(10)
    ]

    result, scored = await agent.evaluate_assessment(
        mastery_attempt_id=attempt_id,
        user_id=user_id,
        learning_path_id=path_id,
        phase_id="phase_01",
        phase_title="RAG Foundations",
        attempt_number=1,
        is_final_phase=False,
        submitted_answers=submitted,
        questions_metadata=questions_meta,
    )

    assert result.score == 80.0
    assert result.passed is True
    assert result.next_action == ACTION_UNLOCK_NEXT_PHASE
    assert len(scored) == 10
    assert sum(1 for s in scored if s["is_correct"]) == 8

@pytest.mark.asyncio
async def test_mastery_agent_failing_score_and_weak_topics():
    agent = MasteryAgent()
    attempt_id = uuid4()
    user_id = uuid4()
    path_id = uuid4()

    # Topics: Chunking (5 q), Embeddings (2 q), Retrieval (3 q)
    # Total: 10 questions
    questions_meta = {}
    for i in range(5):
        questions_meta[f"q_chunk_{i}"] = {"id": f"q_chunk_{i}", "topic": "Chunking", "correct_option_id": "B"}
    for i in range(2):
        questions_meta[f"q_emb_{i}"] = {"id": f"q_emb_{i}", "topic": "Embeddings", "correct_option_id": "B"}
    for i in range(3):
        questions_meta[f"q_ret_{i}"] = {"id": f"q_ret_{i}", "topic": "Retrieval", "correct_option_id": "B"}

    # Submissions:
    # Chunking: 2 correct out of 5 -> 40% (< 60% => Weak)
    # Embeddings: 2 correct out of 2 -> 100% (>= 60% => Mastered)
    # Retrieval: 1 correct out of 3 -> 33.33% (< 60% => Weak)
    # Total correct: 5/10 = 50% (< 75% => Failed)
    submitted = []
    for i in range(5):
        submitted.append(MasteryAnswerSubmission(question_id=f"q_chunk_{i}", selected_option_id="B" if i < 2 else "A"))
    for i in range(2):
        submitted.append(MasteryAnswerSubmission(question_id=f"q_emb_{i}", selected_option_id="B"))
    for i in range(3):
        submitted.append(MasteryAnswerSubmission(question_id=f"q_ret_{i}", selected_option_id="B" if i < 1 else "A"))

    result, scored = await agent.evaluate_assessment(
        mastery_attempt_id=attempt_id,
        user_id=user_id,
        learning_path_id=path_id,
        phase_id="phase_01",
        phase_title="RAG Foundations",
        attempt_number=1,
        is_final_phase=False,
        submitted_answers=submitted,
        questions_metadata=questions_meta,
    )

    assert result.score == 50.0
    assert result.passed is False
    assert result.next_action == ACTION_REMEDIATION_REQUIRED

    weak_topic_names = [wt.topic for wt in result.weak_topics]
    assert "Chunking" in weak_topic_names
    assert "Retrieval" in weak_topic_names
    assert "Embeddings" not in weak_topic_names

    # Check topic results
    for tr in result.topic_results:
        if tr.topic == "Embeddings":
            assert tr.status == TOPIC_STATUS_MASTERED
            assert tr.score == 100.0
        elif tr.topic == "Chunking":
            assert tr.status == TOPIC_STATUS_NEEDS_IMPROVEMENT
            assert tr.score == 40.0
        elif tr.topic == "Retrieval":
            assert tr.status == TOPIC_STATUS_NEEDS_IMPROVEMENT
            assert round(tr.score, 1) == 33.3

@pytest.mark.asyncio
async def test_mastery_agent_final_phase():
    agent = MasteryAgent()
    attempt_id = uuid4()
    user_id = uuid4()
    path_id = uuid4()

    questions_meta = {
        f"q_{i}": {"id": f"q_{i}", "topic": "Capstone", "correct_option_id": "B"}
        for i in range(10)
    }

    # 10/10 correct = 100% on final phase
    submitted = [
        MasteryAnswerSubmission(question_id=f"q_{i}", selected_option_id="B")
        for i in range(10)
    ]

    result, scored = await agent.evaluate_assessment(
        mastery_attempt_id=attempt_id,
        user_id=user_id,
        learning_path_id=path_id,
        phase_id="phase_final",
        phase_title="Advanced Capstone",
        attempt_number=1,
        is_final_phase=True,
        submitted_answers=submitted,
        questions_metadata=questions_meta,
    )

    assert result.score == 100.0
    assert result.passed is True
    assert result.next_action == ACTION_LEARNING_PATH_COMPLETED

def test_question_service_phase_selection():
    qs = MasteryQuestionService()
    questions = qs.select_questions_for_phase(
        domain="generative_ai",
        phase_skills=["RAG"],
        phase_topics=["Chunking", "Embeddings", "Retrieval", "Context Injection"],
        target_count=10
    )

    assert len(questions) == 10
    # Confirm topics in phase are represented
    selected_topics = {q.get("topic") for q in questions}
    assert "Chunking" in selected_topics
    assert "Retrieval" in selected_topics

    # Check public formatting hides answers
    public_q = qs.format_public_questions(questions)
    assert len(public_q) == 10
    for q in public_q:
        assert hasattr(q, "question")
        assert hasattr(q, "options")
        assert not hasattr(q, "correct_option_id")
        assert not hasattr(q, "explanation")
        assert not hasattr(q, "is_correct")

def test_question_service_retest_weak_topic_weighting():
    qs = MasteryQuestionService()
    questions = qs.select_questions_for_phase(
        domain="generative_ai",
        phase_skills=["RAG"],
        phase_topics=["Chunking", "Embeddings", "Retrieval", "Context Injection"],
        weak_topics=["Chunking", "Retrieval"],
        target_count=10
    )

    assert len(questions) == 10
    weak_count = sum(1 for q in questions if q.get("topic") in ["Chunking", "Retrieval"])
    # Weak topics should have significant representation (at least 4-6 questions)
    assert weak_count >= 4
