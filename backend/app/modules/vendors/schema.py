"""
Vendor Pydantic schemas for request/response validation.
"""

from datetime import date, datetime
from typing import Optional, List
from uuid import UUID
from pydantic import BaseModel, Field
from enum import Enum


class VendorCategoryEnum(str, Enum):
    CATERING = "CATERING"
    VENUE = "VENUE"
    PHOTOGRAPHY = "PHOTOGRAPHY"
    VIDEOGRAPHY = "VIDEOGRAPHY"
    DECORATION = "DECORATION"
    MUSIC = "MUSIC"
    DJ = "DJ"
    FLORIST = "FLORIST"
    BAKERY = "BAKERY"
    TRANSPORT = "TRANSPORT"
    MAKEUP = "MAKEUP"
    ATTIRE = "ATTIRE"
    EVENT_PLANNER = "EVENT_PLANNER"
    SECURITY = "SECURITY"
    LIGHTING = "LIGHTING"
    OTHER = "OTHER"


# ---------------------------------------------------------------------------
# Vendor Service schemas
# ---------------------------------------------------------------------------

class VendorServiceCreate(BaseModel):
    """Schema for creating a vendor service."""
    name: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = Field(None, max_length=2000)
    price: Optional[float] = Field(None, ge=0)
    unit: Optional[str] = Field(None, max_length=50)


class VendorServiceResponse(BaseModel):
    """Schema for vendor service response."""
    id: UUID
    vendor_id: UUID
    name: str
    description: Optional[str]
    price: Optional[float]
    unit: Optional[str]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


# ---------------------------------------------------------------------------
# Vendor Image schema
# ---------------------------------------------------------------------------

class VendorImageResponse(BaseModel):
    """Schema for vendor image response."""
    id: UUID
    vendor_id: UUID
    url: str
    caption: Optional[str]
    is_primary: bool

    class Config:
        from_attributes = True


# ---------------------------------------------------------------------------
# Vendor CRUD schemas
# ---------------------------------------------------------------------------

class VendorCreate(BaseModel):
    """Schema for creating a vendor profile."""
    business_name: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = Field(None, max_length=5000)
    category: VendorCategoryEnum
    location: str = Field(..., min_length=1, max_length=255)
    city: Optional[str] = Field(None, max_length=100)
    state: Optional[str] = Field(None, max_length=100)
    country: Optional[str] = Field("India", max_length=100)
    email: Optional[str] = Field(None, max_length=255)
    phone: Optional[str] = Field(None, max_length=30)
    website: Optional[str] = Field(None, max_length=500)
    starting_price: Optional[float] = Field(None, ge=0)
    currency: str = Field("INR", max_length=10)
    supported_event_types: Optional[List[str]] = Field(None, description="List of supported event types")
    primary_image_url: Optional[str] = Field(None, max_length=500)


class VendorUpdate(BaseModel):
    """Schema for updating a vendor profile."""
    business_name: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = Field(None, max_length=5000)
    category: Optional[VendorCategoryEnum] = None
    location: Optional[str] = Field(None, max_length=255)
    city: Optional[str] = Field(None, max_length=100)
    state: Optional[str] = Field(None, max_length=100)
    country: Optional[str] = Field(None, max_length=100)
    email: Optional[str] = Field(None, max_length=255)
    phone: Optional[str] = Field(None, max_length=30)
    website: Optional[str] = Field(None, max_length=500)
    starting_price: Optional[float] = Field(None, ge=0)
    currency: Optional[str] = Field(None, max_length=10)
    supported_event_types: Optional[List[str]] = None
    primary_image_url: Optional[str] = Field(None, max_length=500)
    verified: Optional[bool] = None
    active: Optional[bool] = None


class VendorResponse(BaseModel):
    """Full vendor profile response."""
    id: UUID
    owner_user_id: Optional[str]
    business_name: str
    description: Optional[str]
    category: VendorCategoryEnum
    location: str
    city: Optional[str]
    state: Optional[str]
    country: Optional[str]
    email: Optional[str]
    phone: Optional[str]
    website: Optional[str]
    starting_price: Optional[float]
    currency: str
    rating: float
    review_count: int
    verified: bool
    active: bool
    supported_event_types: Optional[List[str]]
    primary_image_url: Optional[str]
    created_at: datetime
    updated_at: datetime
    services: List[VendorServiceResponse] = Field(default_factory=list)
    images: List[VendorImageResponse] = Field(default_factory=list)

    class Config:
        from_attributes = True


# ---------------------------------------------------------------------------
# Vendor Card — lightweight response for search / marketplace listing
# ---------------------------------------------------------------------------

class VendorCard(BaseModel):
    """Lightweight vendor card returned in search results."""
    id: UUID
    business_name: str
    category: VendorCategoryEnum
    location: str
    city: Optional[str]
    starting_price: Optional[float]
    currency: str
    rating: float
    review_count: int
    verified: bool
    primary_image_url: Optional[str]
    # Match scoring
    match_score: int = Field(0, ge=0, le=100, description="Compatibility score 0-100")
    match_reason: str = Field("", description="Short human-readable match reason")

    class Config:
        from_attributes = True


# ---------------------------------------------------------------------------
# Search params
# ---------------------------------------------------------------------------

class VendorSearchParams(BaseModel):
    """Schema for vendor search query parameters."""
    category: Optional[VendorCategoryEnum] = None
    location: Optional[str] = None
    event_type: Optional[str] = None
    min_price: Optional[float] = Field(None, ge=0)
    max_price: Optional[float] = Field(None, ge=0)
    min_rating: Optional[float] = Field(None, ge=0, le=5)
    availability_date: Optional[date] = None
    verified_only: bool = False
    skip: int = Field(0, ge=0)
    limit: int = Field(12, ge=1, le=50)


class VendorSearchResponse(BaseModel):
    """Response wrapper for vendor search."""
    total: int
    skip: int
    limit: int
    items: List[VendorCard] = Field(default_factory=list)


# ---------------------------------------------------------------------------
# Save / unsave vendor
# ---------------------------------------------------------------------------

class SaveVendorRequest(BaseModel):
    """Schema for saving a vendor to an event."""
    vendor_id: UUID
    notes: Optional[str] = Field(None, max_length=2000)


class SavedVendorResponse(BaseModel):
    """Response for a saved vendor entry."""
    id: UUID
    event_id: UUID
    vendor_id: UUID
    user_id: str
    notes: Optional[str]
    created_at: datetime
    vendor: VendorCard

    class Config:
        from_attributes = True


class SavedVendorListResponse(BaseModel):
    """Response for saved vendor list."""
    total: int
    items: List[SavedVendorResponse] = Field(default_factory=list)


# ---------------------------------------------------------------------------
# Compare vendors
# ---------------------------------------------------------------------------

class CompareVendorsRequest(BaseModel):
    """Request to compare vendors."""
    vendor_ids: List[UUID] = Field(..., min_length=2, max_length=4, description="2-4 vendor IDs to compare")


class VendorCompareItem(BaseModel):
    """Single vendor comparison row."""
    id: UUID
    business_name: str
    category: VendorCategoryEnum
    location: str
    starting_price: Optional[float]
    currency: str
    rating: float
    review_count: int
    verified: bool
    primary_image_url: Optional[str]
    description: Optional[str]
    services: List[VendorServiceResponse] = Field(default_factory=list)
    match_score: int
    match_reason: str

    class Config:
        from_attributes = True


class CompareVendorsResponse(BaseModel):
    """Response for vendor comparison."""
    vendors: List[VendorCompareItem] = Field(default_factory=list)
    recommended_vendor_id: Optional[UUID] = Field(None, description="ID of the recommended vendor")
    recommendation_reason: str = Field("", description="Reason for the recommendation")
