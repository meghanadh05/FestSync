"""Prompt template for the Task Generator Agent."""

SYSTEM_PROMPT = """\
You are a professional event coordinator specialising in breaking down event plans \
into concrete, actionable tasks.

Return **valid JSON only** — no markdown, no extra text.

Schema:
{
  "tasks": [
    {
      "title": "<short, imperative task title>",
      "description": "<1-2 sentence description of what needs to be done>",
      "category": "<category string, e.g. Venue, Catering, Marketing, Logistics>",
      "priority": "<HIGH|MEDIUM|LOW>",
      "due_date": "YYYY-MM-DD"
    }
  ]
}

Rules:
- Generate between 8 and 20 tasks depending on event complexity.
- Distribute tasks across multiple categories.
- due_date must be a real date between today and the event date.
- Tasks should be ordered roughly by when they need to be done.
- Mark critical path items (venue, catering, permits) as HIGH priority.
"""


def build_user_prompt(
    event_title: str,
    event_type: str,
    start_date: str,
    location: str | None,
    estimated_guests: int | None,
    budget: float | None,
    currency: str,
    existing_task_count: int = 0,
) -> str:
    lines = [
        f"Event: {event_title}",
        f"Type: {event_type}",
        f"Date: {start_date}",
    ]
    if location:
        lines.append(f"Location: {location}")
    if estimated_guests:
        lines.append(f"Guest count: {estimated_guests}")
    if budget:
        lines.append(f"Budget: {budget:,.0f} {currency}")
    if existing_task_count:
        lines.append(f"The event already has {existing_task_count} tasks — avoid duplicating obvious ones.")
    lines.append("\nGenerate a task list as JSON.")
    return "\n".join(lines)
