"""
AI module API routes.

All AI calls happen server-side. The frontend never touches AI providers directly.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import get_current_user_id
from app.core.exceptions import NotFoundError, AuthorizationError
from app.modules.ai.engine import AIEngineError
from app.modules.ai.schema import (
    GeneratePlanRequest,
    GenerateTasksRequest,
    BudgetAdviceRequest,
    RecommendVendorsRequest,
    ChatRequest,
    EventPlanResponse,
    TaskGeneratorResponse,
    BudgetAdviceResponse,
    VendorRecommendationResponse,
    ChatResponse,
    AIGenerationMeta,
)
from app.modules.ai.agents import (
    event_planner,
    task_generator,
    budget_advisor,
    vendor_recommendation,
    chat_assistant,
)

router = APIRouter(prefix="/ai")


def _meta(record) -> AIGenerationMeta:
    """Build AIGenerationMeta from an AIGeneration ORM record."""
    return AIGenerationMeta(
        generation_id=record.id,
        agent_type=record.agent_type.value,
        model_used=record.model_used,
        created_at=record.created_at,
    )


def _handle_errors(exc: Exception):
    """Convert domain errors to HTTP responses."""
    if isinstance(exc, AIEngineError):
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail=str(exc),
        )
    if isinstance(exc, NotFoundError):
        raise HTTPException(status_code=404, detail=str(exc))
    if isinstance(exc, AuthorizationError):
        raise HTTPException(status_code=403, detail=str(exc))
    raise exc   # unexpected — let FastAPI's 500 handler catch it


@router.post("/events/{event_id}/generate-plan", response_model=EventPlanResponse, status_code=201)
async def generate_plan(
    event_id: str,
    body: GeneratePlanRequest = None,
    user_id: str = Depends(get_current_user_id),
    db: Session = Depends(get_db),
):
    """
    Generate a comprehensive event plan using AI.

    The plan includes sections, timeline, vendor categories, and risk notes.
    The raw result is stored in ai_generations for audit purposes.
    """
    try:
        output, record = await event_planner.generate_event_plan(
            db=db,
            event_id=event_id,
            user_id=user_id,
            additional_instructions=body.additional_instructions if body else None,
        )
        return EventPlanResponse(meta=_meta(record), result=output)
    except Exception as exc:
        _handle_errors(exc)


@router.post("/events/{event_id}/generate-tasks", response_model=TaskGeneratorResponse, status_code=201)
async def generate_tasks(
    event_id: str,
    body: GenerateTasksRequest = None,
    user_id: str = Depends(get_current_user_id),
    db: Session = Depends(get_db),
):
    """
    Generate a task list for an event using AI.

    Tasks are returned in JSON and can be reviewed before being saved.
    """
    try:
        output, record = await task_generator.generate_tasks(
            db=db,
            event_id=event_id,
            user_id=user_id,
            additional_instructions=body.additional_instructions if body else None,
        )
        return TaskGeneratorResponse(meta=_meta(record), result=output)
    except Exception as exc:
        _handle_errors(exc)


@router.post("/events/{event_id}/budget-advice", response_model=BudgetAdviceResponse, status_code=201)
async def budget_advice(
    event_id: str,
    body: BudgetAdviceRequest = None,
    user_id: str = Depends(get_current_user_id),
    db: Session = Depends(get_db),
):
    """
    Get AI-powered budget allocation advice for an event.

    Returns recommended spend per category plus warnings and saving tips.
    """
    try:
        output, record = await budget_advisor.get_budget_advice(
            db=db,
            event_id=event_id,
            user_id=user_id,
            additional_instructions=body.additional_instructions if body else None,
        )
        return BudgetAdviceResponse(meta=_meta(record), result=output)
    except Exception as exc:
        _handle_errors(exc)


@router.post("/events/{event_id}/recommend-vendors", response_model=VendorRecommendationResponse, status_code=201)
async def recommend_vendors(
    event_id: str,
    body: RecommendVendorsRequest = None,
    user_id: str = Depends(get_current_user_id),
    db: Session = Depends(get_db),
):
    """
    Get AI vendor recommendations for an event.

    Pass vendor_ids in the body to rank specific vendors,
    or leave it empty to let the backend pick top-rated candidates.
    """
    try:
        output, record = await vendor_recommendation.recommend_vendors(
            db=db,
            event_id=event_id,
            user_id=user_id,
            vendor_ids=body.vendor_ids if body else None,
            additional_instructions=body.additional_instructions if body else None,
        )
        return VendorRecommendationResponse(meta=_meta(record), result=output)
    except Exception as exc:
        _handle_errors(exc)


@router.post("/chat", response_model=ChatResponse, status_code=201)
async def chat(
    body: ChatRequest,
    user_id: str = Depends(get_current_user_id),
    db: Session = Depends(get_db),
):
    """
    Chat with the FestSync AI assistant.

    Optionally attach an event_id for contextual answers.
    Pass history (up to 20 turns) to maintain conversation context.
    """
    try:
        output, record = await chat_assistant.chat(
            db=db,
            user_id=user_id,
            message=body.message,
            event_id=body.event_id,
            history=body.history,
        )
        return ChatResponse(meta=_meta(record), result=output)
    except Exception as exc:
        _handle_errors(exc)
