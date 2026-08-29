from sqlalchemy import Column, String, Integer, Float, Boolean, DateTime, ForeignKey, JSON
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid
from app.database.base import Base

class AssessmentAttempt(Base):
    __tablename__ = "assessment_attempts"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String, ForeignKey("learners.user_id"), nullable=False)
    domain = Column(String, nullable=False)
    status = Column(String, default="in_progress")  # in_progress, submitted
    selected_question_ids = Column(JSON, nullable=False)  # List of string question IDs
    
    started_at = Column(DateTime, default=datetime.utcnow)
    submitted_at = Column(DateTime, nullable=True)
    
    total_questions = Column(Integer, default=15)
    correct_answers = Column(Integer, nullable=True)
    overall_score = Column(Float, nullable=True)
    overall_proficiency = Column(String, nullable=True)

    # Relationships
    learner = relationship("Learner", backref="attempts")
    answers = relationship("AssessmentAnswer", backref="attempt", cascade="all, delete-orphan")
    skill_results = relationship("SkillAssessmentResult", backref="attempt", cascade="all, delete-orphan")

class AssessmentAnswer(Base):
    __tablename__ = "assessment_answers"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    attempt_id = Column(String, ForeignKey("assessment_attempts.id"), nullable=False)
    question_id = Column(String, nullable=False)
    selected_option_id = Column(String, nullable=False)
    is_correct = Column(Boolean, nullable=False)

class SkillAssessmentResult(Base):
    __tablename__ = "skill_assessment_results"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    attempt_id = Column(String, ForeignKey("assessment_attempts.id"), nullable=False)
    skill = Column(String, nullable=False)
    questions_attempted = Column(Integer, nullable=False)
    correct_answers = Column(Integer, nullable=False)
    score_percentage = Column(Float, nullable=False)
    proficiency_level = Column(String, nullable=False)
    confidence = Column(String, nullable=False)  # low, medium, high

class SkillGapAnalysis(Base):
    __tablename__ = "skill_gap_analyses"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String, ForeignKey("learners.user_id"), nullable=False)
    assessment_attempt_id = Column(String, ForeignKey("assessment_attempts.id"), nullable=False)
    domain = Column(String, nullable=False)
    overall_assessment_score = Column(Float, nullable=False)
    result_json = Column(JSON, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    learner = relationship("Learner", backref="skill_gaps")
    attempt = relationship("AssessmentAttempt", backref="skill_gap")

