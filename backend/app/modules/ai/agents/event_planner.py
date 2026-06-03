"""Event Planner Agent."""

from sqlalchemy.orm import Session

from app.models.ai_generation import AgentType
from app.models.event import Event
from app.modules.ai import prompts
from app.modules.ai.prompts import event_planner as tmpl
from app.modules.ai.engine import run_agent
from app.modules.ai.schema import EventPlanOutput
from app.core.exceptions import NotFoundError, AuthorizationError


async def generate_event_plan(
    db: Session,
    event_id: str,
    user_id: str,
    additional_instructions: str | None = None,
) -> tuple[EventPlanOutput, object]:
    """
    Generate a comprehensive event plan for the given event.

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
        raise AuthorizationError("You don't have permission to generate a plan for this event")

    user_prompt = tmpl.build_user_prompt(
        event_title=event.title,
        event_type=event.event_type.value,
        start_date=str(event.start_date),
        location=event.location,
        estimated_guests=event.estimated_guests,
        budget=float(event.budget) if event.budget else None,
        currency=event.currency or "INR",
        description=event.description,
    )
    if additional_instructions:
        user_prompt += f"\n\nAdditional instructions: {additional_instructions}"

    return await run_agent(
        db=db,
        user_id=user_id,
        agent_type=AgentType.EVENT_PLANNER,
        system_prompt=tmpl.SYSTEM_PROMPT,
        user_prompt=user_prompt,
        output_schema=EventPlanOutput,
        event_id=event_id,
    )
