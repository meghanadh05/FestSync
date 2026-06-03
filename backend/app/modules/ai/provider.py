"""
AI provider abstraction — OpenAI, Gemini, or Mock.

All agents call `get_completion(prompt)` and receive a raw JSON string back.
The calling agent is responsible for parsing and validating that string.
"""

import json
import logging
from typing import Protocol

from app.core.config import settings

logger = logging.getLogger(__name__)


class AIProvider(Protocol):
    """Protocol that every concrete provider must satisfy."""

    async def complete(self, system_prompt: str, user_prompt: str) -> str:
        """
        Send system + user prompts; return the model's text response.
        Should raise AIProviderError on failure.
        """
        ...

    @property
    def model_name(self) -> str:
        """Human-readable identifier stored in ai_generations.model_used."""
        ...


class AIProviderError(Exception):
    """Raised when the AI provider returns an error or unusable response."""
    pass


# ---------------------------------------------------------------------------
# Mock provider — used when AI_PROVIDER=mock or keys are missing in dev
# ---------------------------------------------------------------------------

_MOCK_RESPONSES = {
    "event_planner": json.dumps({
        "summary": "A beautifully curated event plan.",
        "plan_sections": [
            {"title": "Venue Plan", "content": "Book a 3-star venue in the city centre.", "section_type": "VENUE"},
            {"title": "Catering Plan", "content": "Arrange buffet-style catering for all guests.", "section_type": "CATERING"},
        ],
        "timeline": [
            {"title": "Confirm venue", "due_date": "2026-09-01", "priority": "HIGH"},
            {"title": "Send invitations", "due_date": "2026-09-15", "priority": "MEDIUM"},
        ],
        "vendor_categories_needed": ["Venue", "Catering", "Photography"],
        "risk_notes": ["Book venue at least 3 months in advance to avoid unavailability."],
    }),
    "task_generator": json.dumps({
        "tasks": [
            {"title": "Book venue", "description": "Research and finalise venue.", "category": "Venue", "priority": "HIGH", "due_date": "2026-09-01"},
            {"title": "Send invitations", "description": "Design and send digital invites.", "category": "Communications", "priority": "MEDIUM", "due_date": "2026-09-15"},
            {"title": "Arrange catering", "description": "Get quotes from 3 caterers.", "category": "Catering", "priority": "HIGH", "due_date": "2026-09-10"},
        ]
    }),
    "budget_advisor": json.dumps({
        "budget_split": [
            {"category": "Venue", "recommended_amount": 25000, "reason": "Venue is the primary cost centre."},
            {"category": "Catering", "recommended_amount": 15000, "reason": "Food and beverage for guests."},
            {"category": "Photography", "recommended_amount": 8000, "reason": "Memories last forever."},
            {"category": "Decoration", "recommended_amount": 5000, "reason": "Aesthetic enhancements."},
        ],
        "warnings": ["You are allocating less than 20% of budget to catering. Consider increasing."],
        "saving_tips": ["Book vendors off-season for up to 30% discount.", "Use digital invitations instead of printed ones."],
    }),
    "vendor_recommendation": json.dumps({
        "recommendations": [
            {"vendor_id": "mock-vendor-1", "match_score": 92, "reason": "Highly rated local caterer within budget.", "pros": ["Well reviewed", "Local"], "cons": ["Limited weekend slots"]},
            {"vendor_id": "mock-vendor-2", "match_score": 85, "reason": "Popular venue with good infrastructure.", "pros": ["Good infrastructure", "Parking available"], "cons": ["Slightly over budget"]},
        ]
    }),
    "chat": json.dumps({
        "message": "I'm here to help you plan your event! You can ask me about tasks, budget advice, vendors, or anything else.",
        "suggestions": ["What tasks should I create first?", "How should I split my budget?", "Which vendors are best for my event?"],
    }),
}


class MockProvider:
    """Returns pre-built mock JSON — zero API calls, instant responses."""

    @property
    def model_name(self) -> str:
        return "mock"

    async def complete(self, system_prompt: str, user_prompt: str) -> str:
        # Match on the most distinctive phrase in each system prompt (ordered most→least specific)
        sp = system_prompt.lower()
        if "festsync ai" in sp:
            return _MOCK_RESPONSES["chat"]
        if "breaking down event plans" in sp or "task list" in sp:
            return _MOCK_RESPONSES["task_generator"]
        if "financial planner" in sp or "certified" in sp:
            return _MOCK_RESPONSES["budget_advisor"]
        if "sourcing specialist" in sp:
            return _MOCK_RESPONSES["vendor_recommendation"]
        if "expert event planner" in sp or "15 years" in sp:
            return _MOCK_RESPONSES["event_planner"]
        return _MOCK_RESPONSES["chat"]


# ---------------------------------------------------------------------------
# OpenAI provider
# ---------------------------------------------------------------------------

class OpenAIProvider:
    """Thin wrapper around openai>=1.0 async client."""

    def __init__(self) -> None:
        try:
            from openai import AsyncOpenAI
        except ImportError:
            raise AIProviderError("openai package not installed. Run: pip install openai")
        if not settings.OPENAI_API_KEY:
            raise AIProviderError("OPENAI_API_KEY is not set")
        self._client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)
        self._model = settings.OPENAI_MODEL

    @property
    def model_name(self) -> str:
        return f"openai/{self._model}"

    async def complete(self, system_prompt: str, user_prompt: str) -> str:
        try:
            response = await self._client.chat.completions.create(
                model=self._model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt},
                ],
                response_format={"type": "json_object"},
                temperature=0.4,
            )
            content = response.choices[0].message.content
            if not content:
                raise AIProviderError("OpenAI returned empty content")
            return content
        except Exception as exc:
            logger.error("OpenAI completion failed: %s", exc)
            raise AIProviderError(f"OpenAI error: {exc}") from exc


# ---------------------------------------------------------------------------
# Gemini provider
# ---------------------------------------------------------------------------

class GeminiProvider:
    """Thin wrapper around google-generativeai."""

    def __init__(self) -> None:
        try:
            import google.generativeai as genai
        except ImportError:
            raise AIProviderError(
                "google-generativeai package not installed. Run: pip install google-generativeai"
            )
        if not settings.GEMINI_API_KEY:
            raise AIProviderError("GEMINI_API_KEY is not set")
        genai.configure(api_key=settings.GEMINI_API_KEY)
        self._genai = genai
        self._model_name = settings.GEMINI_MODEL

    @property
    def model_name(self) -> str:
        return f"gemini/{self._model_name}"

    async def complete(self, system_prompt: str, user_prompt: str) -> str:
        import asyncio
        try:
            model = self._genai.GenerativeModel(
                model_name=self._model_name,
                system_instruction=system_prompt,
                generation_config={"response_mime_type": "application/json"},
            )
            # Gemini SDK is sync — run in thread to avoid blocking the event loop
            loop = asyncio.get_event_loop()
            response = await loop.run_in_executor(
                None,
                lambda: model.generate_content(user_prompt),
            )
            text = response.text
            if not text:
                raise AIProviderError("Gemini returned empty content")
            return text
        except AIProviderError:
            raise
        except Exception as exc:
            logger.error("Gemini completion failed: %s", exc)
            raise AIProviderError(f"Gemini error: {exc}") from exc


# ---------------------------------------------------------------------------
# Factory
# ---------------------------------------------------------------------------

def get_provider() -> "OpenAIProvider | GeminiProvider | MockProvider":
    """
    Return the configured provider singleton.

    Falls back to MockProvider if:
    - AI_PROVIDER=mock  (explicit)
    - the selected provider's key is missing in dev/test mode
    """
    provider_name = settings.AI_PROVIDER.lower()

    if provider_name == "openai":
        if not settings.OPENAI_API_KEY or settings.OPENAI_API_KEY.startswith("sk-test"):
            logger.warning("OPENAI_API_KEY not set or is a placeholder — using MockProvider")
            return MockProvider()
        return OpenAIProvider()

    if provider_name == "gemini":
        if not settings.GEMINI_API_KEY or settings.GEMINI_API_KEY == "test-key":
            logger.warning("GEMINI_API_KEY not set or is a placeholder — using MockProvider")
            return MockProvider()
        return GeminiProvider()

    # Default / explicit mock
    return MockProvider()
