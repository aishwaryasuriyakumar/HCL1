from sqlalchemy import Column, String, DateTime, ForeignKey, JSON
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid
from app.database.base import Base

class LearningPath(Base):
    __tablename__ = "learning_paths"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String, ForeignKey("learners.user_id"), nullable=False)
    skill_gap_analysis_id = Column(String, ForeignKey("skill_gap_analyses.id"), nullable=False)
    domain = Column(String, nullable=False)
    path_json = Column(JSON, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    learner = relationship("Learner", backref="learning_paths")
    skill_gap_analysis = relationship("SkillGapAnalysis", backref="learning_path")
