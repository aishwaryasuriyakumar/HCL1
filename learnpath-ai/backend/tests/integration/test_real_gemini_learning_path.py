import pytest
import uuid
from datetime import datetime

from app.core.config import settings
from app.schemas.learner import LearnerProfileResponse
from app.schemas.skill_gap import SkillGapResult, SkillGapItem, RecommendedFocusItem
from app.schemas.learning_path import LearningPathAgentInput
from app.agents.learning_path_agent import LearningPathAgent

pytestmark = pytest.mark.skipif(
    not settings.effective_gemini_api_key,
    reason="GEMINI_API_KEY / LLM_API_KEY is not configured"
)

from app.schemas.learner import LearnerProfileResponse, DomainInfo, YearsOfExperience, LearningFormat, DailyLearningTime, ExperienceLevel

@pytest.mark.asyncio
async def test_real_gemini_learning_path_generation():
    """Integration test invoking the live Gemini API (gemini-3.7-flash)."""
    user_id = str(uuid.uuid4())
    
    learner = LearnerProfileResponse(
        user_id=uuid.UUID(user_id),
        full_name="Integration Test User",
        email=f"integration_{user_id[:8]}@example.com",
        selected_domain=DomainInfo(id="generative_ai", name="Generative AI"),
        experience_level=ExperienceLevel.intermediate,
        years_of_experience=YearsOfExperience.one_to_two,
        learning_goal="Master RAG and AI Agents for production",
        career_goal="Senior AI Systems Engineer",
        motivation="Career transition",
        current_skills=["Python", "FastAPI"],
        interests=["LLMs", "RAG", "AI Agents"],
        projects=[],
        certifications=[],
        completed_courses=[],
        preferred_learning_formats=[LearningFormat.interactive],
        daily_learning_time=DailyLearningTime.time_1_2_hours,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    )

    skill_gap = SkillGapResult(
        analysis_id=uuid.uuid4(),
        user_id=uuid.UUID(user_id),
        assessment_attempt_id=uuid.uuid4(),
        domain="generative_ai",
        career_goal="Senior AI Systems Engineer",
        learning_goal="Master RAG and AI Agents for production",
        overall_assessment_score=60.0,
        overall_proficiency="intermediate",
        skills=[
            SkillGapItem(
                skill="RAG",
                current_score=40.0,
                current_proficiency="beginner",
                target_score=75.0,
                gap_score=35.0,
                severity="critical_gap",
                confidence="high",
                priority_score=85.0,
                priority="critical",
                prerequisites=["Embeddings", "Vector Databases"],
                reason="High priority gap for target learning goal"
            )
        ],
        strong_skills=["LLM Fundamentals", "Prompt Engineering"],
        minor_gaps=[],
        moderate_gaps=["Embeddings"],
        high_gaps=["Vector Databases"],
        critical_gaps=["RAG", "AI Agents"],
        recommended_focus=[
            RecommendedFocusItem(order=1, skill="Embeddings", reason="Required prerequisite"),
            RecommendedFocusItem(order=2, skill="Vector Databases", reason="Required prerequisite"),
            RecommendedFocusItem(order=3, skill="RAG", reason="Critical goal gap"),
            RecommendedFocusItem(order=4, skill="AI Agents", reason="Critical goal gap")
        ],
        summary="Learner needs RAG and AI Agents with Embeddings and Vector DB prerequisites.",
        generated_at=datetime.utcnow()
    )

    agent = LearningPathAgent()
    input_data = LearningPathAgentInput(
        learner_profile=learner,
        skill_gap_result=skill_gap,
        skill_knowledge={}
    )

    result = await agent.run(input_data)

    # Validate live Gemini output structure & requirements
    assert result is not None
    assert result.user_id == uuid.UUID(user_id)
    assert result.domain == "generative_ai"
    assert 3 <= result.total_phases <= 8
    assert result.phases[0].status == "available"
    assert all(p.status == "locked" for p in result.phases[1:])
    assert result.capstone_project is not None
    assert len(result.capstone_project.title) > 0
    assert result.estimated_total_hours > 0
