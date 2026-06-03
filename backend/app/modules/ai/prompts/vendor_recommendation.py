"""Prompt template for the Vendor Recommendation Agent."""

SYSTEM_PROMPT = """\
You are an event sourcing specialist who helps clients choose the right vendors.

Return **valid JSON only** — no markdown, no extra text.

Schema:
{
  "recommendations": [
    {
      "vendor_id": "<the exact vendor_id string provided in the input>",
      "match_score": <integer 0-100>,
      "reason": "<one sentence summary of why this vendor fits>",
      "pros": ["<pro>"],
      "cons": ["<con>"]
    }
  ]
}

Rules:
- Only include vendors whose vendor_id appears in the input list.
- match_score must reflect budget fit, location proximity, rating, and event-type relevance.
- Each vendor must have at least 2 pros and 1 con.
- Sort recommendations by match_score descending.
- Be honest about cons — this builds user trust.
"""


def build_user_prompt(
    event_title: str,
    event_type: str,
    start_date: str,
    location: str | None,
    budget: float | None,
    currency: str,
    vendors: list[dict],
) -> str:
    """
    vendors: list of dicts with keys vendor_id, name, category, city, price, rating, verified
    """
    lines = [
        f"Event: {event_title}",
        f"Type: {event_type}",
        f"Date: {start_date}",
    ]
    if location:
        lines.append(f"Event location: {location}")
    if budget:
        lines.append(f"Budget: {budget:,.0f} {currency}")

    lines.append("\nVendors to evaluate:")
    for v in vendors:
        price = f"{v.get('price'):,.0f} {currency}" if v.get("price") else "Price not listed"
        verified = "Verified" if v.get("verified") else "Not verified"
        lines.append(
            f"- vendor_id={v['vendor_id']} | {v['name']} | {v['category']} | "
            f"{v.get('city', 'unknown city')} | {price} | Rating: {v.get('rating', 0)}/5 | {verified}"
        )

    lines.append("\nReturn recommendations JSON.")
    return "\n".join(lines)
