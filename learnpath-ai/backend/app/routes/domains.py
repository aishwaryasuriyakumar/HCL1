from fastapi import APIRouter, HTTPException
from app.data.domains import DOMAINS
from app.schemas.domain import DomainResponse, DomainListResponse

router = APIRouter()

@router.get("", response_model=DomainListResponse)
def get_domains():
    return {"domains": list(DOMAINS.values())}

@router.get("/{domain_id}", response_model=DomainResponse)
def get_domain(domain_id: str):
    if domain_id not in DOMAINS:
        raise HTTPException(status_code=404, detail="Domain not found")
    return DOMAINS[domain_id]
