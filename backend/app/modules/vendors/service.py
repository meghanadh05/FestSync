"""
Vendor service — business logic, search, match scoring, save/compare.
"""

from datetime import datetime, date
from typing import Optional, List, Tuple, Dict
from uuid import UUID
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_

from app.models.vendor import Vendor, VendorService as VendorServiceModel, VendorImage, SavedVendor
from app.models.event import Event
from app.modules.vendors.schema import (
    VendorCreate,
    VendorUpdate,
    VendorServiceCreate,
    SaveVendorRequest,
    VendorCard,
    VendorCompareItem,
)
from app.core.exceptions import NotFoundError, AuthorizationError, ConflictError


# ---------------------------------------------------------------------------
# Match scoring helpers
# ---------------------------------------------------------------------------

# Event-type → relevant vendor categories (higher relevance = more points)
_EVENT_CATEGORY_MAP: Dict[str, List[str]] = {
    "WEDDING":        ["VENUE", "CATERING", "PHOTOGRAPHY", "DECORATION", "MUSIC", "FLORIST", "BAKERY", "ATTIRE"],
    "BIRTHDAY":       ["CATERING", "DECORATION", "BAKERY", "MUSIC", "PHOTOGRAPHY"],
    "COLLEGE_FEST":   ["MUSIC", "DJ", "CATERING", "LIGHTING", "EVENT_PLANNER"],
    "CORPORATE_EVENT":["VENUE", "CATERING", "EVENT_PLANNER", "PHOTOGRAPHY", "TRANSPORT"],
    "CONFERENCE":     ["VENUE", "CATERING", "EVENT_PLANNER", "LIGHTING", "TRANSPORT"],
    "RECEPTION":      ["VENUE", "CATERING", "DECORATION", "MUSIC", "PHOTOGRAPHY"],
    "ENGAGEMENT":     ["VENUE", "CATERING", "PHOTOGRAPHY", "DECORATION", "FLORIST"],
    "CONCERT":        ["LIGHTING", "MUSIC", "DJ", "CATERING", "SECURITY"],
    "OTHER":          [],
}


def _compute_match_score(
    vendor: Vendor,
    event_budget: Optional[float] = None,
    event_location: Optional[str] = None,
    event_type: Optional[str] = None,
) -> Tuple[int, str]:
    """
    Deterministic match score 0-100.

    Breakdown:
        Rating          → up to 30 pts   (rating / 5 * 30)
        Budget fit      → up to 25 pts
        Location match  → up to 25 pts
        Event-type fit  → up to 20 pts

    Returns (score, short_reason).
    """
    score = 0
    reasons: List[str] = []

    # --- Rating (30 pts) ---
    rating = float(vendor.rating or 0)
    rating_pts = int((rating / 5.0) * 30)
    score += rating_pts
    if rating >= 4.5:
        reasons.append("highly rated")
    elif rating >= 4.0:
        reasons.append("well rated")

    # --- Budget fit (25 pts) ---
    if event_budget and event_budget > 0 and vendor.starting_price is not None:
        vendor_price = float(vendor.starting_price)
        if vendor_price <= event_budget * 0.3:
            # Very affordable — perfect fit
            score += 25
            reasons.append("fits budget")
        elif vendor_price <= event_budget * 0.6:
            score += 18
            reasons.append("budget-friendly")
        elif vendor_price <= event_budget:
            score += 10
        # Over budget → 0 pts
        else:
            reasons.append("above budget")
    elif vendor.starting_price is None:
        # Price not listed – give partial credit
        score += 12

    # --- Location match (25 pts) ---
    if event_location and vendor.city:
        event_loc_lower = event_location.lower()
        vendor_city_lower = vendor.city.lower()
        vendor_location_lower = vendor.location.lower()
        if vendor_city_lower in event_loc_lower or event_loc_lower in vendor_city_lower:
            score += 25
            reasons.append("local vendor")
        elif vendor_location_lower in event_loc_lower or event_loc_lower in vendor_location_lower:
            score += 15
            reasons.append("nearby vendor")
        else:
            score += 5
    elif not event_location:
        score += 12

    # --- Event-type relevance (20 pts) ---
    if event_type and event_type in _EVENT_CATEGORY_MAP:
        preferred_categories = _EVENT_CATEGORY_MAP[event_type]
        cat_value = vendor.category.value if hasattr(vendor.category, "value") else str(vendor.category)
        if cat_value in preferred_categories:
            # Top-3 categories in list score higher
            try:
                pos = preferred_categories.index(cat_value)
                if pos < 3:
                    score += 20
                    reasons.append(f"ideal for {event_type.lower().replace('_', ' ')}")
                else:
                    score += 12
                    reasons.append(f"suitable for {event_type.lower().replace('_', ' ')}")
            except ValueError:
                score += 8

    # Verified bonus (+2, kept small to avoid drowning other signals)
    if vendor.verified:
        score = min(score + 2, 100)
        if "verified" not in reasons:
            reasons.append("verified vendor")

    score = max(0, min(score, 100))
    reason = ", ".join(reasons[:3]) if reasons else "general match"
    return score, reason.capitalize()


def _vendor_to_card(
    vendor: Vendor,
    event_budget: Optional[float] = None,
    event_location: Optional[str] = None,
    event_type: Optional[str] = None,
) -> VendorCard:
    """Convert Vendor ORM object to VendorCard schema."""
    score, reason = _compute_match_score(vendor, event_budget, event_location, event_type)
    return VendorCard(
        id=vendor.id,
        business_name=vendor.business_name,
        category=vendor.category,
        location=vendor.location,
        city=vendor.city,
        starting_price=float(vendor.starting_price) if vendor.starting_price is not None else None,
        currency=vendor.currency,
        rating=float(vendor.rating or 0),
        review_count=vendor.review_count or 0,
        verified=vendor.verified,
        primary_image_url=vendor.primary_image_url,
        match_score=score,
        match_reason=reason,
    )


# ---------------------------------------------------------------------------
# Service class
# ---------------------------------------------------------------------------

class VendorService:
    """Service for vendor operations."""

    # ------------------------------------------------------------------
    # Vendor CRUD
    # ------------------------------------------------------------------

    @staticmethod
    def create_vendor(db: Session, user_id: str, vendor_data: VendorCreate) -> Vendor:
        """Create a new vendor profile owned by the authenticated user."""
        supported = (
            ",".join(vendor_data.supported_event_types)
            if vendor_data.supported_event_types
            else None
        )
        db_vendor = Vendor(
            owner_user_id=user_id,
            business_name=vendor_data.business_name,
            description=vendor_data.description,
            category=vendor_data.category,
            location=vendor_data.location,
            city=vendor_data.city,
            state=vendor_data.state,
            country=vendor_data.country or "India",
            email=vendor_data.email,
            phone=vendor_data.phone,
            website=vendor_data.website,
            starting_price=vendor_data.starting_price,
            currency=vendor_data.currency,
            supported_event_types=supported,
            primary_image_url=vendor_data.primary_image_url,
        )
        db.add(db_vendor)
        db.commit()
        db.refresh(db_vendor)
        return db_vendor

    @staticmethod
    def get_vendor_by_id(db: Session, vendor_id: str) -> Vendor:
        """Fetch a single vendor (public — no ownership check)."""
        if isinstance(vendor_id, str):
            try:
                vendor_id = UUID(vendor_id)
            except ValueError:
                raise NotFoundError("Vendor", vendor_id)

        vendor = db.query(Vendor).filter(
            Vendor.id == vendor_id,
            Vendor.deleted_at.is_(None),
            Vendor.active.is_(True),
        ).first()

        if not vendor:
            raise NotFoundError("Vendor", str(vendor_id))

        return vendor

    @staticmethod
    def update_vendor(db: Session, vendor_id: str, user_id: str, data: VendorUpdate) -> Vendor:
        """Update a vendor profile (owner only)."""
        vendor = VendorService.get_vendor_by_id(db, vendor_id)
        if vendor.owner_user_id != user_id:
            raise AuthorizationError("You don't have permission to update this vendor")

        update = data.model_dump(exclude_unset=True)
        if "supported_event_types" in update and isinstance(update["supported_event_types"], list):
            update["supported_event_types"] = ",".join(update["supported_event_types"])

        for field, value in update.items():
            setattr(vendor, field, value)

        vendor.updated_at = datetime.utcnow()
        db.commit()
        db.refresh(vendor)
        return vendor

    # ------------------------------------------------------------------
    # Search
    # ------------------------------------------------------------------

    @staticmethod
    def search_vendors(
        db: Session,
        skip: int = 0,
        limit: int = 12,
        category: Optional[str] = None,
        location: Optional[str] = None,
        event_type: Optional[str] = None,
        min_price: Optional[float] = None,
        max_price: Optional[float] = None,
        min_rating: Optional[float] = None,
        availability_date: Optional[date] = None,
        verified_only: bool = False,
        # Contextual signals for scoring
        event_budget: Optional[float] = None,
    ) -> Tuple[int, List[VendorCard]]:
        """
        Search & filter vendors; returns cards with match scores.

        availability_date is stored for future booking conflict checks.
        Right now we have no bookings table so it is accepted but not filtered.
        """
        query = db.query(Vendor).filter(
            Vendor.deleted_at.is_(None),
            Vendor.active.is_(True),
        )

        if category:
            query = query.filter(Vendor.category == category)

        if location:
            pattern = f"%{location}%"
            query = query.filter(
                or_(
                    Vendor.city.ilike(pattern),
                    Vendor.location.ilike(pattern),
                    Vendor.state.ilike(pattern),
                )
            )

        if event_type:
            preferred = _EVENT_CATEGORY_MAP.get(event_type, [])
            if preferred:
                query = query.filter(Vendor.category.in_(preferred))

        if min_price is not None:
            query = query.filter(
                or_(Vendor.starting_price >= min_price, Vendor.starting_price.is_(None))
            )

        if max_price is not None:
            query = query.filter(
                or_(Vendor.starting_price <= max_price, Vendor.starting_price.is_(None))
            )

        if min_rating is not None:
            query = query.filter(Vendor.rating >= min_rating)

        if verified_only:
            query = query.filter(Vendor.verified.is_(True))

        total = query.count()
        vendors = query.offset(skip).limit(limit).all()

        cards = [_vendor_to_card(v, event_budget, location, event_type) for v in vendors]
        # Re-sort by match score descending after scoring
        cards.sort(key=lambda c: c.match_score, reverse=True)

        return total, cards

    # ------------------------------------------------------------------
    # Vendor Services
    # ------------------------------------------------------------------

    @staticmethod
    def add_service(
        db: Session,
        vendor_id: str,
        user_id: str,
        service_data: VendorServiceCreate,
    ) -> VendorServiceModel:
        """Add a service to a vendor (owner only)."""
        vendor = VendorService.get_vendor_by_id(db, vendor_id)
        if vendor.owner_user_id != user_id:
            raise AuthorizationError("You don't have permission to add services to this vendor")

        svc = VendorServiceModel(
            vendor_id=vendor.id,
            name=service_data.name,
            description=service_data.description,
            price=service_data.price,
            unit=service_data.unit,
        )
        db.add(svc)
        db.commit()
        db.refresh(svc)
        return svc

    @staticmethod
    def get_services(db: Session, vendor_id: str) -> List[VendorServiceModel]:
        """Get all services for a vendor (public)."""
        if isinstance(vendor_id, str):
            vendor_id = UUID(vendor_id)
        return (
            db.query(VendorServiceModel)
            .filter(VendorServiceModel.vendor_id == vendor_id)
            .order_by(VendorServiceModel.created_at)
            .all()
        )

    # ------------------------------------------------------------------
    # Save / unsave
    # ------------------------------------------------------------------

    @staticmethod
    def _verify_event_ownership(db: Session, event_id, user_id: str) -> Event:
        if isinstance(event_id, str):
            try:
                event_id = UUID(event_id)
            except ValueError:
                raise NotFoundError("Event", str(event_id))

        event = db.query(Event).filter(
            Event.id == event_id,
            Event.deleted_at.is_(None),
        ).first()

        if not event:
            raise NotFoundError("Event", str(event_id))
        if event.user_id != user_id:
            raise AuthorizationError("You don't have permission to manage vendors for this event")
        return event

    @staticmethod
    def save_vendor(
        db: Session,
        event_id: str,
        user_id: str,
        payload: SaveVendorRequest,
    ) -> SavedVendor:
        """Save a vendor to an event shortlist."""
        event = VendorService._verify_event_ownership(db, event_id, user_id)

        # Verify vendor exists
        vendor_uuid = payload.vendor_id if isinstance(payload.vendor_id, UUID) else UUID(str(payload.vendor_id))
        vendor = db.query(Vendor).filter(
            Vendor.id == vendor_uuid,
            Vendor.deleted_at.is_(None),
        ).first()
        if not vendor:
            raise NotFoundError("Vendor", str(payload.vendor_id))

        # Check duplicate
        existing = db.query(SavedVendor).filter(
            SavedVendor.event_id == event.id,
            SavedVendor.vendor_id == vendor_uuid,
        ).first()
        if existing:
            raise ConflictError("Vendor is already saved for this event")

        saved = SavedVendor(
            event_id=event.id,
            vendor_id=vendor_uuid,
            user_id=user_id,
            notes=payload.notes,
        )
        db.add(saved)
        db.commit()
        db.refresh(saved)
        return saved

    @staticmethod
    def get_saved_vendors(
        db: Session,
        event_id: str,
        user_id: str,
    ) -> List[SavedVendor]:
        """Return all saved vendors for an event."""
        event = VendorService._verify_event_ownership(db, event_id, user_id)
        return (
            db.query(SavedVendor)
            .filter(SavedVendor.event_id == event.id)
            .order_by(SavedVendor.created_at.desc())
            .all()
        )

    @staticmethod
    def unsave_vendor(db: Session, event_id: str, vendor_id: str, user_id: str) -> None:
        """Remove a vendor from an event's shortlist."""
        event = VendorService._verify_event_ownership(db, event_id, user_id)

        if isinstance(vendor_id, str):
            vendor_id = UUID(vendor_id)

        saved = db.query(SavedVendor).filter(
            SavedVendor.event_id == event.id,
            SavedVendor.vendor_id == vendor_id,
        ).first()

        if not saved:
            raise NotFoundError("SavedVendor", str(vendor_id))

        db.delete(saved)
        db.commit()

    # ------------------------------------------------------------------
    # Compare
    # ------------------------------------------------------------------

    @staticmethod
    def compare_vendors(
        db: Session,
        event_id: str,
        user_id: str,
        vendor_ids: List[UUID],
    ) -> Dict:
        """
        Return side-by-side comparison data for up to 4 vendors.
        The vendor with the highest match score is recommended.
        """
        event = VendorService._verify_event_ownership(db, event_id, user_id)

        vendors: List[Vendor] = []
        for vid in vendor_ids:
            v = db.query(Vendor).filter(
                Vendor.id == vid,
                Vendor.deleted_at.is_(None),
            ).first()
            if not v:
                raise NotFoundError("Vendor", str(vid))
            vendors.append(v)

        event_budget = float(event.budget) if event.budget else None
        event_location = event.location
        event_type = event.event_type.value if hasattr(event.event_type, "value") else str(event.event_type)

        compare_items: List[VendorCompareItem] = []
        for v in vendors:
            score, reason = _compute_match_score(v, event_budget, event_location, event_type)
            supported = (
                v.supported_event_types.split(",") if v.supported_event_types else []
            )
            compare_items.append(
                VendorCompareItem(
                    id=v.id,
                    business_name=v.business_name,
                    category=v.category,
                    location=v.location,
                    starting_price=float(v.starting_price) if v.starting_price is not None else None,
                    currency=v.currency,
                    rating=float(v.rating or 0),
                    review_count=v.review_count or 0,
                    verified=v.verified,
                    primary_image_url=v.primary_image_url,
                    description=v.description,
                    services=[s for s in v.services],
                    match_score=score,
                    match_reason=reason,
                )
            )

        # Sort by score to find recommendation
        sorted_items = sorted(compare_items, key=lambda x: x.match_score, reverse=True)
        recommended = sorted_items[0] if sorted_items else None

        return {
            "vendors": compare_items,
            "recommended_vendor_id": recommended.id if recommended else None,
            "recommendation_reason": recommended.match_reason if recommended else "",
        }
