"""
Budget Pydantic schemas for request/response validation.
"""

from datetime import datetime
from typing import Optional, List
from uuid import UUID
from pydantic import BaseModel, Field
from enum import Enum


class BudgetHealthStatus(str, Enum):
    """Budget health status enumeration."""
    GOOD = "GOOD"
    WARNING = "WARNING"
    OVER_BUDGET = "OVER_BUDGET"


class BudgetItemBase(BaseModel):
    """Base schema for budget items."""
    category: str = Field(..., min_length=1, max_length=100, description="Budget category")
    planned_amount: float = Field(..., ge=0, description="Planned amount in event currency")
    actual_amount: float = Field(0, ge=0, description="Actual amount spent")
    notes: Optional[str] = Field(None, max_length=2000, description="Notes about this expense")


class BudgetItemCreate(BudgetItemBase):
    """Schema for creating a budget item."""
    pass


class BudgetItemUpdate(BaseModel):
    """Schema for updating a budget item."""
    category: Optional[str] = Field(None, min_length=1, max_length=100)
    planned_amount: Optional[float] = Field(None, ge=0)
    actual_amount: Optional[float] = Field(None, ge=0)
    notes: Optional[str] = Field(None, max_length=2000)


class BudgetItemResponse(BudgetItemBase):
    """Schema for budget item response."""
    id: UUID = Field(..., description="Budget item UUID")
    event_id: UUID = Field(..., description="Event UUID")
    created_at: datetime = Field(..., description="Creation timestamp")
    updated_at: datetime = Field(..., description="Last update timestamp")

    class Config:
        from_attributes = True


class BudgetListResponse(BaseModel):
    """Schema for list of budget items."""
    total: int = Field(..., description="Total number of items")
    skip: int = Field(..., description="Number of records skipped")
    limit: int = Field(..., description="Number of records returned")
    items: List[BudgetItemResponse] = Field(default_factory=list, description="List of budget items")


class OverBudgetCategory(BaseModel):
    """Schema for over-budget category info."""
    category: str = Field(..., description="Category name")
    planned_amount: float = Field(..., ge=0, description="Planned amount")
    actual_amount: float = Field(..., ge=0, description="Actual amount")
    overage: float = Field(..., description="Amount over budget (actual - planned)")


class BudgetSummary(BaseModel):
    """Schema for budget summary."""
    total_budget: float = Field(..., ge=0, description="Total event budget")
    total_planned: float = Field(..., ge=0, description="Total planned amounts across all items")
    total_actual: float = Field(..., ge=0, description="Total actual amounts spent")
    remaining_budget: float = Field(..., description="Remaining budget (total_budget - total_actual)")
    budget_percentage_used: int = Field(ge=0, description="Percentage of budget used (can exceed 100 if over-budget)")
    over_budget_categories: List[OverBudgetCategory] = Field(
        default_factory=list,
        description="Categories where actual > planned"
    )
    budget_health_status: BudgetHealthStatus = Field(..., description="Overall budget health status")
    currency: str = Field("USD", description="Currency code")

    class Config:
        from_attributes = True


class BudgetFilter(BaseModel):
    """Schema for budget filtering parameters."""
    category: Optional[str] = Field(None, description="Filter by category")
    skip: int = Field(0, ge=0, description="Number of records to skip")
    limit: int = Field(10, ge=1, le=100, description="Number of records to return")
