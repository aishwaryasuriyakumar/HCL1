from pydantic import BaseModel
from typing import List

class DomainResponse(BaseModel):
    id: str
    name: str
    description: str
    skills: List[str]

class DomainListResponse(BaseModel):
    domains: List[DomainResponse]
