"""
Event SQLAlchemy ORM model.
"""

from datetime import datetime
from sqlalchemy import Column, String, Text, Date, Numeric, Integer, DateTime, Enum
from sqlalchemy.dialects.postgresql import UUID
import enum
import uuid

from app.core.database import Base


class EventType(str, enum.Enum):
    """Event type enumeration."""
    WEDDING = "WEDDING"
    BIRTHDAY = "BIRTHDAY"
    COLLEGE_FEST = "COLLEGE_FEST"
    CORPORATE_EVENT = "CORPORATE_EVENT"
    CONFERENCE = "CONFERENCE"
    RECEPTION = "RECEPTION"
    ENGAGEMENT = "ENGAGEMENT"
    CONCERT = "CONCERT"
    OTHER = "OTHER"


class EventStatus(str, enum.Enum):
    """Event status enumeration."""
    PLANNING = "PLANNING"
    ACTIVE = "ACTIVE"
    COMPLETED = "COMPLETED"
    CANCELLED = "CANCELLED"


class Event(Base):
    """Event model for storing event information."""

    __tablename__ = "events"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        index=True,
        nullable=False,
    )
    user_id = Column(String, nullable=False, index=True)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    event_type = Column(Enum(EventType), nullable=False, index=True)
    status = Column(Enum(EventStatus), nullable=False, default=EventStatus.PLANNING, index=True)
    start_date = Column(Date, nullable=False, index=True)
    end_date = Column(Date, nullable=False)
    location = Column(String(255), nullable=True)
    estimated_guests = Column(Integer, nullable=True)
    budget = Column(Numeric(12, 2), nullable=True)
    currency = Column(String(10), default="USD")
    thumbnail_url = Column(String(500), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False, index=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    deleted_at = Column(DateTime, nullable=True)

    def __repr__(self) -> str:
        """String representation of Event."""
        return f"<Event(id={self.id}, title={self.title}, user_id={self.user_id})>"
