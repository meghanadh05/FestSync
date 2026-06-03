"""
Task API routes.
"""

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import get_current_user_id
from app.core.exceptions import NotFoundError, AuthorizationError
from app.modules.tasks.schema import (
    TaskCreate,
    TaskUpdate,
    TaskStatusUpdate,
    TaskResponse,
    TaskListResponse,
    TaskKanbanBoard,
    SubtaskCreate,
    SubtaskUpdate,
    SubtaskResponse,
)
from app.modules.tasks.service import TaskService

router = APIRouter()


@router.post("/events/{event_id}/tasks", response_model=TaskResponse, status_code=201)
def create_task(
    event_id: str,
    task_data: TaskCreate,
    user_id: str = Depends(get_current_user_id),
    db: Session = Depends(get_db),
) -> TaskResponse:
    """
    Create a new task for an event.

    Parameters:
        - event_id: UUID of the event

    Returns:
        Created task details.
    """
    try:
        task = TaskService.create_task(db, event_id, user_id, task_data)
        return TaskResponse.model_validate(task)
    except (NotFoundError, AuthorizationError) as e:
        raise HTTPException(status_code=e.status_code, detail=str(e))


@router.get("/events/{event_id}/tasks")
def list_tasks(
    event_id: str,
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    status: str = Query(None),
    priority: str = Query(None),
    category: str = Query(None),
    search: str = Query(None),
    group_by_status: bool = Query(False),
    user_id: str = Depends(get_current_user_id),
    db: Session = Depends(get_db),
):
    """
    Get tasks for an event with optional filtering.

    Parameters:
        - event_id: UUID of the event
        - skip: Number of records to skip
        - limit: Number of records to return (max 100)
        - status: Filter by task status
        - priority: Filter by task priority
        - category: Filter by task category
        - search: Search in title/description
        - group_by_status: Return Kanban board format (True returns grouped by status)

    Returns:
        List of tasks or Kanban board grouped by status.
    """
    try:
        if group_by_status:
            grouped = TaskService.get_tasks_grouped_by_status(
                db, event_id, user_id, priority, category, search
            )
            return TaskKanbanBoard(**grouped)
        else:
            total, tasks = TaskService.get_tasks(
                db, event_id, user_id, skip, limit, status, priority, category, search
            )
            return TaskListResponse(
                total=total,
                skip=skip,
                limit=limit,
                items=[TaskResponse.model_validate(task) for task in tasks],
            )
    except (NotFoundError, AuthorizationError) as e:
        raise HTTPException(status_code=e.status_code, detail=str(e))


@router.get("/tasks/{task_id}", response_model=TaskResponse)
def get_task(
    task_id: str,
    user_id: str = Depends(get_current_user_id),
    db: Session = Depends(get_db),
) -> TaskResponse:
    """
    Get a specific task by ID.

    Parameters:
        - task_id: UUID of the task

    Returns:
        Task details.
    """
    try:
        task = TaskService.get_task_by_id(db, task_id, user_id)
        return TaskResponse.model_validate(task)
    except (NotFoundError, AuthorizationError) as e:
        raise HTTPException(status_code=e.status_code, detail=str(e))


@router.patch("/tasks/{task_id}", response_model=TaskResponse)
def update_task(
    task_id: str,
    task_data: TaskUpdate,
    user_id: str = Depends(get_current_user_id),
    db: Session = Depends(get_db),
) -> TaskResponse:
    """
    Update a task.

    Parameters:
        - task_id: UUID of the task

    Returns:
        Updated task details.
    """
    try:
        task = TaskService.update_task(db, task_id, user_id, task_data)
        return TaskResponse.model_validate(task)
    except (NotFoundError, AuthorizationError) as e:
        raise HTTPException(status_code=e.status_code, detail=str(e))


@router.delete("/tasks/{task_id}", status_code=204)
def delete_task(
    task_id: str,
    user_id: str = Depends(get_current_user_id),
    db: Session = Depends(get_db),
) -> None:
    """
    Delete (soft delete) a task.

    Parameters:
        - task_id: UUID of the task
    """
    try:
        TaskService.delete_task(db, task_id, user_id)
    except (NotFoundError, AuthorizationError) as e:
        raise HTTPException(status_code=e.status_code, detail=str(e))


@router.patch("/tasks/{task_id}/status", response_model=TaskResponse)
def update_task_status(
    task_id: str,
    status_data: TaskStatusUpdate,
    user_id: str = Depends(get_current_user_id),
    db: Session = Depends(get_db),
) -> TaskResponse:
    """
    Update task status (for Kanban board drag-and-drop).

    Parameters:
        - task_id: UUID of the task

    Returns:
        Updated task details.
    """
    try:
        task = TaskService.update_task_status(db, task_id, user_id, status_data)
        return TaskResponse.model_validate(task)
    except (NotFoundError, AuthorizationError) as e:
        raise HTTPException(status_code=e.status_code, detail=str(e))


@router.post("/tasks/{task_id}/subtasks", response_model=SubtaskResponse, status_code=201)
def create_subtask(
    task_id: str,
    subtask_data: SubtaskCreate,
    user_id: str = Depends(get_current_user_id),
    db: Session = Depends(get_db),
) -> SubtaskResponse:
    """
    Create a subtask for a task.

    Parameters:
        - task_id: UUID of the task

    Returns:
        Created subtask details.
    """
    try:
        subtask = TaskService.create_subtask(db, task_id, user_id, subtask_data)
        return SubtaskResponse.model_validate(subtask)
    except (NotFoundError, AuthorizationError) as e:
        raise HTTPException(status_code=e.status_code, detail=str(e))


@router.patch("/subtasks/{subtask_id}", response_model=SubtaskResponse)
def update_subtask(
    subtask_id: str,
    subtask_data: SubtaskUpdate,
    user_id: str = Depends(get_current_user_id),
    db: Session = Depends(get_db),
) -> SubtaskResponse:
    """
    Update a subtask.

    Parameters:
        - subtask_id: UUID of the subtask

    Returns:
        Updated subtask details.
    """
    try:
        subtask = TaskService.update_subtask(db, subtask_id, user_id, subtask_data)
        return SubtaskResponse.model_validate(subtask)
    except (NotFoundError, AuthorizationError) as e:
        raise HTTPException(status_code=e.status_code, detail=str(e))
