"""Prompt template for the Chat Assistant Agent."""

SYSTEM_PROMPT = """\
You are FestSync AI, a friendly and knowledgeable event planning assistant.

Return **valid JSON only** — no markdown, no extra text.

Schema:
{
  "message": "<your helpful response>",
  "suggestions": ["<follow-up question or action the user could take>"]
}

Rules:
- message should be conversational, helpful, and concise (2-4 sentences).
- suggestions should contain 2-3 relevant follow-up prompts the user might want to ask.
- Stay focused on event planning topics: budgets, tasks, vendors, timelines, logistics.
- If you don't know something specific about the event, ask a clarifying question.
"""


def build_user_prompt(
    message: str,
    event_context: dict | None = None,
    chat_history: list[dict] | None = None,
) -> str:
    lines = []

    if event_context:
        lines.append("Event context:")
        lines.append(f"  Title: {event_context.get('title', 'Unknown')}")
        lines.append(f"  Type: {event_context.get('event_type', 'Unknown')}")
        lines.append(f"  Date: {event_context.get('start_date', 'Unknown')}")
        if event_context.get("budget"):
            lines.append(f"  Budget: {event_context['budget']:,.0f} {event_context.get('currency', 'INR')}")
        if event_context.get("location"):
            lines.append(f"  Location: {event_context['location']}")
        lines.append("")

    if chat_history:
        lines.append("Recent conversation:")
        for turn in chat_history[-4:]:   # last 4 turns for context window economy
            role = turn.get("role", "user")
            content = turn.get("content", "")
            lines.append(f"  {role}: {content}")
        lines.append("")

    lines.append(f"User: {message}")
    lines.append("\nRespond as JSON.")
    return "\n".join(lines)
