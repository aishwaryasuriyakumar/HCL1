from sqlalchemy import Column, String, Float, Boolean, Integer, DateTime, ForeignKey, JSON
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid
from app.database.base import Base

class MasteryAttempt(Base):
    __tablename__ = "mastery_attempts"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String, ForeignKey("learners.user_id"), nullable=False)
    learning_path_id = Column(String, ForeignKey("learning_paths.id"), nullable=False)
    phase_id = Column(String, nullable=False)
    status = Column(String, default="in_progress")  # "in_progress", "submitted"
    selected_question_ids = Column(JSON, nullable=False, default=list)
    started_at = Column(DateTime, default=datetime.utcnow)
    submitted_at = Column(DateTime, nullable=True)
    score = Column(Float, nullable=True)
    passed = Column(Boolean, nullable=True)
    attempt_number = Column(Integer, default=1)
    remediation_completed = Column(Boolean, default=False)
    result_json = Column(JSON, nullable=True)

    learner = relationship("Learner", backref="mastery_attempts")
    learning_path = relationship("LearningPath", backref="mastery_attempts")
    answers = relationship("MasteryAnswer", back_populates="attempt", cascade="all, delete-orphan")

class MasteryAnswer(Base):
    __tablename__ = "mastery_answers"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    mastery_attempt_id = Column(String, ForeignKey("mastery_attempts.id"), nullable=False)
    question_id = Column(String, nullable=False)
    selected_option_id = Column(String, nullable=False)
    is_correct = Column(Boolean, nullable=False)

    attempt = relationship("MasteryAttempt", back_populates="answers")
