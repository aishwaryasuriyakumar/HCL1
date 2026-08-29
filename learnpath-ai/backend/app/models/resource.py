from sqlalchemy import Column, String, DateTime, JSON
from datetime import datetime
from uuid import uuid4
from app.database.base import Base

class Resource(Base):
    __tablename__ = "resources"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid4()))
    path_id = Column(String(36), nullable=False, index=True)
    phase_id = Column(String(50), nullable=False, index=True)
    platform = Column(String(50), nullable=False)
    original_url = Column(String(1024), nullable=False)
    title = Column(String(255), nullable=False)
    resource_json = Column(JSON, nullable=False)
    verification_status = Column(String(50), default="verified")
    last_verified_at = Column(DateTime, default=datetime.utcnow)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f"<Resource(id={self.id}, platform={self.platform}, title={self.title})>"
