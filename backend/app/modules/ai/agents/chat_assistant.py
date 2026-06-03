"""Chat Assistant Agent."""

from typing import Optional, List
from uuid import UUID
from sqlalchemy.orm import Session

from app.models.ai_generation import AgentType
from app.models.event import Event
from app.modules.ai.prompts import chat_assistant as tmpl
from app.modules.ai.engine import run_agent
from app.modules.ai.schema import ChatOutput, ChatTurn


async def chat(
    db: Session,
    user_id: str,
    message: str,
    event_id: Optional[UUID] = None,
    history: Optional[List[ChatTurn]] = None,
) -> tuple[ChatOutput, object]:
    """
    Respond to a user message, optionally in the context of an event.

    Returns (validated_output, ai_generation_record).
    """
    event_context: dict | None = None

    if event_id:
        event = db.query(Event).filter(
            Event.id == event_id,
            Event.deleted_at.is_(None),
        ).first()

        # If event exists and belongs to user, add context (but don't 403 if not)
        if event and event.user_id == user_id:
            event_context = {
                "title": event.title,
                "event_type": event.event_type.value,
                "start_date": str(event.start_date),
                "budget": float(event.budget) if event.budget else None,
                "currency": event.currency or "INR",
                "location": event.location,
            }

    history_dicts = (
        [{"role": t.role, "content": t.content} for t in history]
        if history
        else None
    )

    user_prompt = tmpl.build_user_prompt(
        message=message,
        event_context=event_context,
        chat_history=history_dicts,
    )

    return await run_agent(
        db=db,
        user_id=user_id,
        agent_type=AgentType.CHAT_ASSISTANT,
        system_prompt=tmpl.SYSTEM_PROMPT,
        user_prompt=user_prompt,
        output_schema=ChatOutput,
        event_id=str(event_id) if event_id else None,
    )
