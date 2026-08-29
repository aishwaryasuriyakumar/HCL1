from pydantic import BaseModel
from typing import List
from uuid import UUID

class ProgressSummary(BaseModel):
    user_id: UUID
    overall_progress: float
    completed_phases: int
    total_phases: int
    current_phase_id: str
    average_score: float
    completed_modules: List[str]
    remaining_modules: List[str]
    learning_speed: str
