"""
AI Generation SQLAlchemy ORM model.
"""

from datetime import datetime
from sqlalchemy import Column, String, Text, DateTime, Enum
from sqlalchemy.dialects.postgresql import UUID
import enum
import uuid

from app.core.database import Base


class AgentType(str, enum.Enum):
    """Supported AI agent types."""
    EVENT_PLANNER = "EVENT_PLANNER"
    TASK_GENERATOR = "TASK_GENERATOR"
    BUDGET_ADVISOR = "BUDGET_ADVISOR"
    VENDOR_RECOMMENDATION = "VENDOR_RECOMMENDATION"
    CHAT_ASSISTANT = "CHAT_ASSISTANT"


class GenerationStatus(str, enum.Enum):
    """Status of an AI generation request."""
    SUCCESS = "SUCCESS"
    FAILED = "FAILED"
    INVALID_JSON = "INVALID_JSON"


class AIGeneration(Base):
    """Stores every AI generation request and its result."""

    __tablename__ = "ai_generations"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        index=True,
        nullable=False,
    )
    user_id = Column(String, nullable=False, index=True)
    event_id = Column(String, nullable=True, index=True)   # nullable for chat
    agent_type = Column(Enum(AgentType), nullable=False, index=True)
    prompt = Column(Text, nullable=False)
    response_json = Column(Text, nullable=True)            # null if FAILED/INVALID_JSON
    status = Column(Enum(GenerationStatus), nullable=False, default=GenerationStatus.SUCCESS)
    error_message = Column(Text, nullable=True)
    model_used = Column(String(100), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False, index=True)

    def __repr__(self) -> str:
        return f"<AIGeneration(id={self.id}, agent={self.agent_type}, status={self.status})>"
