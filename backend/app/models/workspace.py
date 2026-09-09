"""
Workspace and membership models.
"""

import enum
import uuid
from datetime import datetime

from sqlalchemy import Column, DateTime, Enum, String, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID

from app.core.database import Base


class WorkspaceRole(str, enum.Enum):
    """Workspace membership roles."""

    OWNER = "OWNER"
    ADMIN = "ADMIN"
    PLANNER = "PLANNER"
    MEMBER = "MEMBER"
    VIEWER = "VIEWER"


class Workspace(Base):
    """Collaborative container for events and related planning records."""

    __tablename__ = "workspaces"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True, nullable=False)
    name = Column(String(255), nullable=False)
    organization = Column(String(255), nullable=True)
    country = Column(String(100), nullable=False, default="India")
    currency = Column(String(10), nullable=False, default="INR")
    timezone = Column(String(100), nullable=False, default="Asia/Kolkata")
    created_by = Column(String, nullable=False, index=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False, index=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    deleted_at = Column(DateTime, nullable=True)


class WorkspaceMember(Base):
    """User membership inside a workspace."""

    __tablename__ = "workspace_members"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True, nullable=False)
    workspace_id = Column(UUID(as_uuid=True), nullable=False, index=True)
    user_id = Column(String, nullable=False, index=True)
    email = Column(String(255), nullable=True)
    role = Column(Enum(WorkspaceRole), nullable=False, default=WorkspaceRole.MEMBER)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    __table_args__ = (
        UniqueConstraint("workspace_id", "user_id", name="uq_workspace_member_user"),
    )
