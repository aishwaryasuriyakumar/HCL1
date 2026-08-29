from pydantic import BaseModel, ConfigDict
from typing import List, Optional
from uuid import UUID
from datetime import datetime

class OptionPublic(BaseModel):
    id: str
    text: str

    model_config = ConfigDict(from_attributes=True)

class QuestionPublic(BaseModel):
    id: str
    skill: str
    difficulty: str
    question: str
    options: List[OptionPublic]

    model_config = ConfigDict(from_attributes=True)

class AssessmentStartRequest(BaseModel):
    user_id: UUID

class AssessmentStartResponse(BaseModel):
    attempt_id: UUID
    user_id: UUID
    domain: str
    status: str
    total_questions: int
    questions: List[QuestionPublic]
    started_at: datetime

    model_config = ConfigDict(from_attributes=True)

class AnswerSubmit(BaseModel):
    question_id: str
    selected_option_id: str

class AssessmentSubmitRequest(BaseModel):
    answers: List[AnswerSubmit]

class SkillResult(BaseModel):
    skill: str
    questions_attempted: int
    correct_answers: int
    score: float
    proficiency: str
    confidence: str

    model_config = ConfigDict(from_attributes=True)

class OverallResult(BaseModel):
    total_questions: int
    correct_answers: int
    incorrect_answers: int
    score: float
    proficiency: str

    model_config = ConfigDict(from_attributes=True)

class AssessmentResult(BaseModel):
    attempt_id: UUID
    user_id: UUID
    domain: str
    status: str
    overall: OverallResult
    skill_results: List[SkillResult]
    started_at: datetime
    submitted_at: datetime

    model_config = ConfigDict(from_attributes=True)

class ReviewAnswerDetail(BaseModel):
    question_id: str
    skill: str
    difficulty: str
    question: str
    selected_answer: Optional[OptionPublic] = None
    correct_answer: OptionPublic
    is_correct: bool
    explanation: str

    model_config = ConfigDict(from_attributes=True)

class AssessmentHistoryItem(BaseModel):
    attempt_id: UUID
    domain: str
    status: str
    score: Optional[float] = None
    proficiency: Optional[str] = None
    started_at: datetime
    submitted_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)

class AssessmentHistoryResponse(BaseModel):
    user_id: UUID
    attempts: List[AssessmentHistoryItem]

    model_config = ConfigDict(from_attributes=True)
