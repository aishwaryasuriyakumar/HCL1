from pydantic import BaseModel
from typing import List
from uuid import UUID

class Phase(BaseModel):
    phase_id: str
    order: int
    title: str
    description: str
    skills: List[str]
    prerequisites: List[str]
    estimated_hours: int
    status: str

class LearningPathResult(BaseModel):
    user_id: UUID
    domain: str
    goal: str
    phases: List[Phase]
