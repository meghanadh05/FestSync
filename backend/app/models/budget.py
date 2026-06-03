"""
Budget SQLAlchemy ORM model.
"""

from datetime import datetime
from sqlalchemy import Column, String, Text, DateTime, ForeignKey, Numeric
from sqlalchemy.dialects.postgresql import UUID
import uuid

from app.core.database import Base


class BudgetItem(Base):
    """Budget item model for tracking event expenses."""

    __tablename__ = "budget_items"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        index=True,
        nullable=False,
    )
    event_id = Column(UUID(as_uuid=True), ForeignKey("events.id"), nullable=False, index=True)
    category = Column(String(100), nullable=False, index=True)
    planned_amount = Column(Numeric(12, 2), nullable=False, default=0)
    actual_amount = Column(Numeric(12, 2), nullable=False, default=0)
    notes = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False, index=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    deleted_at = Column(DateTime, nullable=True)

    def __repr__(self) -> str:
        """String representation of BudgetItem."""
        return f"<BudgetItem(id={self.id}, category={self.category}, event_id={self.event_id})>"
