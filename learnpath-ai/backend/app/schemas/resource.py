from enum import Enum
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field
from datetime import datetime
from uuid import UUID, uuid4

class AccessType(str, Enum):
    PUBLIC_FREE = "public_free"
    PUBLIC_ACCOUNT_REQUIRED = "public_account_required"
    PAID = "paid"
    RESTRICTED = "restricted"
    UNKNOWN = "unknown"

class VerificationStatus(str, Enum):
    VERIFIED = "verified"
    UNVERIFIED = "unverified"
    INACTIVE = "inactive"
    RESTRICTED = "restricted"
    ERROR = "error"

class ResourceCandidate(BaseModel):
    resource_id: str = Field(default_factory=lambda: str(uuid4()))
    platform: str
    title: str
    original_url: str
    description: str = ""
    resource_type: str = "article"  # video, article, interactive, course, documentation
    skills: List[str] = Field(default_factory=list)
    difficulty: str = "intermediate"
    rating: Optional[float] = None
    review_count: Optional[int] = None
    is_free: bool = True
    access_type: AccessType = AccessType.PUBLIC_FREE
    duration_minutes: Optional[float] = None
    published_at: Optional[datetime] = None
    source_domain: str = ""
    last_verified_at: Optional[datetime] = None
    is_active: bool = True
    is_publicly_accessible: bool = True
    metadata: Dict[str, Any] = Field(default_factory=dict)
    overall_score: Optional[float] = None
    why_recommended: Optional[str] = None

class ResourceCardData(BaseModel):
    resource_id: str
    title: str
    platform: str
    description: str
    resource_type: str
    difficulty: str
    is_free: bool
    access_type: AccessType
    duration_minutes: Optional[float] = None
    rating: Optional[float] = None
    review_count: Optional[int] = None
    overall_score: float
    why_recommended: str
    original_url: str
    is_active: bool = True
    last_verified_at: datetime

class PhaseResources(BaseModel):
    phase_id: str
    resources: List[ResourceCardData]

class CuratedPathResources(BaseModel):
    path_id: UUID
    phases: List[PhaseResources]
    curated_at: datetime = Field(default_factory=datetime.utcnow)

class ProviderStatusItem(BaseModel):
    platform: str
    status: str  # "available", "unavailable"
    reason: Optional[str] = None

class ProviderStatusResponse(BaseModel):
    providers: List[ProviderStatusItem]
