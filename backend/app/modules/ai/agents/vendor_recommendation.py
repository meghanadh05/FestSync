"""Vendor Recommendation Agent."""

from typing import Optional, List
from uuid import UUID
from sqlalchemy.orm import Session

from app.models.ai_generation import AgentType
from app.models.event import Event
from app.models.vendor import Vendor, SavedVendor
from app.modules.ai.prompts import vendor_recommendation as tmpl
from app.modules.ai.engine import run_agent
from app.modules.ai.schema import VendorRecommendationOutput
from app.core.exceptions import NotFoundError, AuthorizationError

_TOP_N_DEFAULT = 6   # vendors pulled from DB when caller doesn't specify IDs


async def recommend_vendors(
    db: Session,
    event_id: str,
    user_id: str,
    vendor_ids: Optional[List[UUID]] = None,
    additional_instructions: str | None = None,
) -> tuple[VendorRecommendationOutput, object]:
    """
    AI ranks vendors by fit for this event.

    If vendor_ids are provided, only those are evaluated.
    Otherwise, the top _TOP_N_DEFAULT active vendors are used.

    Returns (validated_output, ai_generation_record).
    """
    event = db.query(Event).filter(
        Event.id == UUID(event_id),
        Event.deleted_at.is_(None),
    ).first()

    if not event:
        raise NotFoundError("Event", event_id)
    if event.user_id != user_id:
        raise AuthorizationError("You don't have permission to get vendor recommendations for this event")

    # Resolve vendor list
    if vendor_ids:
        vendors = db.query(Vendor).filter(
            Vendor.id.in_(vendor_ids),
            Vendor.deleted_at.is_(None),
        ).all()
    else:
        # Pull top-rated vendors in relevant categories
        from app.modules.vendors.service import _EVENT_CATEGORY_MAP
        event_type = event.event_type.value
        preferred_cats = _EVENT_CATEGORY_MAP.get(event_type, [])

        query = db.query(Vendor).filter(Vendor.deleted_at.is_(None), Vendor.active.is_(True))
        if preferred_cats:
            query = query.filter(Vendor.category.in_(preferred_cats))
        vendors = query.order_by(Vendor.rating.desc()).limit(_TOP_N_DEFAULT).all()

    if not vendors:
        raise NotFoundError("Vendors", "no vendors available for this event type")

    vendor_dicts = [
        {
            "vendor_id": str(v.id),
            "name": v.business_name,
            "category": v.category.value,
            "city": v.city or v.location,
            "price": float(v.starting_price) if v.starting_price else None,
            "rating": float(v.rating or 0),
            "verified": v.verified,
        }
        for v in vendors
    ]

    user_prompt = tmpl.build_user_prompt(
        event_title=event.title,
        event_type=event.event_type.value,
        start_date=str(event.start_date),
        location=event.location,
        budget=float(event.budget) if event.budget else None,
        currency=event.currency or "INR",
        vendors=vendor_dicts,
    )
    if additional_instructions:
        user_prompt += f"\n\nAdditional instructions: {additional_instructions}"

    return await run_agent(
        db=db,
        user_id=user_id,
        agent_type=AgentType.VENDOR_RECOMMENDATION,
        system_prompt=tmpl.SYSTEM_PROMPT,
        user_prompt=user_prompt,
        output_schema=VendorRecommendationOutput,
        event_id=event_id,
    )
