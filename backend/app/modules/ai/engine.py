"""
AI Generation Engine — handles the call → parse → validate → persist flow.

Every agent goes through run_agent() so logging, error handling,
and DB persistence are done in one place.
"""

import json
import logging
from typing import Type, TypeVar
from uuid import UUID
from pydantic import BaseModel, ValidationError
from sqlalchemy.orm import Session

from app.models.ai_generation import AIGeneration, AgentType, GenerationStatus
from app.modules.ai.provider import get_provider, AIProviderError

logger = logging.getLogger(__name__)

T = TypeVar("T", bound=BaseModel)


class AIEngineError(Exception):
    """Raised when the engine cannot produce a valid result."""
    def __init__(self, message: str, status: GenerationStatus = GenerationStatus.FAILED) -> None:
        super().__init__(message)
        self.status = status


async def run_agent(
    db: Session,
    user_id: str,
    agent_type: AgentType,
    system_prompt: str,
    user_prompt: str,
    output_schema: Type[T],
    event_id: str | None = None,
) -> tuple[T, AIGeneration]:
    """
    Core execution flow:
      1. Call the AI provider.
      2. Parse the raw text as JSON.
      3. Validate against output_schema.
      4. Persist the generation record.
      5. Return (validated_output, generation_record).

    Raises AIEngineError (which the route layer converts to HTTPException).
    """
    provider = get_provider()
    raw_text: str | None = None
    status = GenerationStatus.SUCCESS
    error_message: str | None = None
    response_json: str | None = None

    # ---- Step 1: call provider ----
    try:
        raw_text = await provider.complete(system_prompt, user_prompt)
    except AIProviderError as exc:
        error_message = str(exc)
        status = GenerationStatus.FAILED
        _persist(db, user_id, event_id, agent_type, user_prompt, None, status, error_message, provider.model_name)
        raise AIEngineError(f"AI provider failed: {exc}")

    # ---- Step 2: parse JSON ----
    try:
        parsed = json.loads(raw_text)
    except json.JSONDecodeError as exc:
        error_message = f"AI returned invalid JSON: {exc}"
        status = GenerationStatus.INVALID_JSON
        _persist(db, user_id, event_id, agent_type, user_prompt, None, status, error_message, provider.model_name)
        raise AIEngineError(error_message, GenerationStatus.INVALID_JSON)

    # ---- Step 3: validate schema ----
    try:
        validated: T = output_schema.model_validate(parsed)
    except ValidationError as exc:
        error_message = f"AI output failed schema validation: {exc}"
        status = GenerationStatus.INVALID_JSON
        _persist(db, user_id, event_id, agent_type, user_prompt, None, status, error_message, provider.model_name)
        raise AIEngineError(error_message, GenerationStatus.INVALID_JSON)

    # ---- Step 4: persist success ----
    response_json = json.dumps(parsed)
    record = _persist(
        db, user_id, event_id, agent_type, user_prompt,
        response_json, GenerationStatus.SUCCESS, None, provider.model_name,
    )

    logger.info(
        "AI generation %s | agent=%s | model=%s | user=%s",
        record.id, agent_type.value, provider.model_name, user_id,
    )

    return validated, record


def _persist(
    db: Session,
    user_id: str,
    event_id: str | None,
    agent_type: AgentType,
    prompt: str,
    response_json: str | None,
    status: GenerationStatus,
    error_message: str | None,
    model_used: str,
) -> AIGeneration:
    record = AIGeneration(
        user_id=user_id,
        event_id=str(event_id) if event_id else None,
        agent_type=agent_type,
        prompt=prompt,
        response_json=response_json,
        status=status,
        error_message=error_message,
        model_used=model_used,
    )
    db.add(record)
    db.commit()
    db.refresh(record)
    return record
