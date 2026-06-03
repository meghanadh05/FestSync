"""Budget Advisor Agent."""

from sqlalchemy.orm import Session
from sqlalchemy import func

from app.models.ai_generation import AgentType
from app.models.event import Event
from app.models.budget import BudgetItem
from app.modules.ai.prompts import budget_advisor as tmpl
from app.modules.ai.engine import run_agent
from app.modules.ai.schema import BudgetAdvisorOutput
from app.core.exceptions import NotFoundError, AuthorizationError


async def get_budget_advice(
    db: Session,
    event_id: str,
    user_id: str,
    additional_instructions: str | None = None,
) -> tuple[BudgetAdvisorOutput, object]:
    """
    Generate budget allocation advice for the event.

    Returns (validated_output, ai_generation_record).
    """
    from uuid import UUID
    event = db.query(Event).filter(
        Event.id == UUID(event_id),
        Event.deleted_at.is_(None),
    ).first()

    if not event:
        raise NotFoundError("Event", event_id)
    if event.user_id != user_id:
        raise AuthorizationError("You don't have permission to get budget advice for this event")

    # Aggregate existing spend to give the AI real context
    totals = db.query(
        func.sum(BudgetItem.planned_amount).label("planned"),
        func.sum(BudgetItem.actual_amount).label("actual"),
    ).filter(
        BudgetItem.event_id == event.id,
        BudgetItem.deleted_at.is_(None),
    ).first()

    already_planned = float(totals.planned or 0)
    already_spent = float(totals.actual or 0)

    user_prompt = tmpl.build_user_prompt(
        event_title=event.title,
        event_type=event.event_type.value,
        start_date=str(event.start_date),
        location=event.location,
        estimated_guests=event.estimated_guests,
        total_budget=float(event.budget) if event.budget else 0.0,
        currency=event.currency or "INR",
        already_planned=already_planned,
        already_spent=already_spent,
    )
    if additional_instructions:
        user_prompt += f"\n\nAdditional instructions: {additional_instructions}"

    return await run_agent(
        db=db,
        user_id=user_id,
        agent_type=AgentType.BUDGET_ADVISOR,
        system_prompt=tmpl.SYSTEM_PROMPT,
        user_prompt=user_prompt,
        output_schema=BudgetAdvisorOutput,
        event_id=event_id,
    )
