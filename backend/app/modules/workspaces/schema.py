"""
Workspace request and response schemas.
"""

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field

from app.models.workspace import WorkspaceRole


class WorkspaceCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    organization: str | None = Field(None, max_length=255)
    country: str = Field("India", min_length=2, max_length=100)
    currency: str = Field("INR", min_length=3, max_length=10)
    timezone: str = Field("Asia/Kolkata", min_length=1, max_length=100)


class WorkspaceResponse(BaseModel):
    id: UUID
    name: str
    organization: str | None
    country: str
    currency: str
    timezone: str
    created_by: str
    created_at: datetime
    updated_at: datetime
    role: WorkspaceRole

    class Config:
        from_attributes = True


class WorkspaceListResponse(BaseModel):
    total: int
    items: list[WorkspaceResponse] = Field(default_factory=list)


class WorkspaceMemberResponse(BaseModel):
    id: UUID
    workspace_id: UUID
    user_id: str
    email: str | None
    role: WorkspaceRole
    created_at: datetime

    class Config:
        from_attributes = True
