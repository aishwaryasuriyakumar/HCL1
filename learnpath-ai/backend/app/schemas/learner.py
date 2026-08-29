from pydantic import BaseModel, EmailStr, Field, field_validator
from typing import List, Optional
from uuid import UUID
from enum import Enum
from datetime import datetime
from app.data.domains import DOMAINS

class ExperienceLevel(str, Enum):
    beginner = "beginner"
    intermediate = "intermediate"
    advanced = "advanced"
    professional = "professional"

class YearsOfExperience(str, Enum):
    none = "none"
    less_than_1 = "less_than_1"
    one_to_two = "1_2"
    three_to_five = "3_5"
    five_plus = "5_plus"

class CourseStatus(str, Enum):
    completed = "completed"
    in_progress = "in_progress"

class LearningFormat(str, Enum):
    video = "video"
    reading = "reading"
    hands_on = "hands_on"
    interactive = "interactive"
    mixed = "mixed"

class DailyLearningTime(str, Enum):
    time_15_30_min = "15_30_min"
    time_30_60_min = "30_60_min"
    time_1_2_hours = "1_2_hours"
    time_2_plus_hours = "2_plus_hours"

class ProjectInput(BaseModel):
    name: str
    description: Optional[str] = None
    technologies: List[str] = Field(default_factory=list)
    url: Optional[str] = None

class CertificationInput(BaseModel):
    name: str
    issuing_organization: str
    year: Optional[int] = None

class CompletedCourseInput(BaseModel):
    name: str
    platform: str
    status: CourseStatus

class LearnerProfileCreate(BaseModel):
    full_name: str
    email: EmailStr
    selected_domain: str
    experience_level: ExperienceLevel
    years_of_experience: Optional[YearsOfExperience] = None
    learning_goal: str
    career_goal: str
    motivation: Optional[str] = None
    current_skills: List[str] = Field(default_factory=list)
    interests: List[str] = Field(default_factory=list)
    projects: List[ProjectInput] = Field(default_factory=list)
    certifications: List[CertificationInput] = Field(default_factory=list)
    completed_courses: List[CompletedCourseInput] = Field(default_factory=list)
    preferred_learning_formats: List[LearningFormat] = Field(default_factory=list)
    daily_learning_time: Optional[DailyLearningTime] = None

    @field_validator('selected_domain')
    def validate_domain(cls, v):
        if v not in DOMAINS:
            raise ValueError(f"Invalid domain. Supported domains are: {list(DOMAINS.keys())}")
        return v

class LearnerProfileUpdate(BaseModel):
    full_name: Optional[str] = None
    email: Optional[EmailStr] = None
    selected_domain: Optional[str] = None
    experience_level: Optional[ExperienceLevel] = None
    years_of_experience: Optional[YearsOfExperience] = None
    learning_goal: Optional[str] = None
    career_goal: Optional[str] = None
    motivation: Optional[str] = None
    current_skills: Optional[List[str]] = None
    interests: Optional[List[str]] = None
    projects: Optional[List[ProjectInput]] = None
    certifications: Optional[List[CertificationInput]] = None
    completed_courses: Optional[List[CompletedCourseInput]] = None
    preferred_learning_formats: Optional[List[LearningFormat]] = None
    daily_learning_time: Optional[DailyLearningTime] = None
    
    @field_validator('selected_domain')
    def validate_domain(cls, v):
        if v is not None and v not in DOMAINS:
            raise ValueError(f"Invalid domain. Supported domains are: {list(DOMAINS.keys())}")
        return v

from pydantic import ConfigDict

class DomainInfo(BaseModel):
    id: str
    name: str

class LearnerProfileResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    user_id: UUID
    full_name: str
    email: EmailStr
    selected_domain: DomainInfo
    experience_level: ExperienceLevel
    years_of_experience: Optional[YearsOfExperience] = None
    learning_goal: str
    career_goal: str
    motivation: Optional[str] = None
    current_skills: List[str]
    interests: List[str]
    projects: List[ProjectInput]
    certifications: List[CertificationInput]
    completed_courses: List[CompletedCourseInput]
    preferred_learning_formats: List[LearningFormat]
    daily_learning_time: Optional[DailyLearningTime] = None
    created_at: datetime
    updated_at: datetime
