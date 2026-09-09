"""Task Generator Agent."""

from sqlalchemy.orm import Session

from app.models.ai_generation import AgentType
from app.models.event import Event
from app.models.task import Task
from app.modules.ai.prompts import task_generator as tmpl
from app.modules.ai.engine import run_agent
from app.modules.ai.schema import TaskGeneratorOutput
from app.core.exceptions import NotFoundError, AuthorizationError


async def generate_tasks(
    db: Session,
    event_id: str,
    user_id: str,
    additional_instructions: str | None = None,
) -> tuple[TaskGeneratorOutput, object]:
    """
    Generate a list of tasks for the event.

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
        raise AuthorizationError("You don't have permission to generate tasks for this event")

    existing_count = db.query(Task).filter(
        Task.event_id == event.id,
        Task.deleted_at.is_(None),
    ).count()

    user_prompt = tmpl.build_user_prompt(
        event_title=event.title,
        event_type=event.event_type.value,
        start_date=str(event.start_date),
        location=event.location,
        estimated_guests=event.estimated_guests,
        budget=float(event.budget) if event.budget else None,
        currency=event.currency or "INR",
        existing_task_count=existing_count,
    )
    if additional_instructions:
        user_prompt += f"\n\nAdditional instructions: {additional_instructions}"

    return await run_agent(
        db=db,
        user_id=user_id,
        agent_type=AgentType.TASK_GENERATOR,
        system_prompt=tmpl.SYSTEM_PROMPT,
        user_prompt=user_prompt,
        output_schema=TaskGeneratorOutput,
        event_id=event_id,
    )
