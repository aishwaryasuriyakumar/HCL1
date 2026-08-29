from pydantic import BaseModel
from uuid import UUID

class RecommendedResource(BaseModel):
    resource_id: UUID
    phase_id: str
    title: str
    provider: str
    url: str
    resource_type: str
    is_free: bool
    availability_status: str
    relevance_score: float
    quality_score: float
    why_recommended: str
    learning_outcome: str
