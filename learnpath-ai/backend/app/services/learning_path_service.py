import logging
from typing import Optional
from sqlalchemy.orm import Session
from fastapi import HTTPException

from app.models.learner import Learner
from app.models.assessment import SkillGapAnalysis
from app.models.learning_path import LearningPath
from app.repositories.learner_repository import learner_repo
from app.services.profile_service import profile_service
from app.agents.learning_path_agent import LearningPathAgent
from app.schemas.skill_gap import SkillGapResult
from app.schemas.learning_path import LearningPathAgentInput, LearningPathResult
from app.data.skill_requirements import PREREQUISITES, SKILL_TARGET_SCORES, SKILL_IMPORTANCE_LEVELS

logger = logging.getLogger(__name__)

class LearningPathService:
    async def generate_learning_path(
        self, db: Session, user_id: str, agent_override: Optional[LearningPathAgent] = None
    ) -> LearningPathResult:
        logger.info(f"Initiating learning path generation for user {user_id}")
        
        # 1. Retrieve learner profile
        learner = learner_repo.get_by_id(db, user_id=user_id)
        if not learner:
            raise HTTPException(status_code=404, detail="Learner profile not found")

        # 2. Retrieve latest skill gap analysis for the learner
        latest_skill_gap = (
            db.query(SkillGapAnalysis)
            .filter(SkillGapAnalysis.user_id == user_id, SkillGapAnalysis.domain == learner.selected_domain)
            .order_by(SkillGapAnalysis.created_at.desc())
            .first()
        )

        if not latest_skill_gap:
            logger.warning(f"Skill gap analysis missing for user {user_id}")
            raise HTTPException(
                status_code=409,
                detail="Skill gap analysis required before learning path generation"
            )

        # 3. Idempotency Check: Return existing LearningPath if generated for this skill gap analysis
        existing_path = (
            db.query(LearningPath)
            .filter(
                LearningPath.user_id == user_id,
                LearningPath.skill_gap_analysis_id == latest_skill_gap.id
            )
            .first()
        )

        if existing_path:
            logger.info(f"Found existing learning path {existing_path.id} for skill gap analysis {latest_skill_gap.id}. Returning cached result.")
            return LearningPathResult(**existing_path.path_json)

        # 4. Map schemas for Agent boundary
        learner_pydantic = profile_service._map_to_response(learner)
        skill_gap_pydantic = SkillGapResult(**latest_skill_gap.result_json)

        domain = learner.selected_domain
        skill_knowledge = {
            "target_scores": SKILL_TARGET_SCORES.get(domain, {}),
            "importance_levels": SKILL_IMPORTANCE_LEVELS.get(domain, {}),
            "prerequisites": PREREQUISITES.get(domain, {}),
        }

        agent_input = LearningPathAgentInput(
            learner_profile=learner_pydantic,
            skill_gap_result=skill_gap_pydantic,
            skill_knowledge=skill_knowledge
        )

        # 5. Instantiate & run agent
        agent = agent_override or LearningPathAgent()
        result: LearningPathResult = await agent.run(agent_input)

        # 6. Persist to DB
        db_path = LearningPath(
            id=str(result.path_id),
            user_id=user_id,
            skill_gap_analysis_id=latest_skill_gap.id,
            domain=domain,
            path_json=result.model_dump(mode="json")
        )

        db.add(db_path)
        db.commit()
        db.refresh(db_path)
        logger.info(f"learning_path_persisted successfully stored learning path {db_path.id} for user {user_id}")

        return result

    def get_latest_path(self, db: Session, user_id: str) -> LearningPathResult:
        path = (
            db.query(LearningPath)
            .filter(LearningPath.user_id == user_id)
            .order_by(LearningPath.created_at.desc())
            .first()
        )
        if not path:
            raise HTTPException(status_code=404, detail="Learning path not found for user")
        return LearningPathResult(**path.path_json)

    def get_path(self, db: Session, path_id: str) -> LearningPathResult:
        path = db.query(LearningPath).filter(LearningPath.id == path_id).first()
        if not path:
            raise HTTPException(status_code=404, detail="Learning path not found")
        return LearningPathResult(**path.path_json)

    def get_path_model(self, db: Session, path_id: str) -> Optional[LearningPath]:
        return db.query(LearningPath).filter(LearningPath.id == path_id).first()

    def complete_phase(self, db: Session, learning_path_id: str, phase_id: str) -> None:
        db_path = self.get_path_model(db, learning_path_id)
        if not db_path:
            raise HTTPException(status_code=404, detail="Learning path not found")

        path_data = dict(db_path.path_json)
        phases = path_data.get("phases", [])
        updated = False

        for phase in phases:
            if phase.get("phase_id") == phase_id:
                phase["status"] = "completed"
                updated = True
                break

        if updated:
            db_path.path_json = path_data
            from sqlalchemy.orm.attributes import flag_modified
            flag_modified(db_path, "path_json")
            db.commit()
            db.refresh(db_path)
            logger.info(f"phase_completed successfully marked phase {phase_id} as completed in path {learning_path_id}")

    def unlock_next_phase(self, db: Session, learning_path_id: str, current_phase_id: str) -> Optional[str]:
        db_path = self.get_path_model(db, learning_path_id)
        if not db_path:
            raise HTTPException(status_code=404, detail="Learning path not found")

        path_data = dict(db_path.path_json)
        phases = path_data.get("phases", [])

        # Sort phases by order
        sorted_phases = sorted(phases, key=lambda p: p.get("order", 0))
        next_phase_id = None

        for idx, phase in enumerate(sorted_phases):
            if phase.get("phase_id") == current_phase_id:
                if idx + 1 < len(sorted_phases):
                    next_phase = sorted_phases[idx + 1]
                    next_phase_id = next_phase.get("phase_id")
                    if next_phase.get("status") == "locked":
                        next_phase["status"] = "available"
                break

        if next_phase_id:
            db_path.path_json = path_data
            from sqlalchemy.orm.attributes import flag_modified
            flag_modified(db_path, "path_json")
            db.commit()
            db.refresh(db_path)
            logger.info(f"next_phase_unlocked successfully unlocked next phase {next_phase_id} in path {learning_path_id}")

        return next_phase_id

    def is_final_phase(self, path_data: dict, phase_id: str) -> bool:
        phases = path_data.get("phases", [])
        if not phases:
            return True
        sorted_phases = sorted(phases, key=lambda p: p.get("order", 0))
        return sorted_phases[-1].get("phase_id") == phase_id

    def get_phase_info(self, path_data: dict, phase_id: str) -> Optional[dict]:
        phases = path_data.get("phases", [])
        for p in phases:
            if p.get("phase_id") == phase_id:
                return p
        return None

learning_path_service = LearningPathService()
