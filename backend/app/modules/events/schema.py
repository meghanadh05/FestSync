"""
Event Pydantic schemas for request/response validation.
"""

from datetime import date, datetime
from typing import Optional
from uuid import UUID
from pydantic import BaseModel, Field, field_validator
from enum import Enum

from app.models.event import EventType, EventStatus


class EventTypeEnum(str, Enum):
    """Event type options."""
    WEDDING = "WEDDING"
    BIRTHDAY = "BIRTHDAY"
    COLLEGE_FEST = "COLLEGE_FEST"
    CORPORATE_EVENT = "CORPORATE_EVENT"
    CONFERENCE = "CONFERENCE"
    RECEPTION = "RECEPTION"
    ENGAGEMENT = "ENGAGEMENT"
    CONCERT = "CONCERT"
    OTHER = "OTHER"


class EventStatusEnum(str, Enum):
    """Event status options."""
    PLANNING = "PLANNING"
    ACTIVE = "ACTIVE"
    COMPLETED = "COMPLETED"
    CANCELLED = "CANCELLED"


class EventBase(BaseModel):
    """Base schema with common event fields."""
    title: str = Field(..., min_length=1, max_length=255, description="Event title")
    description: Optional[str] = Field(None, max_length=2000, description="Event description")
    event_type: EventTypeEnum = Field(..., description="Type of event")
    start_date: date = Field(..., description="Event start date")
    end_date: date = Field(..., description="Event end date")
    location: Optional[str] = Field(None, max_length=255, description="Event location")
    estimated_guests: Optional[int] = Field(None, ge=0, description="Estimated number of guests")
    budget: Optional[float] = Field(None, ge=0, description="Event budget in selected currency")
    currency: str = Field("USD", max_length=10, description="Currency code")
    thumbnail_url: Optional[str] = Field(None, max_length=500, description="Event thumbnail URL")

    @field_validator("end_date")
    @classmethod
    def validate_end_date(cls, v, values):
        """Ensure end_date is not before start_date."""
        if "start_date" in values.data and v < values.data["start_date"]:
            raise ValueError("end_date must be after or equal to start_date")
        return v


class EventCreate(EventBase):
    """Schema for creating a new event."""
    pass


class EventUpdate(BaseModel):
    """Schema for updating an event."""
    title: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = Field(None, max_length=2000)
    event_type: Optional[EventTypeEnum] = None
    status: Optional[EventStatusEnum] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    location: Optional[str] = Field(None, max_length=255)
    estimated_guests: Optional[int] = Field(None, ge=0)
    budget: Optional[float] = Field(None, ge=0)
    currency: Optional[str] = Field(None, max_length=10)
    thumbnail_url: Optional[str] = Field(None, max_length=500)

    @field_validator("end_date")
    @classmethod
    def validate_end_date(cls, v, values):
        """Ensure end_date is not before start_date."""
        if v is None:
            return v
        start_date = values.data.get("start_date")
        if start_date and v < start_date:
            raise ValueError("end_date must be after or equal to start_date")
        return v


class EventResponse(EventBase):
    """Schema for event response."""
    id: UUID = Field(..., description="Event UUID")
    user_id: str = Field(..., description="User ID who created the event")
    status: EventStatusEnum = Field(EventStatusEnum.PLANNING, description="Current event status")
    created_at: datetime = Field(..., description="Creation timestamp")
    updated_at: datetime = Field(..., description="Last update timestamp")

    class Config:
        from_attributes = True


class EventListResponse(BaseModel):
    """Schema for list of events."""
    total: int = Field(..., description="Total number of events")
    skip: int = Field(..., description="Number of records skipped")
    limit: int = Field(..., description="Number of records returned")
    items: list[EventResponse] = Field(default_factory=list, description="List of events")


class EventDashboard(BaseModel):
    """Schema for event dashboard data."""
    event: EventResponse = Field(..., description="Event details")
    tasks_total: int = Field(default=0, ge=0, description="Total number of tasks")
    tasks_completed: int = Field(default=0, ge=0, description="Number of completed tasks")
    tasks_completion_percentage: int = Field(default=0, ge=0, le=100, description="Task completion percentage")
    budget_total: float = Field(default=0, ge=0, description="Total budget")
    budget_spent: float = Field(default=0, ge=0, description="Amount spent")
    budget_remaining: float = Field(default=0, ge=0, description="Remaining budget")
    budget_percentage_used: int = Field(default=0, ge=0, le=100, description="Budget usage percentage")
    vendors_saved: int = Field(default=0, ge=0, description="Number of saved vendors")
    guests_count: int = Field(default=0, ge=0, description="Number of guests")
    days_remaining: int = Field(description="Days until event start")
    progress_percentage: int = Field(ge=0, le=100, description="Overall event progress percentage")

    class Config:
        from_attributes = True


class EventSearch(BaseModel):
    """Schema for event search/filter parameters."""
    search: Optional[str] = Field(None, description="Search by title or description")
    event_type: Optional[EventTypeEnum] = Field(None, description="Filter by event type")
    status: Optional[EventStatusEnum] = Field(None, description="Filter by status")
    skip: int = Field(0, ge=0, description="Number of records to skip")
    limit: int = Field(10, ge=1, le=100, description="Number of records to return")
