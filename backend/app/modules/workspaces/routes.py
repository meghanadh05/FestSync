"""
Workspace API routes.
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.exceptions import AuthorizationError, NotFoundError
from app.core.security import get_current_user, get_current_user_id
from app.modules.workspaces.schema import (
    WorkspaceCreate,
    WorkspaceListResponse,
    WorkspaceMemberResponse,
    WorkspaceResponse,
)
from app.modules.workspaces.service import WorkspaceService

router = APIRouter(prefix="/workspaces", tags=["workspaces"])


def _workspace_response(workspace, role) -> WorkspaceResponse:
    return WorkspaceResponse(
        id=workspace.id,
        name=workspace.name,
        organization=workspace.organization,
        country=workspace.country,
        currency=workspace.currency,
        timezone=workspace.timezone,
        created_by=workspace.created_by,
        created_at=workspace.created_at,
        updated_at=workspace.updated_at,
        role=role,
    )


@router.post("", response_model=WorkspaceResponse, status_code=201)
def create_workspace(
    workspace_data: WorkspaceCreate,
    user=Depends(get_current_user),
    db: Session = Depends(get_db),
) -> WorkspaceResponse:
    workspace = WorkspaceService.create_workspace(
        db,
        user_id=user["sub"],
        data=workspace_data,
        email=user.get("email"),
    )
    return _workspace_response(workspace, "OWNER")


@router.get("", response_model=WorkspaceListResponse)
def list_workspaces(
    user_id: str = Depends(get_current_user_id),
    db: Session = Depends(get_db),
) -> WorkspaceListResponse:
    rows = WorkspaceService.list_workspaces(db, user_id)
    return WorkspaceListResponse(
        total=len(rows),
        items=[_workspace_response(workspace, role) for workspace, role in rows],
    )


@router.get("/{workspace_id}", response_model=WorkspaceResponse)
def get_workspace(
    workspace_id: str,
    user_id: str = Depends(get_current_user_id),
    db: Session = Depends(get_db),
) -> WorkspaceResponse:
    try:
        workspace, role = WorkspaceService.get_workspace(db, workspace_id, user_id)
        return _workspace_response(workspace, role)
    except (NotFoundError, AuthorizationError) as exc:
        raise HTTPException(status_code=exc.status_code, detail=str(exc))


@router.get("/{workspace_id}/members", response_model=list[WorkspaceMemberResponse])
def list_workspace_members(
    workspace_id: str,
    user_id: str = Depends(get_current_user_id),
    db: Session = Depends(get_db),
) -> list[WorkspaceMemberResponse]:
    try:
        members = WorkspaceService.list_members(db, workspace_id, user_id)
        return [WorkspaceMemberResponse.model_validate(member) for member in members]
    except (NotFoundError, AuthorizationError) as exc:
        raise HTTPException(status_code=exc.status_code, detail=str(exc))
