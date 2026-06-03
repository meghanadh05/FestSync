"""
Budget service containing business logic.
"""

from datetime import datetime
from typing import Optional, List, Tuple, Dict
from uuid import UUID
from decimal import Decimal
from sqlalchemy.orm import Session
from sqlalchemy import and_

from app.models.budget import BudgetItem
from app.models.event import Event
from app.modules.budget.schema import (
    BudgetItemCreate,
    BudgetItemUpdate,
    BudgetHealthStatus,
    OverBudgetCategory,
)
from app.core.exceptions import NotFoundError, AuthorizationError


class BudgetService:
    """Service for budget-related operations."""

    @staticmethod
    def create_budget_item(
        db: Session,
        event_id: str,
        user_id: str,
        item_data: BudgetItemCreate,
    ) -> BudgetItem:
        """
        Create a new budget item for an event.

        Args:
            db: Database session
            event_id: Event ID (string or UUID)
            user_id: User ID (for ownership verification)
            item_data: Budget item creation data

        Returns:
            Created BudgetItem object

        Raises:
            NotFoundError: If event not found
            AuthorizationError: If user doesn't own the event
        """
        # Verify event ownership
        if isinstance(event_id, str):
            event_id = UUID(event_id)

        event = db.query(Event).filter(
            Event.id == event_id,
            Event.deleted_at.is_(None)
        ).first()

        if not event:
            raise NotFoundError("Event", str(event_id))

        if event.user_id != user_id:
            raise AuthorizationError("You don't have permission to manage budget for this event")

        db_item = BudgetItem(
            event_id=event_id,
            category=item_data.category,
            planned_amount=item_data.planned_amount,
            actual_amount=item_data.actual_amount,
            notes=item_data.notes,
        )
        db.add(db_item)
        db.commit()
        db.refresh(db_item)
        return db_item

    @staticmethod
    def get_budget_items(
        db: Session,
        event_id: str,
        user_id: str,
        skip: int = 0,
        limit: int = 10,
        category: Optional[str] = None,
    ) -> Tuple[int, List[BudgetItem]]:
        """
        Get budget items for an event.

        Args:
            db: Database session
            event_id: Event ID
            user_id: User ID (for ownership verification)
            skip: Number of records to skip
            limit: Number of records to return
            category: Filter by category

        Returns:
            Tuple of (total_count, items_list)

        Raises:
            NotFoundError: If event not found
            AuthorizationError: If user doesn't own the event
        """
        # Verify event ownership
        if isinstance(event_id, str):
            event_id = UUID(event_id)

        event = db.query(Event).filter(
            Event.id == event_id,
            Event.deleted_at.is_(None)
        ).first()

        if not event:
            raise NotFoundError("Event", str(event_id))

        if event.user_id != user_id:
            raise AuthorizationError("You don't have permission to view budget for this event")

        query = db.query(BudgetItem).filter(
            BudgetItem.event_id == event_id,
            BudgetItem.deleted_at.is_(None)
        )

        if category:
            query = query.filter(BudgetItem.category == category)

        total = query.count()
        items = query.order_by(BudgetItem.created_at.desc()).offset(skip).limit(limit).all()

        return total, items

    @staticmethod
    def get_budget_item_by_id(
        db: Session,
        item_id: str,
        user_id: str,
    ) -> BudgetItem:
        """
        Get a budget item by ID with ownership verification.

        Args:
            db: Database session
            item_id: Budget item ID
            user_id: User ID (for ownership verification)

        Returns:
            BudgetItem object

        Raises:
            NotFoundError: If item not found
            AuthorizationError: If user doesn't own the event
        """
        if isinstance(item_id, str):
            item_id = UUID(item_id)

        item = db.query(BudgetItem).filter(
            BudgetItem.id == item_id,
            BudgetItem.deleted_at.is_(None)
        ).first()

        if not item:
            raise NotFoundError("Budget item", str(item_id))

        # Verify event ownership
        event = db.query(Event).filter(Event.id == item.event_id).first()
        if event.user_id != user_id:
            raise AuthorizationError("You don't have permission to access this budget item")

        return item

    @staticmethod
    def update_budget_item(
        db: Session,
        item_id: str,
        user_id: str,
        item_data: BudgetItemUpdate,
    ) -> BudgetItem:
        """
        Update a budget item.

        Args:
            db: Database session
            item_id: Budget item ID
            user_id: User ID (for ownership verification)
            item_data: Budget item update data

        Returns:
            Updated BudgetItem object

        Raises:
            NotFoundError: If item not found
            AuthorizationError: If user doesn't own the event
        """
        item = BudgetService.get_budget_item_by_id(db, item_id, user_id)

        # Update only provided fields
        update_data = item_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(item, field, value)

        item.updated_at = datetime.utcnow()
        db.commit()
        db.refresh(item)
        return item

    @staticmethod
    def delete_budget_item(
        db: Session,
        item_id: str,
        user_id: str,
    ) -> None:
        """
        Soft delete a budget item.

        Args:
            db: Database session
            item_id: Budget item ID
            user_id: User ID (for ownership verification)

        Raises:
            NotFoundError: If item not found
            AuthorizationError: If user doesn't own the event
        """
        item = BudgetService.get_budget_item_by_id(db, item_id, user_id)
        item.deleted_at = datetime.utcnow()
        db.commit()

    @staticmethod
    def get_budget_summary(
        db: Session,
        event_id: str,
        user_id: str,
    ) -> Dict:
        """
        Get comprehensive budget summary for an event.

        Args:
            db: Database session
            event_id: Event ID
            user_id: User ID (for ownership verification)

        Returns:
            Dictionary with budget summary data

        Raises:
            NotFoundError: If event not found
            AuthorizationError: If user doesn't own the event
        """
        # Verify event ownership
        if isinstance(event_id, str):
            event_id = UUID(event_id)

        event = db.query(Event).filter(
            Event.id == event_id,
            Event.deleted_at.is_(None)
        ).first()

        if not event:
            raise NotFoundError("Event", str(event_id))

        if event.user_id != user_id:
            raise AuthorizationError("You don't have permission to view budget for this event")

        # Get all budget items for the event
        items = db.query(BudgetItem).filter(
            BudgetItem.event_id == event_id,
            BudgetItem.deleted_at.is_(None)
        ).all()

        # Calculate totals
        total_planned = float(sum(float(item.planned_amount) for item in items))
        total_actual = float(sum(float(item.actual_amount) for item in items))
        total_budget = float(event.budget or 0)
        remaining_budget = total_budget - total_actual

        # Calculate percentage
        if total_budget > 0:
            budget_percentage_used = int((total_actual / total_budget) * 100)
        else:
            budget_percentage_used = 0

        # Find over-budget categories
        over_budget_categories = []
        for item in items:
            actual = float(item.actual_amount)
            planned = float(item.planned_amount)
            if actual > planned:
                over_budget_categories.append(
                    OverBudgetCategory(
                        category=item.category,
                        planned_amount=planned,
                        actual_amount=actual,
                        overage=actual - planned,
                    )
                )

        # Determine budget health status
        if total_actual <= (total_budget * 0.8):
            health_status = BudgetHealthStatus.GOOD
        elif total_actual <= total_budget:
            health_status = BudgetHealthStatus.WARNING
        else:
            health_status = BudgetHealthStatus.OVER_BUDGET

        return {
            "total_budget": total_budget,
            "total_planned": total_planned,
            "total_actual": total_actual,
            "remaining_budget": remaining_budget,
            "budget_percentage_used": budget_percentage_used,
            "over_budget_categories": over_budget_categories,
            "budget_health_status": health_status,
            "currency": event.currency or "USD",
        }
