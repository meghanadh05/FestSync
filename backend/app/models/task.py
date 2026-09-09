"""
Task and Subtask SQLAlchemy ORM models.
"""

from datetime import datetime
from sqlalchemy import Column, String, Text, Date, DateTime, Enum, ForeignKey, Boolean, Integer
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import enum
import uuid

from app.core.database import Base


class TaskStatus(str, enum.Enum):
    """Task status enumeration."""
    PENDING = "PENDING"
    IN_PROGRESS = "IN_PROGRESS"
    COMPLETED = "COMPLETED"


class TaskPriority(str, enum.Enum):
    """Task priority enumeration."""
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    URGENT = "URGENT"


class Task(Base):
    """Task model for storing event tasks."""

    __tablename__ = "tasks"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        index=True,
        nullable=False,
    )
    event_id = Column(UUID(as_uuid=True), ForeignKey("events.id"), nullable=False, index=True)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    status = Column(Enum(TaskStatus), nullable=False, default=TaskStatus.PENDING, index=True)
    priority = Column(Enum(TaskPriority), nullable=False, default=TaskPriority.MEDIUM, index=True)
    category = Column(String(100), nullable=True, index=True)
    due_date = Column(Date, nullable=True, index=True)
    assigned_to = Column(String, nullable=True)  # User ID
    ai_generated = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False, index=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    deleted_at = Column(DateTime, nullable=True)

    # Relationships
    subtasks = relationship("Subtask", back_populates="task", cascade="all, delete-orphan")

    def __repr__(self) -> str:
        """String representation of Task."""
        return f"<Task(id={self.id}, title={self.title}, event_id={self.event_id})>"


class Subtask(Base):
    """Subtask model for storing task subtasks."""

    __tablename__ = "subtasks"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        index=True,
        nullable=False,
    )
    task_id = Column(UUID(as_uuid=True), ForeignKey("tasks.id"), nullable=False, index=True)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    status = Column(Enum(TaskStatus), nullable=False, default=TaskStatus.PENDING, index=True)
    order = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False, index=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # Relationships
    task = relationship("Task", back_populates="subtasks")

    def __repr__(self) -> str:
        """String representation of Subtask."""
        return f"<Subtask(id={self.id}, title={self.title}, task_id={self.task_id})>"
