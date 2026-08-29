from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session
from uuid import UUID
from app.database.session import get_db
from app.schemas.resource import (
    CuratedPathResources,
    PhaseResources,
    ProviderStatusResponse
)
from app.services.resource_service import resource_service

router = APIRouter()

@router.post("/curate/{path_id}", response_model=CuratedPathResources, status_code=status.HTTP_200_OK)
async def curate_resources_for_path(
    path_id: UUID,
    force_refresh: bool = Query(False, description="Set to true to force re-curation & re-verification of resources"),
    db: Session = Depends(get_db)
):
    """
    Discovers, validates, ranks, and recommends learning resources for all phases of a learning path.
    """
    return await resource_service.curate_resources_for_path(db, path_id=path_id, force_refresh=force_refresh)

@router.get("/path/{path_id}", response_model=CuratedPathResources, status_code=status.HTTP_200_OK)
def get_path_resources(
    path_id: UUID,
    db: Session = Depends(get_db)
):
    """
    Retrieves the curated learning resources for a specific learning path.
    """
    return resource_service.get_path_resources(db, path_id=path_id)

@router.get("/phase/{phase_id}", response_model=PhaseResources, status_code=status.HTTP_200_OK)
def get_phase_resources(
    phase_id: str,
    db: Session = Depends(get_db)
):
    """
    Retrieves recommended learning resources for a specific phase ID.
    """
    return resource_service.get_phase_resources(db, phase_id=phase_id)

@router.post("/refresh/{path_id}", response_model=CuratedPathResources, status_code=status.HTTP_200_OK)
async def refresh_resources(
    path_id: UUID,
    db: Session = Depends(get_db)
):
    """
    Revalidates stale resources and discovers new resource candidates for a learning path.
    """
    return await resource_service.refresh_resources(db, path_id=path_id)

@router.get("/providers/status", response_model=ProviderStatusResponse, status_code=status.HTTP_200_OK)
def get_providers_status():
    """
    Returns health and availability status for all configured public resource providers.
    """
    return resource_service.get_providers_status()
