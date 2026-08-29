from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from app.models.learner import Learner
from app.schemas.learner import LearnerProfileCreate, LearnerProfileUpdate
from uuid import UUID

class LearnerRepository:
    def get_by_id(self, db: Session, user_id: str):
        return db.query(Learner).filter(Learner.user_id == user_id).first()

    def get_by_email(self, db: Session, email: str):
        return db.query(Learner).filter(Learner.email == email).first()

    def create(self, db: Session, learner_in: LearnerProfileCreate):
        db_obj = Learner(
            full_name=learner_in.full_name,
            email=learner_in.email,
            selected_domain=learner_in.selected_domain,
            experience_level=learner_in.experience_level,
            years_of_experience=learner_in.years_of_experience,
            learning_goal=learner_in.learning_goal,
            career_goal=learner_in.career_goal,
            motivation=learner_in.motivation,
            current_skills=learner_in.current_skills,
            interests=learner_in.interests,
            projects=[p.model_dump() for p in learner_in.projects],
            certifications=[c.model_dump() for c in learner_in.certifications],
            completed_courses=[c.model_dump() for c in learner_in.completed_courses],
            preferred_learning_formats=learner_in.preferred_learning_formats,
            daily_learning_time=learner_in.daily_learning_time
        )
        db.add(db_obj)
        try:
            db.commit()
            db.refresh(db_obj)
            return db_obj
        except IntegrityError:
            db.rollback()
            return None

    def update(self, db: Session, db_obj: Learner, obj_in: LearnerProfileUpdate):
        update_data = obj_in.model_dump(exclude_unset=True)
        
        # Serialize nested lists of dicts
        for field in ['projects', 'certifications', 'completed_courses']:
            if field in update_data and update_data[field] is not None:
                update_data[field] = [item for item in update_data[field]]
        
        for field in update_data:
            setattr(db_obj, field, update_data[field])
            
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

learner_repo = LearnerRepository()
