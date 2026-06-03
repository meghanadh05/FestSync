"""
Vendor API routes.
"""

from datetime import date
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import get_current_user_id
from app.core.exceptions import NotFoundError, AuthorizationError, ConflictError
from app.modules.vendors.schema import (
    VendorCreate,
    VendorUpdate,
    VendorResponse,
    VendorCard,
    VendorSearchResponse,
    VendorServiceCreate,
    VendorServiceResponse,
    SaveVendorRequest,
    SavedVendorResponse,
    SavedVendorListResponse,
    CompareVendorsRequest,
    CompareVendorsResponse,
    VendorCategoryEnum,
)
from app.modules.vendors.service import VendorService, _vendor_to_card

router = APIRouter()


# ---------------------------------------------------------------------------
# Helper — build VendorResponse from ORM object (handles list deserialization)
# ---------------------------------------------------------------------------

def _serialize_vendor(vendor) -> dict:
    """Convert ORM Vendor to dict suitable for VendorResponse."""
    supported = (
        vendor.supported_event_types.split(",")
        if vendor.supported_event_types
        else []
    )
    return {
        **{c.name: getattr(vendor, c.name) for c in vendor.__table__.columns},
        "supported_event_types": supported,
    }


# ---------------------------------------------------------------------------
# Vendor CRUD
# ---------------------------------------------------------------------------

@router.post("/vendors", status_code=201)
def create_vendor(
    vendor_data: VendorCreate,
    user_id: str = Depends(get_current_user_id),
    db: Session = Depends(get_db),
):
    """Create a new vendor profile."""
    try:
        vendor = VendorService.create_vendor(db, user_id, vendor_data)
        data = _serialize_vendor(vendor)
        data["services"] = []
        data["images"] = []
        return VendorResponse(**data)
    except (NotFoundError, AuthorizationError) as e:
        raise HTTPException(status_code=e.status_code, detail=str(e))


@router.get("/vendors/search", response_model=VendorSearchResponse)
def search_vendors(
    category: Optional[VendorCategoryEnum] = Query(None),
    location: Optional[str] = Query(None),
    event_type: Optional[str] = Query(None),
    min_price: Optional[float] = Query(None, ge=0),
    max_price: Optional[float] = Query(None, ge=0),
    min_rating: Optional[float] = Query(None, ge=0, le=5),
    availability_date: Optional[date] = Query(None),
    verified_only: bool = Query(False),
    event_budget: Optional[float] = Query(None, ge=0),
    skip: int = Query(0, ge=0),
    limit: int = Query(12, ge=1, le=50),
    db: Session = Depends(get_db),
):
    """
    Search and filter vendors.

    Accepts optional scoring context (event_budget, location, event_type)
    to rank results by match score.
    """
    total, cards = VendorService.search_vendors(
        db,
        skip=skip,
        limit=limit,
        category=category,
        location=location,
        event_type=event_type,
        min_price=min_price,
        max_price=max_price,
        min_rating=min_rating,
        availability_date=availability_date,
        verified_only=verified_only,
        event_budget=event_budget,
    )
    return VendorSearchResponse(total=total, skip=skip, limit=limit, items=cards)


@router.get("/vendors/{vendor_id}")
def get_vendor(
    vendor_id: str,
    db: Session = Depends(get_db),
):
    """Get full vendor profile (public, no auth required)."""
    try:
        vendor = VendorService.get_vendor_by_id(db, vendor_id)
        data = _serialize_vendor(vendor)
        data["services"] = list(vendor.services)
        data["images"] = list(vendor.images)
        return VendorResponse(**data)
    except NotFoundError as e:
        raise HTTPException(status_code=e.status_code, detail=str(e))


@router.patch("/vendors/{vendor_id}")
def update_vendor(
    vendor_id: str,
    vendor_data: VendorUpdate,
    user_id: str = Depends(get_current_user_id),
    db: Session = Depends(get_db),
):
    """Update a vendor profile (owner only)."""
    try:
        vendor = VendorService.update_vendor(db, vendor_id, user_id, vendor_data)
        data = _serialize_vendor(vendor)
        data["services"] = list(vendor.services)
        data["images"] = list(vendor.images)
        return VendorResponse(**data)
    except (NotFoundError, AuthorizationError) as e:
        raise HTTPException(status_code=e.status_code, detail=str(e))


# ---------------------------------------------------------------------------
# Vendor Services
# ---------------------------------------------------------------------------

@router.post("/vendors/{vendor_id}/services", response_model=VendorServiceResponse, status_code=201)
def add_vendor_service(
    vendor_id: str,
    service_data: VendorServiceCreate,
    user_id: str = Depends(get_current_user_id),
    db: Session = Depends(get_db),
):
    """Add a service offering to a vendor (owner only)."""
    try:
        svc = VendorService.add_service(db, vendor_id, user_id, service_data)
        return VendorServiceResponse.model_validate(svc)
    except (NotFoundError, AuthorizationError) as e:
        raise HTTPException(status_code=e.status_code, detail=str(e))


@router.get("/vendors/{vendor_id}/services", response_model=list[VendorServiceResponse])
def list_vendor_services(
    vendor_id: str,
    db: Session = Depends(get_db),
):
    """Get all services for a vendor (public)."""
    try:
        services = VendorService.get_services(db, vendor_id)
        return [VendorServiceResponse.model_validate(s) for s in services]
    except NotFoundError as e:
        raise HTTPException(status_code=e.status_code, detail=str(e))


# ---------------------------------------------------------------------------
# Save / unsave / compare  (event-scoped, require auth)
# ---------------------------------------------------------------------------

@router.post("/events/{event_id}/vendors/save", status_code=201)
def save_vendor_to_event(
    event_id: str,
    payload: SaveVendorRequest,
    user_id: str = Depends(get_current_user_id),
    db: Session = Depends(get_db),
):
    """Save a vendor to an event's shortlist."""
    try:
        saved = VendorService.save_vendor(db, event_id, user_id, payload)
        vendor = VendorService.get_vendor_by_id(db, str(saved.vendor_id))
        card = _vendor_to_card(vendor)
        return SavedVendorResponse(
            id=saved.id,
            event_id=saved.event_id,
            vendor_id=saved.vendor_id,
            user_id=saved.user_id,
            notes=saved.notes,
            created_at=saved.created_at,
            vendor=card,
        )
    except (NotFoundError, AuthorizationError) as e:
        raise HTTPException(status_code=e.status_code, detail=str(e))
    except ConflictError as e:
        raise HTTPException(status_code=e.status_code, detail=str(e))


@router.get("/events/{event_id}/vendors/saved", response_model=SavedVendorListResponse)
def list_saved_vendors(
    event_id: str,
    user_id: str = Depends(get_current_user_id),
    db: Session = Depends(get_db),
):
    """Get all saved vendors for an event."""
    try:
        saved_list = VendorService.get_saved_vendors(db, event_id, user_id)
        items = []
        for saved in saved_list:
            vendor = VendorService.get_vendor_by_id(db, str(saved.vendor_id))
            card = _vendor_to_card(vendor)
            items.append(
                SavedVendorResponse(
                    id=saved.id,
                    event_id=saved.event_id,
                    vendor_id=saved.vendor_id,
                    user_id=saved.user_id,
                    notes=saved.notes,
                    created_at=saved.created_at,
                    vendor=card,
                )
            )
        return SavedVendorListResponse(total=len(items), items=items)
    except (NotFoundError, AuthorizationError) as e:
        raise HTTPException(status_code=e.status_code, detail=str(e))


@router.delete("/events/{event_id}/vendors/{vendor_id}/unsave", status_code=204)
def unsave_vendor(
    event_id: str,
    vendor_id: str,
    user_id: str = Depends(get_current_user_id),
    db: Session = Depends(get_db),
):
    """Remove a vendor from an event's shortlist."""
    try:
        VendorService.unsave_vendor(db, event_id, vendor_id, user_id)
    except (NotFoundError, AuthorizationError) as e:
        raise HTTPException(status_code=e.status_code, detail=str(e))


@router.post("/events/{event_id}/vendors/compare", response_model=CompareVendorsResponse)
def compare_vendors(
    event_id: str,
    payload: CompareVendorsRequest,
    user_id: str = Depends(get_current_user_id),
    db: Session = Depends(get_db),
):
    """
    Compare 2-4 vendors side by side with match scores.

    Returns vendors in request order plus a recommended vendor.
    """
    try:
        result = VendorService.compare_vendors(db, event_id, user_id, payload.vendor_ids)
        return CompareVendorsResponse(**result)
    except (NotFoundError, AuthorizationError) as e:
        raise HTTPException(status_code=e.status_code, detail=str(e))

