from pydantic import BaseModel, ConfigDict, Field
from typing import List, Dict, Any, Optional
from uuid import UUID
from datetime import datetime
from app.schemas.learner import LearnerProfileResponse
from app.schemas.skill_gap import SkillGapResult

class ProjectSpec(BaseModel):
    title: str = Field(default="Hands-on Phase Project", description="Short descriptive title of the practical project")
    description: str = Field(default="Apply skills learned in this phase to build a practical deliverable.", description="Detailed instructions and requirements")
    deliverable: str = Field(default="Source code and project documentation", description="Expected output or artifact produced")
    estimated_hours: float = Field(default=4.0, description="Estimated time in hours to complete the project")

    model_config = ConfigDict(from_attributes=True, populate_by_name=True)

class CompletionCriteria(BaseModel):
    assessment_required: bool = Field(default=True, description="Whether a quiz or evaluation is required")
    mastery_threshold: float = Field(default=70.0, description="Minimum score percentage required to pass phase")

    model_config = ConfigDict(from_attributes=True, populate_by_name=True)

class PhaseSpec(BaseModel):
    phase_id: str = Field(default="phase_01", description="Unique identifier for phase, e.g., 'phase_01'")
    order: int = Field(default=1, alias="phase_number", description="Sequencing order starting from 1")
    title: str = Field(default="Learning Phase", description="Clear title of the learning phase")
    description: str = Field(default="Overview of topics and skills developed in this phase.", description="Overview of topics covered")
    skills: List[str] = Field(default_factory=list, alias="target_skills", description="List of target skills developed in this phase")
    prerequisite_phase_ids: List[str] = Field(default_factory=list, description="IDs of prerequisite phases")
    learning_objectives: List[str] = Field(default_factory=list, description="Measurable action-oriented learning objectives")
    learning_outcomes: List[str] = Field(default_factory=list, description="Key practical abilities gained upon completion")
    resource_topics: List[str] = Field(default_factory=list, description="Conceptual resource topic strings for study")
    project: ProjectSpec = Field(default_factory=ProjectSpec, description="Practical hands-on project for the phase")
    estimated_hours: float = Field(default=6.0, description="Estimated effort in hours (2 to 18 hours per phase)")
    difficulty: str = Field(default="intermediate", description="Difficulty level: beginner, intermediate, advanced")
    recommendation_reason: str = Field(default="Prioritized based on learner skill gaps and learning goal alignment.", description="Personalized explanation")
    completion_criteria: CompletionCriteria = Field(default_factory=CompletionCriteria, description="Mastery & completion criteria")
    status: str = Field(default="locked", description="Phase availability status: 'available' or 'locked'")

    model_config = ConfigDict(from_attributes=True, populate_by_name=True)

class CapstoneProject(BaseModel):
    title: str = Field(default="Final Capstone Project", description="Title of the overall capstone project")
    description: str = Field(default="Comprehensive final capstone project synthesizing learning path skills.", description="Comprehensive project description")
    deliverables: List[str] = Field(default_factory=lambda: ["GitHub Repository", "Project Documentation"], description="List of key deliverables")
    estimated_hours: float = Field(default=15.0, description="Estimated time in hours to complete capstone project")

    model_config = ConfigDict(from_attributes=True, populate_by_name=True)

class LearningPathLLMOutput(BaseModel):
    title: str = Field(default="Personalized Learning Path", description="Overarching title for the personalized learning path")
    description: str = Field(default="Personalized learning journey tailored to your goals and skill gaps.", description="High-level description")
    overall_level: str = Field(default="intermediate", description="Target proficiency level of the learning path")
    summary_recommendation: str = Field(default="Tailored path focusing on key skill gaps and prerequisites.", description="High-level personalized recommendation summary")
    phases: List[PhaseSpec] = Field(default_factory=list, description="Ordered list of learning path phases (3 to 8 phases)")
    capstone_project: CapstoneProject = Field(default_factory=CapstoneProject, description="Final capstone project synthesizing path skills")

    model_config = ConfigDict(from_attributes=True, populate_by_name=True)

class LearningPathAgentInput(BaseModel):
    learner_profile: LearnerProfileResponse
    skill_gap_result: SkillGapResult
    skill_knowledge: Dict[str, Any]

    model_config = ConfigDict(from_attributes=True, populate_by_name=True)

class LearningPathResult(BaseModel):
    path_id: UUID
    user_id: UUID
    skill_gap_analysis_id: UUID
    domain: str
    title: str
    description: str
    learning_goal: str
    career_goal: str
    overall_level: str
    total_phases: int
    estimated_total_hours: float
    phases: List[PhaseSpec]
    capstone_project: CapstoneProject
    generated_at: datetime

    model_config = ConfigDict(from_attributes=True, populate_by_name=True)

class UserPathSummary(BaseModel):
    path_id: UUID
    domain: str
    title: str
    description: str
    learning_goal: str
    career_goal: str
    experience_level: str
    status: str
    progress_percentage: float
    completed_phases: int
    total_phases: int
    phases: List[PhaseSpec] = Field(default_factory=list)
    created_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True, populate_by_name=True)

class UserLearningPathsResponse(BaseModel):
    user_id: UUID
    paths: List[UserPathSummary]

    model_config = ConfigDict(from_attributes=True, populate_by_name=True)

