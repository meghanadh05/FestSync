"""
AI module Pydantic schemas — request bodies, validated AI outputs, API responses.
"""

from datetime import date, datetime
from typing import Optional, List, Any
from uuid import UUID
from pydantic import BaseModel, Field
from enum import Enum


# ---------------------------------------------------------------------------
# Shared enums
# ---------------------------------------------------------------------------

class AIPriority(str, Enum):
    HIGH = "HIGH"
    MEDIUM = "MEDIUM"
    LOW = "LOW"


class PlanSectionType(str, Enum):
    VENUE = "VENUE"
    CATERING = "CATERING"
    ENTERTAINMENT = "ENTERTAINMENT"
    DECOR = "DECOR"
    LOGISTICS = "LOGISTICS"
    PHOTOGRAPHY = "PHOTOGRAPHY"
    OTHER = "OTHER"


# ---------------------------------------------------------------------------
# Event Planner output schema
# ---------------------------------------------------------------------------

class PlanSection(BaseModel):
    title: str
    content: str
    section_type: PlanSectionType = PlanSectionType.OTHER


class TimelineItem(BaseModel):
    title: str
    due_date: str    # kept as str — validated loosely (AI dates vary in format)
    priority: AIPriority = AIPriority.MEDIUM


class EventPlanOutput(BaseModel):
    """Validated AI output for the Event Planner agent."""
    summary: str
    plan_sections: List[PlanSection] = Field(min_length=1)
    timeline: List[TimelineItem] = Field(min_length=1)
    vendor_categories_needed: List[str] = Field(default_factory=list)
    risk_notes: List[str] = Field(default_factory=list)


# ---------------------------------------------------------------------------
# Task Generator output schema
# ---------------------------------------------------------------------------

class AIGeneratedTask(BaseModel):
    title: str = Field(min_length=1, max_length=255)
    description: Optional[str] = None
    category: Optional[str] = None
    priority: AIPriority = AIPriority.MEDIUM
    due_date: Optional[str] = None   # YYYY-MM-DD string


class TaskGeneratorOutput(BaseModel):
    """Validated AI output for the Task Generator agent."""
    tasks: List[AIGeneratedTask] = Field(min_length=1)


# ---------------------------------------------------------------------------
# Budget Advisor output schema
# ---------------------------------------------------------------------------

class BudgetSplitItem(BaseModel):
    category: str
    recommended_amount: float = Field(ge=0)
    reason: str


class BudgetAdvisorOutput(BaseModel):
    """Validated AI output for the Budget Advisor agent."""
    budget_split: List[BudgetSplitItem] = Field(min_length=1)
    warnings: List[str] = Field(default_factory=list)
    saving_tips: List[str] = Field(default_factory=list)


# ---------------------------------------------------------------------------
# Vendor Recommendation output schema
# ---------------------------------------------------------------------------

class VendorRecommendationItem(BaseModel):
    vendor_id: str
    match_score: int = Field(ge=0, le=100)
    reason: str
    pros: List[str] = Field(default_factory=list)
    cons: List[str] = Field(default_factory=list)


class VendorRecommendationOutput(BaseModel):
    """Validated AI output for the Vendor Recommendation agent."""
    recommendations: List[VendorRecommendationItem]


# ---------------------------------------------------------------------------
# Chat Assistant output schema
# ---------------------------------------------------------------------------

class ChatOutput(BaseModel):
    """Validated AI output for the Chat Assistant agent."""
    message: str
    suggestions: List[str] = Field(default_factory=list)


# ---------------------------------------------------------------------------
# API request bodies
# ---------------------------------------------------------------------------

class GeneratePlanRequest(BaseModel):
    """Optional overrides when triggering the Event Planner agent."""
    additional_instructions: Optional[str] = Field(None, max_length=500)


class GenerateTasksRequest(BaseModel):
    """Optional overrides when triggering the Task Generator agent."""
    additional_instructions: Optional[str] = Field(None, max_length=500)


class BudgetAdviceRequest(BaseModel):
    """Optional overrides when triggering the Budget Advisor agent."""
    additional_instructions: Optional[str] = Field(None, max_length=500)


class RecommendVendorsRequest(BaseModel):
    """Specify which vendor IDs to evaluate (empty = top-rated from DB)."""
    vendor_ids: Optional[List[UUID]] = Field(None, max_length=10)
    additional_instructions: Optional[str] = Field(None, max_length=500)


class ChatTurn(BaseModel):
    """A single turn in chat history."""
    role: str = Field(pattern="^(user|assistant)$")
    content: str = Field(min_length=1, max_length=2000)


class ChatRequest(BaseModel):
    """Request body for the chat endpoint."""
    message: str = Field(..., min_length=1, max_length=2000)
    event_id: Optional[UUID] = None
    history: List[ChatTurn] = Field(default_factory=list, max_length=20)


# ---------------------------------------------------------------------------
# API response wrappers
# ---------------------------------------------------------------------------

class AIGenerationMeta(BaseModel):
    """Metadata about the generation stored in ai_generations table."""
    generation_id: UUID
    agent_type: str
    model_used: Optional[str]
    created_at: datetime


class EventPlanResponse(BaseModel):
    meta: AIGenerationMeta
    result: EventPlanOutput


class TaskGeneratorResponse(BaseModel):
    meta: AIGenerationMeta
    result: TaskGeneratorOutput


class BudgetAdviceResponse(BaseModel):
    meta: AIGenerationMeta
    result: BudgetAdvisorOutput


class VendorRecommendationResponse(BaseModel):
    meta: AIGenerationMeta
    result: VendorRecommendationOutput


class ChatResponse(BaseModel):
    meta: AIGenerationMeta
    result: ChatOutput


# ---------------------------------------------------------------------------
# Stored generation record (returned from history queries)
# ---------------------------------------------------------------------------

class AIGenerationRecord(BaseModel):
    id: UUID
    user_id: str
    event_id: Optional[str]
    agent_type: str
    status: str
    model_used: Optional[str]
    created_at: datetime

    class Config:
        from_attributes = True
