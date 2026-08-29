from sqlalchemy.orm import Session
from datetime import datetime
from app.models.assessment import AssessmentAttempt, AssessmentAnswer, SkillAssessmentResult
from typing import List, Optional

class AssessmentRepository:
    def get_attempt(self, db: Session, attempt_id: str) -> Optional[AssessmentAttempt]:
        return db.query(AssessmentAttempt).filter(AssessmentAttempt.id == attempt_id).first()

    def get_active_attempt(self, db: Session, user_id: str, domain: str) -> Optional[AssessmentAttempt]:
        return db.query(AssessmentAttempt).filter(
            AssessmentAttempt.user_id == user_id,
            AssessmentAttempt.domain == domain,
            AssessmentAttempt.status == "in_progress"
        ).first()

    def get_attempts_by_user(self, db: Session, user_id: str) -> List[AssessmentAttempt]:
        return db.query(AssessmentAttempt).filter(
            AssessmentAttempt.user_id == user_id
        ).order_by(AssessmentAttempt.started_at.desc()).all()

    def create_attempt(self, db: Session, attempt: AssessmentAttempt) -> AssessmentAttempt:
        db.add(attempt)
        db.commit()
        db.refresh(attempt)
        return attempt

    def save_answers_and_results(
        self,
        db: Session,
        attempt: AssessmentAttempt,
        answers: List[AssessmentAnswer],
        skill_results: List[SkillAssessmentResult]
    ) -> AssessmentAttempt:
        # Atomic commit
        attempt.status = "submitted"
        attempt.submitted_at = datetime.utcnow()
        
        db.add(attempt)
        for ans in answers:
            db.add(ans)
        for res in skill_results:
            db.add(res)
            
        db.commit()
        db.refresh(attempt)
        return attempt

assessment_repo = AssessmentRepository()
