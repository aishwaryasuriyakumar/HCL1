from pydantic import BaseModel, ConfigDict
from typing import List, Optional
from uuid import UUID
from datetime import datetime

# Import existing schemas to reuse the contracts
from app.schemas.learner import LearnerProfileResponse
from app.schemas.assessment import AssessmentResult

class SkillGapAgentInput(BaseModel):
    learner: LearnerProfileResponse
    assessment: AssessmentResult

    model_config = ConfigDict(from_attributes=True)

class SkillGapItem(BaseModel):
    skill: str
    current_score: float
    current_proficiency: str
    target_score: float
    gap_score: float
    severity: str
    confidence: str
    priority_score: float
    priority: str
    prerequisites: List[str]
    reason: str

    model_config = ConfigDict(from_attributes=True)

class RecommendedFocusItem(BaseModel):
    order: int
    skill: str
    reason: str

    model_config = ConfigDict(from_attributes=True)

class SkillGapResult(BaseModel):
    analysis_id: UUID
    user_id: UUID
    assessment_attempt_id: UUID
    domain: str
    career_goal: str
    learning_goal: str
    overall_assessment_score: float
    overall_proficiency: str
    skills: List[SkillGapItem]
    strong_skills: List[str]
    minor_gaps: List[str]
    moderate_gaps: List[str]
    high_gaps: List[str]
    critical_gaps: List[str]
    recommended_focus: List[RecommendedFocusItem]
    summary: str
    generated_at: datetime

    model_config = ConfigDict(from_attributes=True)

# Contract for the future Personalized Learning Path Agent
class LearningPathAgentInput(BaseModel):
    learner: LearnerProfileResponse
    skill_gap: SkillGapResult

    model_config = ConfigDict(from_attributes=True)
