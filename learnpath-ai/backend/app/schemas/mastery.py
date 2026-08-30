from pydantic import BaseModel, ConfigDict, Field
from typing import List, Dict, Any, Optional
from uuid import UUID
from datetime import datetime

class MasteryQuestionOption(BaseModel):
    id: str
    text: str

    model_config = ConfigDict(from_attributes=True)

class MasteryQuestionPublic(BaseModel):
    id: str
    question_id: str
    topic: str
    difficulty: str
    question: str
    options: List[MasteryQuestionOption]

    model_config = ConfigDict(from_attributes=True, populate_by_name=True)

class MasteryStartRequest(BaseModel):
    user_id: UUID
    phase_id: str

class MasteryStartResponse(BaseModel):
    mastery_attempt_id: UUID
    user_id: UUID
    phase_id: str
    attempt_number: int
    total_questions: int
    questions: List[MasteryQuestionPublic]

    model_config = ConfigDict(from_attributes=True)

class MasteryAnswerSubmission(BaseModel):
    question_id: str
    selected_option_id: str

class MasterySubmitRequest(BaseModel):
    answers: List[MasteryAnswerSubmission]

class MasteryTopicResult(BaseModel):
    topic: str
    questions_attempted: int
    correct_answers: int
    score: float
    status: str = Field(..., description="'mastered' or 'needs_improvement'")

    model_config = ConfigDict(from_attributes=True, populate_by_name=True)

class WeakTopicInfo(BaseModel):
    topic: str
    score: float
    reason: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)

class MasteryResult(BaseModel):
    mastery_attempt_id: UUID
    user_id: UUID
    learning_path_id: UUID
    phase_id: str
    phase_title: str
    score: float
    pass_threshold: float
    passed: bool
    topic_results: List[MasteryTopicResult]
    weak_topics: List[WeakTopicInfo]
    next_action: str
    attempt_number: int
    submitted_at: datetime
    explanation: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)

class MasteryAgentInput(BaseModel):
    user_id: UUID
    learning_path_id: UUID
    phase: Dict[str, Any]
    assessment_result: Optional[Dict[str, Any]] = None

    model_config = ConfigDict(from_attributes=True)

class RemediationRequest(BaseModel):
    user_id: UUID
    phase_id: str
    domain: str
    weak_topics: List[str]

    model_config = ConfigDict(from_attributes=True)

class MasteryReviewItem(BaseModel):
    question_id: str
    topic: str
    difficulty: str
    question: str
    options: List[MasteryQuestionOption]
    selected_option_id: str
    correct_option_id: str
    is_correct: bool
    explanation: str

    model_config = ConfigDict(from_attributes=True)

class MasteryReviewResponse(BaseModel):
    mastery_attempt_id: UUID
    score: float
    passed: bool
    questions: List[MasteryReviewItem]

    model_config = ConfigDict(from_attributes=True)

class MasteryAttemptHistoryItem(BaseModel):
    mastery_attempt_id: UUID
    attempt_number: int
    score: Optional[float] = None
    passed: Optional[bool] = None
    weak_topics: List[str] = []
    submitted_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)
