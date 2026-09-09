"""
Event API routes.
"""

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import get_current_user_id
from app.core.exceptions import NotFoundError, AuthorizationError
from app.modules.events.schema import (
    EventCreate,
    EventUpdate,
    EventResponse,
    EventListResponse,
    EventDashboard,
)
from app.modules.events.service import EventService

router = APIRouter(prefix="/events", tags=["events"])


@router.post("", response_model=EventResponse, status_code=201)
def create_event(
    event_data: EventCreate,
    user_id: str = Depends(get_current_user_id),
    db: Session = Depends(get_db),
) -> EventResponse:
    """
    Create a new event.

    Returns:
        Created event details.
    """
    event = EventService.create_event(db, user_id, event_data)
    return EventResponse.model_validate(event)


@router.get("", response_model=EventListResponse)
def list_events(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    search: str = Query(None),
    event_type: str = Query(None),
    status: str = Query(None),
    user_id: str = Depends(get_current_user_id),
    db: Session = Depends(get_db),
) -> EventListResponse:
    """
    Get all events for the authenticated user with optional filtering.

    Query Parameters:
        - skip: Number of records to skip
        - limit: Number of records to return (max 100)
        - search: Search term for title/description
        - event_type: Filter by event type
        - status: Filter by event status

    Returns:
        List of events with pagination info.
    """
    total, events = EventService.get_user_events(
        db,
        user_id,
        skip=skip,
        limit=limit,
        search=search,
        event_type=event_type,
        status=status,
    )

    return EventListResponse(
        total=total,
        skip=skip,
        limit=limit,
        items=[EventResponse.model_validate(event) for event in events],
    )


@router.get("/{event_id}", response_model=EventResponse)
def get_event(
    event_id: str,
    user_id: str = Depends(get_current_user_id),
    db: Session = Depends(get_db),
) -> EventResponse:
    """
    Get a specific event by ID.

    Parameters:
        - event_id: UUID of the event

    Returns:
        Event details.

    Raises:
        NotFoundError: If event not found
        AuthorizationError: If user doesn't own the event
    """
    try:
        event = EventService.get_event_by_id(db, event_id, user_id)
        return EventResponse.model_validate(event)
    except (NotFoundError, AuthorizationError) as e:
        raise HTTPException(status_code=e.status_code, detail=str(e))


@router.patch("/{event_id}", response_model=EventResponse)
def update_event(
    event_id: str,
    event_data: EventUpdate,
    user_id: str = Depends(get_current_user_id),
    db: Session = Depends(get_db),
) -> EventResponse:
    """
    Update an event.

    Parameters:
        - event_id: UUID of the event

    Returns:
        Updated event details.

    Raises:
        NotFoundError: If event not found
        AuthorizationError: If user doesn't own the event
    """
    try:
        event = EventService.update_event(db, event_id, user_id, event_data)
        return EventResponse.model_validate(event)
    except (NotFoundError, AuthorizationError) as e:
        raise HTTPException(status_code=e.status_code, detail=str(e))


@router.delete("/{event_id}", status_code=204)
def delete_event(
    event_id: str,
    user_id: str = Depends(get_current_user_id),
    db: Session = Depends(get_db),
) -> None:
    """
    Delete (soft delete) an event.

    Parameters:
        - event_id: UUID of the event

    Raises:
        NotFoundError: If event not found
        AuthorizationError: If user doesn't own the event
    """
    try:
        EventService.delete_event(db, event_id, user_id)
    except (NotFoundError, AuthorizationError) as e:
        raise HTTPException(status_code=e.status_code, detail=str(e))


@router.get("/{event_id}/dashboard", response_model=EventDashboard)
def get_event_dashboard(
    event_id: str,
    user_id: str = Depends(get_current_user_id),
    db: Session = Depends(get_db),
) -> EventDashboard:
    """
    Get comprehensive event dashboard data.

    Includes event details, task completion stats, budget summary,
    vendor count, guest count, days remaining, and progress percentage.

    Parameters:
        - event_id: UUID of the event

    Returns:
        Event dashboard with all summary statistics.

    Raises:
        NotFoundError: If event not found
        AuthorizationError: If user doesn't own the event
    """
    try:
        dashboard_data = EventService.get_event_dashboard(db, event_id, user_id)
        return EventDashboard(**dashboard_data)
    except (NotFoundError, AuthorizationError) as e:
        raise HTTPException(status_code=e.status_code, detail=str(e))
