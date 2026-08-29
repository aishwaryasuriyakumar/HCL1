import logging
from typing import List, Optional
from uuid import UUID
from datetime import datetime
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.models.learning_path import LearningPath
from app.models.learner import Learner
from app.models.resource import Resource
from app.schemas.learning_path import LearningPathResult
from app.schemas.learner import LearnerProfileResponse
from app.services.profile_service import profile_service
from app.schemas.resource import (
    CuratedPathResources,
    PhaseResources,
    ResourceCardData,
    ProviderStatusResponse
)
from app.agents.resource_curator_agent import ResourceCuratorAgent

logger = logging.getLogger(__name__)

class ResourceService:
    def __init__(self, agent: Optional[ResourceCuratorAgent] = None):
        self.agent = agent or ResourceCuratorAgent()

    def get_providers_status(self) -> ProviderStatusResponse:
        statuses = self.agent.get_providers_status()
        return ProviderStatusResponse(providers=statuses)

    async def curate_resources_for_path(
        self,
        db: Session,
        path_id: UUID,
        force_refresh: bool = False
    ) -> CuratedPathResources:
        path_str = str(path_id)

        # 1. Fetch LearningPath from DB
        db_path = db.query(LearningPath).filter(LearningPath.id == path_str).first()
        if not db_path:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Learning path with ID '{path_id}' not found."
            )

        # 2. Check cached resources if not force_refresh
        if not force_refresh:
            cached_resources = db.query(Resource).filter(Resource.path_id == path_str).all()
            if cached_resources:
                logger.info(f"Returning cached resources for learning path '{path_id}'.")
                return self._build_curated_path_from_db(path_id, cached_resources)

        # 3. Fetch Learner Profile
        db_learner = db.query(Learner).filter(Learner.user_id == db_path.user_id).first()
        if not db_learner:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Learner for path '{path_id}' not found."
            )

        # 4. Parse Pydantic schemas
        path_result = LearningPathResult.model_validate(db_path.path_json)
        learner_profile = profile_service.get_profile(db, user_id=db_path.user_id)

        # 5. Run ResourceCuratorAgent
        curated_result: CuratedPathResources = await self.agent.run(path_result, learner_profile)

        # 6. Save/Persist to Database
        db.query(Resource).filter(Resource.path_id == path_str).delete()

        for phase_res in curated_result.phases:
            for card in phase_res.resources:
                db_resource = Resource(
                    id=card.resource_id,
                    path_id=path_str,
                    phase_id=phase_res.phase_id,
                    platform=card.platform,
                    original_url=card.original_url,  # Save original URL
                    title=card.title,
                    resource_json=card.model_dump(mode="json"),
                    verification_status="verified" if card.is_active else "inactive",
                    last_verified_at=card.last_verified_at
                )
                db.add(db_resource)

        db.commit()
        return curated_result

    def get_path_resources(self, db: Session, path_id: UUID) -> CuratedPathResources:
        path_str = str(path_id)
        resources = db.query(Resource).filter(Resource.path_id == path_str).all()
        if not resources:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"No resources found for learning path ID '{path_id}'."
            )
        return self._build_curated_path_from_db(path_id, resources)

    def get_phase_resources(self, db: Session, phase_id: str) -> PhaseResources:
        resources = db.query(Resource).filter(Resource.phase_id == phase_id).all()
        if not resources:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"No resources found for phase ID '{phase_id}'."
            )
        cards = [ResourceCardData.model_validate(r.resource_json) for r in resources]
        return PhaseResources(phase_id=phase_id, resources=cards)

    async def refresh_resources(self, db: Session, path_id: UUID) -> CuratedPathResources:
        return await self.curate_resources_for_path(db, path_id=path_id, force_refresh=True)

    def _build_curated_path_from_db(self, path_id: UUID, db_resources: List[Resource]) -> CuratedPathResources:
        phase_map = {}
        for r in db_resources:
            phase_id = r.phase_id
            card = ResourceCardData.model_validate(r.resource_json)
            if phase_id not in phase_map:
                phase_map[phase_id] = []
            phase_map[phase_id].append(card)

        phases = [PhaseResources(phase_id=pid, resources=cards) for pid, cards in phase_map.items()]
        return CuratedPathResources(path_id=path_id, phases=phases)

resource_service = ResourceService()
