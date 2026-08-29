import pytest
import asyncio
from datetime import datetime
from uuid import uuid4
from app.schemas.resource import (
    ResourceCandidate,
    AccessType,
    VerificationStatus,
    ResourceCardData,
    CuratedPathResources
)
from app.schemas.learning_path import LearningPathResult, PhaseSpec, CapstoneProject, ProjectSpec
from app.schemas.learner import LearnerProfileResponse, DomainInfo
from app.integrations.resource_providers.fake_provider import FakeResourceProvider
from app.integrations.resource_providers.youtube_adapter import YouTubeAdapter
from app.integrations.resource_providers.freecodecamp_adapter import FreeCodeCampAdapter
from app.integrations.resource_providers.documentation_adapter import DocumentationAdapter
from app.integrations.resource_providers.mit_ocw_adapter import MITOpenCourseWareAdapter
from app.services.resource_validator import ResourceValidator
from app.services.resource_scorer import ResourceScorer
from app.agents.resource_curator_agent import ResourceCuratorAgent

class MockLLMService:
    def generate_text(self, system_instruction: str, prompt: str, temperature: float = 0.3) -> dict:
        return {"why_recommended": "This resource directly matches your target skill gaps and learning goal."}

def create_mock_learner(full_name: str, email: str, goal: str, career: str, level: str = "intermediate") -> LearnerProfileResponse:
    now = datetime.utcnow()
    return LearnerProfileResponse(
        user_id=uuid4(),
        full_name=full_name,
        email=email,
        selected_domain=DomainInfo(id="generative_ai", name="Generative AI"),
        experience_level=level,
        learning_goal=goal,
        career_goal=career,
        current_skills=[],
        interests=[],
        projects=[],
        certifications=[],
        completed_courses=[],
        preferred_learning_formats=[],
        created_at=now,
        updated_at=now
    )

@pytest.mark.asyncio
async def test_resource_validator_access_types():
    validator = ResourceValidator()

    # Reachable public URL
    free_cand = ResourceCandidate(
        platform="TestPlatform",
        title="Free Tutorial",
        original_url="https://docs.python.org/3/",
        access_type=AccessType.PUBLIC_FREE
    )
    c_out, status = await validator.validate_candidate(free_cand)
    assert status in (VerificationStatus.VERIFIED, VerificationStatus.UNVERIFIED)
    assert c_out.is_publicly_accessible is True

    # Paid content candidate
    paid_cand = ResourceCandidate(
        platform="TestPlatform",
        title="Paid Course",
        original_url="https://docs.python.org/3/",
        access_type=AccessType.PAID
    )
    c_out, status = await validator.validate_candidate(paid_cand, allow_paid=False)
    assert status == VerificationStatus.RESTRICTED
    assert c_out.is_publicly_accessible is False

    # Restricted content candidate
    restricted_cand = ResourceCandidate(
        platform="TestPlatform",
        title="Restricted Content",
        original_url="https://docs.python.org/3/",
        access_type=AccessType.RESTRICTED
    )
    c_out, status = await validator.validate_candidate(restricted_cand)
    assert status == VerificationStatus.RESTRICTED

@pytest.mark.asyncio
async def test_resource_scorer_and_diversity():
    scorer = ResourceScorer()

    c1 = ResourceCandidate(
        platform="YouTube",
        title="RAG Tutorial Video",
        original_url="https://www.youtube.com/watch?v=123",
        resource_type="video",
        skills=["RAG", "Embeddings"],
        difficulty="intermediate",
        rating=4.8,
        access_type=AccessType.PUBLIC_FREE
    )
    c2 = ResourceCandidate(
        platform="Official Documentation",
        title="Python RAG Docs",
        original_url="https://docs.python.org/3/rag",
        resource_type="documentation",
        skills=["RAG"],
        difficulty="intermediate",
        access_type=AccessType.PUBLIC_FREE
    )
    c3 = ResourceCandidate(
        platform="freeCodeCamp",
        title="RAG Interactive Guide",
        original_url="https://www.freecodecamp.org/news/rag",
        resource_type="article",
        skills=["RAG", "Vector Databases"],
        difficulty="intermediate",
        access_type=AccessType.PUBLIC_FREE
    )

    c1.overall_score = scorer.calculate_score(c1, phase_skills=["RAG"], phase_title="RAG Systems")
    c2.overall_score = scorer.calculate_score(c2, phase_skills=["RAG"], phase_title="RAG Systems")
    c3.overall_score = scorer.calculate_score(c3, phase_skills=["RAG"], phase_title="RAG Systems")

    assert c1.overall_score > 50.0
    assert c2.overall_score > 50.0
    assert c3.overall_score > 50.0

    selected = scorer.select_diverse_top_resources([c1, c2, c3], target_count=2)
    assert len(selected) == 2
    types = {s.resource_type for s in selected}
    assert len(types) == 2  # Proves format diversity!

@pytest.mark.asyncio
async def test_provider_fault_isolation():
    # Simulate YouTube API failure (unavailable)
    youtube_failed = YouTubeAdapter(api_key="")
    fcc = FreeCodeCampAdapter()
    docs = DocumentationAdapter()
    mit = MITOpenCourseWareAdapter()

    agent = ResourceCuratorAgent(
        llm_service=MockLLMService(),
        providers=[youtube_failed, fcc, docs, mit]
    )

    statuses = agent.get_providers_status()
    yt_status = next(s for s in statuses if s.platform == "YouTube")
    assert yt_status.status == "unavailable"

    # Create dummy learning path and learner profile
    path_id = uuid4()
    phase = PhaseSpec(
        phase_id="phase_01",
        order=1,
        title="Retrieval Augmented Generation",
        description="Learn RAG fundamentals",
        skills=["RAG", "Embeddings", "Vector Databases"],
        learning_objectives=["Implement vector search"],
        resource_topics=["RAG", "Embeddings"],
        project=ProjectSpec(title="RAG Project", description="Build RAG app", deliverable="Code"),
        estimated_hours=10.0,
        difficulty="intermediate",
        recommendation_reason="Targeting RAG gap",
        status="available"
    )
    path_result = LearningPathResult(
        path_id=path_id,
        user_id=uuid4(),
        skill_gap_analysis_id=uuid4(),
        domain="generative_ai",
        title="RAG Learning Path",
        description="Path for RAG",
        learning_goal="Master RAG",
        career_goal="AI Engineer",
        overall_level="intermediate",
        total_phases=1,
        estimated_total_hours=10.0,
        phases=[phase],
        capstone_project=CapstoneProject(title="Capstone", description="Cap", deliverables=["Doc"]),
        generated_at=datetime.utcnow()
    )

    learner = create_mock_learner("Test Learner", "test@example.com", "Master RAG", "AI Engineer")

    curated = await agent.run(path_result, learner)
    assert len(curated.phases) == 1
    phase_res = curated.phases[0]
    assert len(phase_res.resources) > 0

    # Ensure all returned resources preserve original URLs and come from active providers
    for r in phase_res.resources:
        assert r.original_url.startswith("http")
        assert r.platform != "YouTube"  # Youtube was skipped due to failure
        assert r.why_recommended is not None

@pytest.mark.asyncio
async def test_original_url_preservation():
    fake_provider = FakeResourceProvider(
        platform_name="Official Documentation",
        candidates=[
            ResourceCandidate(
                platform="Official Documentation",
                title="Python Official Docs",
                original_url="https://docs.python.org/3/tutorial/index.html",
                resource_type="documentation",
                skills=["Python"],
                difficulty="beginner",
                is_free=True,
                access_type=AccessType.PUBLIC_FREE
            )
        ]
    )

    agent = ResourceCuratorAgent(
        llm_service=MockLLMService(),
        providers=[fake_provider]
    )

    phase = PhaseSpec(
        phase_id="phase_01",
        order=1,
        title="Python Fundamentals",
        description="Learn Python",
        skills=["Python"],
        learning_objectives=["Write Python code"],
        resource_topics=["Python"],
        project=ProjectSpec(title="Python Project", description="Desc", deliverable="Code"),
        estimated_hours=8.0,
        difficulty="beginner",
        recommendation_reason="Python gap",
        status="available"
    )

    path_result = LearningPathResult(
        path_id=uuid4(),
        user_id=uuid4(),
        skill_gap_analysis_id=uuid4(),
        domain="generative_ai",
        title="Python Path",
        description="Desc",
        learning_goal="Learn Python",
        career_goal="Software Developer",
        overall_level="beginner",
        total_phases=1,
        estimated_total_hours=8.0,
        phases=[phase],
        capstone_project=CapstoneProject(title="Capstone", description="Cap", deliverables=["Doc"]),
        generated_at=datetime.utcnow()
    )

    learner = create_mock_learner("Python Learner", "py@example.com", "Learn Python", "Software Developer", "beginner")

    curated = await agent.run(path_result, learner)
    card = curated.phases[0].resources[0]

    # Verify original URL is strictly preserved
    assert card.original_url == "https://docs.python.org/3/tutorial/index.html"
    assert card.platform == "Official Documentation"
