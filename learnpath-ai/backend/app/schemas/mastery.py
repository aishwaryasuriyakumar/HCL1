from pydantic import BaseModel
from typing import List
from uuid import UUID

class MasteryResult(BaseModel):
    user_id: UUID
    phase_id: str
    score: float
    passed: bool
    weak_topics: List[str]
    next_action: str
