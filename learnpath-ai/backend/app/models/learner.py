from sqlalchemy import Column, String, JSON, DateTime, Enum as SQLAlchemyEnum
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime
import uuid
from app.database.base import Base
from app.schemas.learner import ExperienceLevel, YearsOfExperience, DailyLearningTime

class Learner(Base):
    __tablename__ = "learners"

    # SQLite compatibility for UUID
    user_id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    full_name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    selected_domain = Column(String, nullable=False)
    experience_level = Column(String, nullable=False)
    years_of_experience = Column(String, nullable=True)
    learning_goal = Column(String, nullable=False)
    career_goal = Column(String, nullable=False)
    motivation = Column(String, nullable=True)
    
    current_skills = Column(JSON, default=list)
    interests = Column(JSON, default=list)
    projects = Column(JSON, default=list)
    certifications = Column(JSON, default=list)
    completed_courses = Column(JSON, default=list)
    preferred_learning_formats = Column(JSON, default=list)
    
    daily_learning_time = Column(String, nullable=True)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
