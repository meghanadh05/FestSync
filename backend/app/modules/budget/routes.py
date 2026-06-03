"""
Budget API routes.
"""

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import get_current_user_id
from app.core.exceptions import NotFoundError, AuthorizationError
from app.modules.budget.schema import (
    BudgetItemCreate,
    BudgetItemUpdate,
    BudgetItemResponse,
    BudgetListResponse,
    BudgetSummary,
)
from app.modules.budget.service import BudgetService

router = APIRouter()


@router.post("/events/{event_id}/budget", response_model=BudgetItemResponse, status_code=201)
def create_budget_item(
    event_id: str,
    item_data: BudgetItemCreate,
    user_id: str = Depends(get_current_user_id),
    db: Session = Depends(get_db),
) -> BudgetItemResponse:
    """
    Create a new budget item for an event.

    Parameters:
        - event_id: UUID of the event

    Returns:
        Created budget item details.
    """
    try:
        item = BudgetService.create_budget_item(db, event_id, user_id, item_data)
        return BudgetItemResponse.model_validate(item)
    except (NotFoundError, AuthorizationError) as e:
        raise HTTPException(status_code=e.status_code, detail=str(e))


@router.get("/events/{event_id}/budget", response_model=BudgetListResponse)
def list_budget_items(
    event_id: str,
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    category: str = Query(None),
    user_id: str = Depends(get_current_user_id),
    db: Session = Depends(get_db),
) -> BudgetListResponse:
    """
    Get budget items for an event with optional filtering.

    Parameters:
        - event_id: UUID of the event
        - skip: Number of records to skip
        - limit: Number of records to return (max 100)
        - category: Filter by category

    Returns:
        List of budget items.
    """
    try:
        total, items = BudgetService.get_budget_items(
            db, event_id, user_id, skip, limit, category
        )
        return BudgetListResponse(
            total=total,
            skip=skip,
            limit=limit,
            items=[BudgetItemResponse.model_validate(item) for item in items],
        )
    except (NotFoundError, AuthorizationError) as e:
        raise HTTPException(status_code=e.status_code, detail=str(e))


@router.patch("/budget/{budget_item_id}", response_model=BudgetItemResponse)
def update_budget_item(
    budget_item_id: str,
    item_data: BudgetItemUpdate,
    user_id: str = Depends(get_current_user_id),
    db: Session = Depends(get_db),
) -> BudgetItemResponse:
    """
    Update a budget item.

    Parameters:
        - budget_item_id: UUID of the budget item

    Returns:
        Updated budget item details.
    """
    try:
        item = BudgetService.update_budget_item(db, budget_item_id, user_id, item_data)
        return BudgetItemResponse.model_validate(item)
    except (NotFoundError, AuthorizationError) as e:
        raise HTTPException(status_code=e.status_code, detail=str(e))


@router.delete("/budget/{budget_item_id}", status_code=204)
def delete_budget_item(
    budget_item_id: str,
    user_id: str = Depends(get_current_user_id),
    db: Session = Depends(get_db),
) -> None:
    """
    Delete (soft delete) a budget item.

    Parameters:
        - budget_item_id: UUID of the budget item
    """
    try:
        BudgetService.delete_budget_item(db, budget_item_id, user_id)
    except (NotFoundError, AuthorizationError) as e:
        raise HTTPException(status_code=e.status_code, detail=str(e))


@router.get("/events/{event_id}/budget/summary", response_model=BudgetSummary)
def get_budget_summary(
    event_id: str,
    user_id: str = Depends(get_current_user_id),
    db: Session = Depends(get_db),
) -> BudgetSummary:
    """
    Get comprehensive budget summary for an event.

    Includes total budget, planned amounts, actual spending, remaining budget,
    over-budget categories, and overall budget health status.

    Parameters:
        - event_id: UUID of the event

    Returns:
        Budget summary with all calculations.
    """
    try:
        summary_data = BudgetService.get_budget_summary(db, event_id, user_id)
        return BudgetSummary(**summary_data)
    except (NotFoundError, AuthorizationError) as e:
        raise HTTPException(status_code=e.status_code, detail=str(e))
