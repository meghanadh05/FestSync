"""
Workspace business logic.
"""

from sqlalchemy.orm import Session
from uuid import UUID

from app.core.exceptions import NotFoundError
from app.core.permissions import require_workspace_role
from app.models.workspace import Workspace, WorkspaceMember, WorkspaceRole
from app.modules.workspaces.schema import WorkspaceCreate


class WorkspaceService:
    """Workspace operations."""

    @staticmethod
    def create_workspace(db: Session, user_id: str, data: WorkspaceCreate, email: str | None = None) -> Workspace:
        workspace = Workspace(
            name=data.name,
            organization=data.organization,
            country=data.country,
            currency=data.currency.upper(),
            timezone=data.timezone,
            created_by=user_id,
        )
        db.add(workspace)
        db.flush()

        db.add(
            WorkspaceMember(
                workspace_id=workspace.id,
                user_id=user_id,
                email=email,
                role=WorkspaceRole.OWNER,
            )
        )
        db.commit()
        db.refresh(workspace)
        return workspace

    @staticmethod
    def list_workspaces(db: Session, user_id: str) -> list[tuple[Workspace, WorkspaceRole]]:
        rows = db.query(Workspace, WorkspaceMember.role).join(
            WorkspaceMember,
            WorkspaceMember.workspace_id == Workspace.id,
        ).filter(
            WorkspaceMember.user_id == user_id,
            Workspace.deleted_at.is_(None),
        ).order_by(Workspace.created_at.desc()).all()

        return rows

    @staticmethod
    def get_workspace(db: Session, workspace_id: str, user_id: str) -> tuple[Workspace, WorkspaceRole]:
        member = require_workspace_role(db, workspace_id, user_id, WorkspaceRole.VIEWER)
        workspace_uuid = UUID(str(workspace_id))
        workspace = db.query(Workspace).filter(
            Workspace.id == workspace_uuid,
            Workspace.deleted_at.is_(None),
        ).first()

        if not workspace:
            raise NotFoundError("Workspace", workspace_id)

        return workspace, member.role

    @staticmethod
    def list_members(db: Session, workspace_id: str, user_id: str) -> list[WorkspaceMember]:
        require_workspace_role(db, workspace_id, user_id, WorkspaceRole.VIEWER)
        workspace_uuid = UUID(str(workspace_id))
        return db.query(WorkspaceMember).filter(
            WorkspaceMember.workspace_id == workspace_uuid,
        ).order_by(WorkspaceMember.created_at.asc()).all()
