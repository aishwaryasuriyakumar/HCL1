import pytest
import uuid
from datetime import datetime
from typing import Type, TypeVar, Optional, Any
from pydantic import BaseModel

from app.schemas.learner import LearnerProfileResponse
from app.schemas.skill_gap import SkillGapResult, SkillGapItem, RecommendedFocusItem
from app.schemas.learning_path import (
    LearningPathAgentInput,
    LearningPathLLMOutput,
    LearningPathResult,
    PhaseSpec,
    ProjectSpec,
    CompletionCriteria,
    CapstoneProject,
)
from app.agents.learning_path_agent import LearningPathAgent
from app.integrations.llm.llm_service import LLMService

T = TypeVar("T", bound=BaseModel)

class FakeLLMService(LLMService):
    def __init__(self, mock_output: Optional[LearningPathLLMOutput] = None):
        # Do not call parent __init__ so it doesn't require real API key or config
        self.api_key = "fake_key_for_testing"
        self.model_name = "fake_model"
        self.mock_output = mock_output

    def generate_structured(self, prompt: str, system_instruction: str, response_model: Type[T]) -> T:
        if self.mock_output is not None:
            return self.mock_output  # type: ignore

        # Default fallback mock output for testing
        if "production RAG" in prompt or "advanced" in prompt.lower():
            return LearningPathLLMOutput(
                title="Advanced Production RAG Architecture",
                description="Tailored roadmap for building scalable production RAG systems.",
                overall_level="advanced",
                summary_recommendation="Prioritizing advanced retrieval optimization and evaluation.",
                phases=[
                    PhaseSpec(
                        phase_id="phase_01",
                        order=1,
                        title="Advanced Vector Retrieval",
                        description="Mastering dense & sparse embeddings and vector databases.",
                        skills=["Embeddings", "Vector Databases"],
                        prerequisite_phase_ids=[],
                        learning_objectives=["Implement hybrid search", "Benchmark vector index latency"],
                        learning_outcomes=["Optimized vector database configuration"],
                        resource_topics=["Dense vector retrieval", "Hybrid search strategies"],
                        project=ProjectSpec(
                            title="Hybrid Vector Search Engine",
                            description="Build high-throughput vector search benchmark",
                            deliverable="Benchmarking repository with latency graphs",
                            estimated_hours=6.0
                        ),
                        estimated_hours=8.0,
                        difficulty="advanced",
                        recommendation_reason="Vector databases are required for high-scale retrieval.",
                        completion_criteria=CompletionCriteria(assessment_required=True, mastery_threshold=80.0),
                        status="available"
                    ),
                    PhaseSpec(
                        phase_id="phase_02",
                        order=2,
                        title="Production RAG Pipelines",
                        description="Deploying end-to-end RAG with continuous evaluation.",
                        skills=["RAG", "LLM Evaluation"],
                        prerequisite_phase_ids=["phase_01"],
                        learning_objectives=["Implement RAG evaluation suite", "Build contextual re-ranking"],
                        learning_outcomes=["Production-ready RAG application"],
                        resource_topics=["RAG architecture", "RAG trilemma evaluation"],
                        project=ProjectSpec(
                            title="Evaluation-Driven RAG Service",
                            description="Implement end-to-end RAG with RAGAS evaluation",
                            deliverable="Deployed API service with evaluation metrics dashboard",
                            estimated_hours=10.0
                        ),
                        estimated_hours=12.0,
                        difficulty="advanced",
                        recommendation_reason="Directly targets your career goal of building production RAG.",
                        completion_criteria=CompletionCriteria(assessment_required=True, mastery_threshold=80.0),
                        status="locked"
                    )
                ],
                capstone_project=CapstoneProject(
                    title="Enterprise Agentic RAG Platform",
                    description="Build a production-grade multi-tenant Agentic RAG pipeline.",
                    deliverables=["Source code repository", "Architecture diagram", "Evaluation report"],
                    estimated_hours=20.0
                )
            )  # type: ignore

        # Standard beginner mock output
        return LearningPathLLMOutput(
            title="Generative AI Foundations & RAG Essentials",
            description="Comprehensive beginner-to-intermediate guide for GenAI mastery.",
            overall_level="beginner",
            summary_recommendation="Building core foundations before advancing to RAG.",
            phases=[
                PhaseSpec(
                    phase_id="phase_01",
                    order=1,
                    title="LLM Foundations & Tokens",
                    description="Understanding how language models process text.",
                    skills=["LLM Fundamentals", "Tokens & Context Windows"],
                    prerequisite_phase_ids=[],
                    learning_objectives=["Explain tokenization", "Calculate context window limits"],
                    learning_outcomes=["Understand foundational transformer concepts"],
                    resource_topics=["Tokenization mechanics", "LLM architectures"],
                    project=ProjectSpec(
                        title="Token Counter & Cost Calculator",
                        description="Build a simple CLI tool to measure prompt token counts",
                        deliverable="Python CLI script",
                        estimated_hours=3.0
                    ),
                    estimated_hours=5.0,
                    difficulty="beginner",
                    recommendation_reason="Foundation required before exploring embeddings.",
                    completion_criteria=CompletionCriteria(assessment_required=True, mastery_threshold=70.0),
                    status="available"
                ),
                PhaseSpec(
                    phase_id="phase_02",
                    order=2,
                    title="Vector Embeddings",
                    description="Representing text semantically using vector spaces.",
                    skills=["Embeddings"],
                    prerequisite_phase_ids=["phase_01"],
                    learning_objectives=["Generate vector embeddings using OpenAI/HuggingFace", "Compute cosine similarity"],
                    learning_outcomes=["Build semantic search tools"],
                    resource_topics=["Semantic similarity", "Vector space theory"],
                    project=ProjectSpec(
                        title="Semantic Document Search",
                        description="Create semantic similarity search tool",
                        deliverable="Jupyter Notebook demonstrating similarity search",
                        estimated_hours=4.0
                    ),
                    estimated_hours=6.0,
                    difficulty="intermediate",
                    recommendation_reason="Embeddings are a prerequisite for RAG and Vector Databases.",
                    completion_criteria=CompletionCriteria(assessment_required=True, mastery_threshold=70.0),
                    status="locked"
                ),
                PhaseSpec(
                    phase_id="phase_03",
                    order=3,
                    title="RAG Systems",
                    description="Augmenting LLMs with vector database retrieval.",
                    skills=["Vector Databases", "RAG"],
                    prerequisite_phase_ids=["phase_02"],
                    learning_objectives=["Index documents in Chroma/Qdrant", "Build QA chatbot with document context"],
                    learning_outcomes=["Functional RAG system"],
                    resource_topics=["RAG pipelines", "Chunking strategies"],
                    project=ProjectSpec(
                        title="Document Q&A Assistant",
                        description="Build a RAG application for PDF documentation",
                        deliverable="Full-stack Python application",
                        estimated_hours=8.0
                    ),
                    estimated_hours=10.0,
                    difficulty="intermediate",
                    recommendation_reason="Achieves your primary learning goal of building RAG apps.",
                    completion_criteria=CompletionCriteria(assessment_required=True, mastery_threshold=75.0),
                    status="locked"
                )
            ],
            capstone_project=CapstoneProject(
                title="Personal AI Document Assistant",
                description="Build a full document indexing and query system.",
                deliverables=["GitHub repository", "Demo video"],
                estimated_hours=15.0
            )
        )  # type: ignore

from app.schemas.learner import DomainInfo, YearsOfExperience, LearningFormat, DailyLearningTime, ExperienceLevel

def create_mock_learner(
    user_id: str,
    domain: str = "generative_ai",
    exp_level: str = "beginner",
    learning_goal: str = "Learn GenAI",
    career_goal: str = "AI Engineer"
) -> LearnerProfileResponse:
    return LearnerProfileResponse(
        user_id=uuid.UUID(user_id),
        full_name="Test Learner",
        email=f"test_{user_id[:8]}@example.com",
        selected_domain=DomainInfo(id=domain, name=domain.replace("_", " ").title()),
        experience_level=ExperienceLevel(exp_level),
        years_of_experience=YearsOfExperience.one_to_two,
        learning_goal=learning_goal,
        career_goal=career_goal,
        motivation="Career growth",
        current_skills=["Python"],
        interests=["AI"],
        projects=[],
        certifications=[],
        completed_courses=[],
        preferred_learning_formats=[LearningFormat.interactive],
        daily_learning_time=DailyLearningTime.time_1_2_hours,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    )

def create_mock_skill_gap(
    user_id: str,
    domain: str = "generative_ai",
    critical_gaps: list = None,
    high_gaps: list = None,
    strong_skills: list = None
) -> SkillGapResult:
    return SkillGapResult(
        analysis_id=uuid.uuid4(),
        user_id=uuid.UUID(user_id),
        assessment_attempt_id=uuid.uuid4(),
        domain=domain,
        career_goal="AI Engineer",
        learning_goal="Master GenAI",
        overall_assessment_score=55.0,
        overall_proficiency="intermediate",
        skills=[
            SkillGapItem(
                skill="RAG",
                current_score=30.0,
                current_proficiency="beginner",
                target_score=75.0,
                gap_score=45.0,
                severity="critical_gap",
                confidence="high",
                priority_score=90.0,
                priority="critical",
                prerequisites=["Embeddings", "Vector Databases"],
                reason="High gap in primary goal area"
            )
        ],
        strong_skills=strong_skills or ["Python"],
        minor_gaps=[],
        moderate_gaps=[],
        high_gaps=high_gaps or ["Embeddings", "Vector Databases"],
        critical_gaps=critical_gaps or ["RAG"],
        recommended_focus=[
            RecommendedFocusItem(order=1, skill="Embeddings", reason="Required prerequisite for RAG"),
            RecommendedFocusItem(order=2, skill="Vector Databases", reason="Required prerequisite for RAG"),
            RecommendedFocusItem(order=3, skill="RAG", reason="Primary learning target")
        ],
        summary="Learner has critical gap in RAG and requires prerequisites Embeddings and Vector Databases.",
        generated_at=datetime.utcnow()
    )

@pytest.mark.asyncio
async def test_llm_mock_test_without_api_key():
    """Verify that unit tests pass with FakeLLMService without needing an API key."""
    fake_service = FakeLLMService()
    agent = LearningPathAgent(llm_service_instance=fake_service)
    
    user_id = str(uuid.uuid4())
    input_data = LearningPathAgentInput(
        learner_profile=create_mock_learner(user_id),
        skill_gap_result=create_mock_skill_gap(user_id),
        skill_knowledge={}
    )

    result = await agent.run(input_data)
    assert result is not None
    assert result.user_id == uuid.UUID(user_id)
    assert result.total_phases > 0
    assert result.phases[0].status == "available"
    assert result.phases[1].status == "locked"

@pytest.mark.asyncio
async def test_personalization_test():
    """Verify that beginner and advanced learners receive meaningfully different paths."""
    user_a = str(uuid.uuid4())
    user_b = str(uuid.uuid4())

    input_a = LearningPathAgentInput(
        learner_profile=create_mock_learner(user_a, exp_level="beginner", learning_goal="Learn GenAI from scratch"),
        skill_gap_result=create_mock_skill_gap(user_a, critical_gaps=["LLM Fundamentals", "RAG"]),
        skill_knowledge={}
    )

    input_b = LearningPathAgentInput(
        learner_profile=create_mock_learner(user_b, exp_level="advanced", learning_goal="Build production RAG systems"),
        skill_gap_result=create_mock_skill_gap(user_b, critical_gaps=["RAG", "LLM Evaluation"], strong_skills=["LLM Fundamentals"]),
        skill_knowledge={}
    )

    agent = LearningPathAgent(llm_service_instance=FakeLLMService())
    result_a = await agent.run(input_a)
    result_b = await agent.run(input_b)

    # Verify differences
    assert result_a.title != result_b.title
    assert result_a.overall_level == "beginner"
    assert result_b.overall_level == "advanced"
    assert result_a.phases[0].title != result_b.phases[0].title
    assert result_a.capstone_project.title != result_b.capstone_project.title
    assert result_a.estimated_total_hours != result_b.estimated_total_hours

@pytest.mark.asyncio
async def test_prerequisite_topological_sort_test():
    """Verify that prerequisites appear BEFORE dependent skills in the final phase sequence."""
    # Construct a mock output where LLM mistakenly puts RAG (dependent) BEFORE Embeddings and Vector Databases
    flawed_llm_output = LearningPathLLMOutput(
        title="Flawed Order LLM Output",
        description="Testing backend prerequisite correction",
        overall_level="intermediate",
        summary_recommendation="Testing sorting",
        phases=[
            PhaseSpec(
                phase_id="phase_01",
                order=1,
                title="RAG Systems",
                description="RAG topics",
                skills=["RAG"],
                prerequisite_phase_ids=[],
                learning_objectives=["Build RAG"],
                learning_outcomes=["RAG app"],
                resource_topics=["RAG"],
                project=ProjectSpec(title="RAG Proj", description="Desc", deliverable="Code", estimated_hours=4.0),
                estimated_hours=6.0,
                difficulty="intermediate",
                recommendation_reason="High gap",
                completion_criteria=CompletionCriteria(),
                status="available"
            ),
            PhaseSpec(
                phase_id="phase_02",
                order=2,
                title="Embeddings & Vectors",
                description="Embeddings topics",
                skills=["Embeddings", "Vector Databases"],
                prerequisite_phase_ids=[],
                learning_objectives=["Learn embeddings"],
                learning_outcomes=["Embeddings skill"],
                resource_topics=["Embeddings"],
                project=ProjectSpec(title="Emb Proj", description="Desc", deliverable="Code", estimated_hours=4.0),
                estimated_hours=6.0,
                difficulty="intermediate",
                recommendation_reason="Prerequisite",
                completion_criteria=CompletionCriteria(),
                status="locked"
            )
        ],
        capstone_project=CapstoneProject(title="Cap", description="Desc", deliverables=["Doc"], estimated_hours=10.0)
    )

    fake_service = FakeLLMService(mock_output=flawed_llm_output)
    agent = LearningPathAgent(llm_service_instance=fake_service)

    user_id = str(uuid.uuid4())
    input_data = LearningPathAgentInput(
        learner_profile=create_mock_learner(user_id, domain="generative_ai"),
        skill_gap_result=create_mock_skill_gap(user_id, domain="generative_ai"),
        skill_knowledge={}
    )

    result = await agent.run(input_data)

    # In GenAI domain: RAG requires Embeddings and Vector Databases.
    # The topological sort MUST re-order Embeddings & Vectors BEFORE RAG!
    first_phase_skills = result.phases[0].skills
    second_phase_skills = result.phases[1].skills

    assert "Embeddings" in first_phase_skills or "Vector Databases" in first_phase_skills
    assert "RAG" in second_phase_skills
    assert result.phases[0].status == "available"
    assert result.phases[1].status == "locked"

@pytest.mark.asyncio
async def test_domain_isolation_test():
    """Verify that foreign-domain skills (e.g. Docker or React in a GenAI path) are filtered out."""
    flawed_llm_output = LearningPathLLMOutput(
        title="GenAI Path with Mixed Skills",
        description="Testing domain isolation filter",
        overall_level="beginner",
        summary_recommendation="Testing isolation",
        phases=[
            PhaseSpec(
                phase_id="phase_01",
                order=1,
                title="Mixed Skills Phase",
                description="Contains foreign skills",
                skills=["Embeddings", "Docker", "React"],
                prerequisite_phase_ids=[],
                learning_objectives=["Learn embeddings"],
                learning_outcomes=["Outcome"],
                resource_topics=["Topics"],
                project=ProjectSpec(title="Proj", description="Desc", deliverable="Del", estimated_hours=4.0),
                estimated_hours=5.0,
                difficulty="beginner",
                recommendation_reason="Reason",
                completion_criteria=CompletionCriteria(),
                status="available"
            )
        ],
        capstone_project=CapstoneProject(title="Cap", description="Desc", deliverables=["Del"], estimated_hours=8.0)
    )

    fake_service = FakeLLMService(mock_output=flawed_llm_output)
    agent = LearningPathAgent(llm_service_instance=fake_service)

    user_id = str(uuid.uuid4())
    input_data = LearningPathAgentInput(
        learner_profile=create_mock_learner(user_id, domain="generative_ai"),
        skill_gap_result=create_mock_skill_gap(user_id, domain="generative_ai"),
        skill_knowledge={}
    )

    result = await agent.run(input_data)
    skills = result.phases[0].skills

    assert "Embeddings" in skills
    assert "Docker" not in skills
    assert "React" not in skills
