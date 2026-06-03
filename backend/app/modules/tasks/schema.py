"""
Task and Subtask Pydantic schemas for request/response validation.
"""

from datetime import date, datetime
from typing import Optional, List
from uuid import UUID
from pydantic import BaseModel, Field
from enum import Enum

from app.models.task import TaskStatus, TaskPriority


class TaskStatusEnum(str, Enum):
    """Task status options."""
    PENDING = "PENDING"
    IN_PROGRESS = "IN_PROGRESS"
    COMPLETED = "COMPLETED"


class TaskPriorityEnum(str, Enum):
    """Task priority options."""
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    URGENT = "URGENT"


class SubtaskBase(BaseModel):
    """Base schema for subtasks."""
    title: str = Field(..., min_length=1, max_length=255, description="Subtask title")
    description: Optional[str] = Field(None, max_length=2000, description="Subtask description")
    status: Optional[TaskStatusEnum] = Field(TaskStatusEnum.PENDING, description="Subtask status")


class SubtaskCreate(SubtaskBase):
    """Schema for creating a subtask."""
    pass


class SubtaskUpdate(BaseModel):
    """Schema for updating a subtask."""
    title: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = Field(None, max_length=2000)
    status: Optional[TaskStatusEnum] = None


class SubtaskResponse(SubtaskBase):
    """Schema for subtask response."""
    id: UUID = Field(..., description="Subtask UUID")
    task_id: UUID = Field(..., description="Parent task UUID")
    order: int = Field(0, ge=0, description="Display order")
    created_at: datetime = Field(..., description="Creation timestamp")
    updated_at: datetime = Field(..., description="Last update timestamp")

    class Config:
        from_attributes = True


class TaskBase(BaseModel):
    """Base schema with common task fields."""
    title: str = Field(..., min_length=1, max_length=255, description="Task title")
    description: Optional[str] = Field(None, max_length=2000, description="Task description")
    priority: TaskPriorityEnum = Field(TaskPriorityEnum.MEDIUM, description="Task priority")
    category: Optional[str] = Field(None, max_length=100, description="Task category")
    due_date: Optional[date] = Field(None, description="Task due date")
    assigned_to: Optional[str] = Field(None, max_length=255, description="User ID assigned to task")


class TaskCreate(TaskBase):
    """Schema for creating a task."""
    pass


class TaskUpdate(BaseModel):
    """Schema for updating a task."""
    title: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = Field(None, max_length=2000)
    status: Optional[TaskStatusEnum] = None
    priority: Optional[TaskPriorityEnum] = None
    category: Optional[str] = Field(None, max_length=100)
    due_date: Optional[date] = None
    assigned_to: Optional[str] = Field(None, max_length=255)


class TaskStatusUpdate(BaseModel):
    """Schema for updating only task status."""
    status: TaskStatusEnum = Field(..., description="New task status")


class TaskResponse(TaskBase):
    """Schema for task response."""
    id: UUID = Field(..., description="Task UUID")
    event_id: UUID = Field(..., description="Event UUID")
    status: TaskStatusEnum = Field(TaskStatusEnum.PENDING, description="Current task status")
    ai_generated: bool = Field(False, description="Whether task was AI-generated")
    created_at: datetime = Field(..., description="Creation timestamp")
    updated_at: datetime = Field(..., description="Last update timestamp")
    subtasks: List[SubtaskResponse] = Field(default_factory=list, description="Subtasks")

    class Config:
        from_attributes = True


class TaskListResponse(BaseModel):
    """Schema for list of tasks."""
    total: int = Field(..., description="Total number of tasks")
    skip: int = Field(..., description="Number of records skipped")
    limit: int = Field(..., description="Number of records returned")
    items: List[TaskResponse] = Field(default_factory=list, description="List of tasks")


class TaskKanbanBoard(BaseModel):
    """Schema for Kanban board grouped by status."""
    pending: List[TaskResponse] = Field(default_factory=list, description="Pending tasks")
    in_progress: List[TaskResponse] = Field(default_factory=list, description="In progress tasks")
    completed: List[TaskResponse] = Field(default_factory=list, description="Completed tasks")

    class Config:
        from_attributes = True


class TaskFilter(BaseModel):
    """Schema for task filtering parameters."""
    status: Optional[TaskStatusEnum] = Field(None, description="Filter by status")
    priority: Optional[TaskPriorityEnum] = Field(None, description="Filter by priority")
    category: Optional[str] = Field(None, description="Filter by category")
    search: Optional[str] = Field(None, description="Search in title/description")
    skip: int = Field(0, ge=0, description="Number of records to skip")
    limit: int = Field(10, ge=1, le=100, description="Number of records to return")
    group_by_status: bool = Field(False, description="Return Kanban board format")
