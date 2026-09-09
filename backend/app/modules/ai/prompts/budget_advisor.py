"""Prompt template for the Budget Advisor Agent."""

SYSTEM_PROMPT = """\
You are a certified financial planner who specialises in event budgets.

Return **valid JSON only** — no markdown, no extra text.

Schema:
{
  "budget_split": [
    {
      "category": "<spend category>",
      "recommended_amount": <number>,
      "reason": "<one sentence justification>"
    }
  ],
  "warnings": ["<warning string>"],
  "saving_tips": ["<actionable tip to reduce cost>"]
}

Rules:
- budget_split amounts must sum to no more than the total budget provided.
- Include 4–8 categories in the split.
- Provide at least 2 warnings about potential over-spending or common pitfalls.
- Provide at least 3 saving_tips specific to this event type and location.
- recommended_amount must be a plain number (no currency symbol).
"""


def build_user_prompt(
    event_title: str,
    event_type: str,
    start_date: str,
    location: str | None,
    estimated_guests: int | None,
    total_budget: float,
    currency: str,
    already_planned: float = 0.0,
    already_spent: float = 0.0,
) -> str:
    lines = [
        f"Event: {event_title}",
        f"Type: {event_type}",
        f"Date: {start_date}",
        f"Total budget: {total_budget:,.0f} {currency}",
    ]
    if location:
        lines.append(f"Location: {location}")
    if estimated_guests:
        lines.append(f"Guests: {estimated_guests}")
    if already_planned > 0:
        lines.append(f"Already planned: {already_planned:,.0f} {currency}")
    if already_spent > 0:
        lines.append(f"Already spent: {already_spent:,.0f} {currency}")
    lines.append("\nProvide a recommended budget breakdown as JSON.")
    return "\n".join(lines)
