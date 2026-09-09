"""
Permission helpers for workspace-scoped resources.
"""

from sqlalchemy.orm import Session
from uuid import UUID

from app.core.exceptions import AuthorizationError, NotFoundError
from app.models.workspace import WorkspaceMember, WorkspaceRole


ROLE_ORDER = {
    WorkspaceRole.VIEWER: 0,
    WorkspaceRole.MEMBER: 1,
    WorkspaceRole.PLANNER: 2,
    WorkspaceRole.ADMIN: 3,
    WorkspaceRole.OWNER: 4,
}


def require_workspace_role(
    db: Session,
    workspace_id: str,
    user_id: str,
    minimum_role: WorkspaceRole = WorkspaceRole.VIEWER,
) -> WorkspaceMember:
    """Return membership if the user has at least the requested workspace role."""
    try:
        workspace_uuid = UUID(str(workspace_id))
    except ValueError:
        raise NotFoundError("Workspace", workspace_id)

    member = db.query(WorkspaceMember).filter(
        WorkspaceMember.workspace_id == workspace_uuid,
        WorkspaceMember.user_id == user_id,
    ).first()

    if not member or ROLE_ORDER[member.role] < ROLE_ORDER[minimum_role]:
        raise AuthorizationError("You do not have access to this workspace")

    return member
