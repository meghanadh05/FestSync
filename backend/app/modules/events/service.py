"""
Event service containing business logic.
"""

from datetime import datetime, date
from typing import Optional
from uuid import UUID
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_

from app.models.event import Event, EventStatus
from app.modules.events.schema import EventCreate, EventUpdate
from app.core.exceptions import NotFoundError, AuthorizationError


class EventService:
    """Service for event-related operations."""

    @staticmethod
    def create_event(db: Session, user_id: str, event_data: EventCreate) -> Event:
        """
        Create a new event.

        Args:
            db: Database session
            user_id: ID of the user creating the event
            event_data: Event creation data

        Returns:
            Created Event object
        """
        db_event = Event(
            user_id=user_id,
            title=event_data.title,
            description=event_data.description,
            event_type=event_data.event_type,
            status=EventStatus.PLANNING,
            start_date=event_data.start_date,
            end_date=event_data.end_date,
            location=event_data.location,
            estimated_guests=event_data.estimated_guests,
            budget=event_data.budget,
            currency=event_data.currency,
            thumbnail_url=event_data.thumbnail_url,
        )
        db.add(db_event)
        db.commit()
        db.refresh(db_event)
        return db_event

    @staticmethod
    def get_event_by_id(db: Session, event_id: str, user_id: str) -> Event:
        """
        Get an event by ID, ensuring user owns it.

        Args:
            db: Database session
            event_id: Event ID (string or UUID)
            user_id: User ID (for ownership verification)

        Returns:
            Event object

        Raises:
            NotFoundError: If event not found
            AuthorizationError: If user doesn't own the event
        """
        # Convert string to UUID if needed
        if isinstance(event_id, str):
            try:
                event_id = UUID(event_id)
            except ValueError:
                raise NotFoundError("Event", str(event_id))

        db_event = db.query(Event).filter(
            Event.id == event_id,
            Event.deleted_at.is_(None)
        ).first()

        if not db_event:
            raise NotFoundError("Event", event_id)

        if db_event.user_id != user_id:
            raise AuthorizationError("You don't have permission to access this event")

        return db_event

    @staticmethod
    def get_user_events(
        db: Session,
        user_id: str,
        skip: int = 0,
        limit: int = 10,
        search: Optional[str] = None,
        event_type: Optional[str] = None,
        status: Optional[str] = None,
    ) -> tuple[int, list[Event]]:
        """
        Get all events for a user with optional filtering.

        Args:
            db: Database session
            user_id: User ID
            skip: Number of records to skip
            limit: Number of records to return
            search: Search term for title/description
            event_type: Filter by event type
            status: Filter by event status

        Returns:
            Tuple of (total_count, events_list)
        """
        query = db.query(Event).filter(
            Event.user_id == user_id,
            Event.deleted_at.is_(None)
        )

        # Apply search filter
        if search:
            search_term = f"%{search}%"
            query = query.filter(
                or_(
                    Event.title.ilike(search_term),
                    Event.description.ilike(search_term)
                )
            )

        # Apply event type filter
        if event_type:
            query = query.filter(Event.event_type == event_type)

        # Apply status filter
        if status:
            query = query.filter(Event.status == status)

        total = query.count()
        events = query.order_by(Event.created_at.desc()).offset(skip).limit(limit).all()

        return total, events

    @staticmethod
    def update_event(db: Session, event_id: str, user_id: str, event_data: EventUpdate) -> Event:
        """
        Update an event, ensuring user owns it.

        Args:
            db: Database session
            event_id: Event ID
            user_id: User ID (for ownership verification)
            event_data: Event update data

        Returns:
            Updated Event object

        Raises:
            NotFoundError: If event not found
            AuthorizationError: If user doesn't own the event
        """
        db_event = EventService.get_event_by_id(db, event_id, user_id)

        # Update only provided fields
        update_data = event_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_event, field, value)

        db_event.updated_at = datetime.utcnow()
        db.commit()
        db.refresh(db_event)
        return db_event

    @staticmethod
    def delete_event(db: Session, event_id: str, user_id: str) -> None:
        """
        Soft delete an event, ensuring user owns it.

        Args:
            db: Database session
            event_id: Event ID
            user_id: User ID (for ownership verification)

        Raises:
            NotFoundError: If event not found
            AuthorizationError: If user doesn't own the event
        """
        db_event = EventService.get_event_by_id(db, event_id, user_id)

        db_event.deleted_at = datetime.utcnow()
        db.commit()

    @staticmethod
    def get_event_dashboard(
        db: Session,
        event_id: str,
        user_id: str,
        task_stats: Optional[dict] = None,
        budget_stats: Optional[dict] = None,
        vendor_count: int = 0,
        guest_count: int = 0,
    ) -> dict:
        """
        Get comprehensive event dashboard data.

        Args:
            db: Database session
            event_id: Event ID
            user_id: User ID (for ownership verification)
            task_stats: Task statistics {total, completed}
            budget_stats: Budget statistics {total, spent}
            vendor_count: Number of saved vendors
            guest_count: Number of guests

        Returns:
            Dictionary with event dashboard data
        """
        event = EventService.get_event_by_id(db, event_id, user_id)

        # Default stats
        if task_stats is None:
            task_stats = {"total": 0, "completed": 0}
        if budget_stats is None:
            budget_stats = {"total": float(event.budget or 0), "spent": 0}

        # Calculate completion percentages
        tasks_completion_percentage = 0
        if task_stats["total"] > 0:
            tasks_completion_percentage = int(
                (task_stats["completed"] / task_stats["total"]) * 100
            )

        budget_percentage_used = 0
        if budget_stats["total"] > 0:
            budget_percentage_used = int(
                (budget_stats["spent"] / budget_stats["total"]) * 100
            )

        # Calculate days remaining
        days_remaining = (event.start_date - date.today()).days

        # Calculate overall progress (simple average of completion percentages)
        progress_percentage = int(
            (tasks_completion_percentage + budget_percentage_used) / 2
        )

        return {
            "event": event,
            "tasks_total": task_stats["total"],
            "tasks_completed": task_stats["completed"],
            "tasks_completion_percentage": tasks_completion_percentage,
            "budget_total": budget_stats["total"],
            "budget_spent": budget_stats["spent"],
            "budget_remaining": max(0, budget_stats["total"] - budget_stats["spent"]),
            "budget_percentage_used": budget_percentage_used,
            "vendors_saved": vendor_count,
            "guests_count": guest_count,
            "days_remaining": days_remaining,
            "progress_percentage": progress_percentage,
        }
