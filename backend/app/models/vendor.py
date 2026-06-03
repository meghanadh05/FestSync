"""
Vendor SQLAlchemy ORM models.
"""

from datetime import datetime
from sqlalchemy import (
    Column, String, Text, Date, DateTime, Enum,
    ForeignKey, Boolean, Integer, Float, Numeric, UniqueConstraint,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import enum
import uuid

from app.core.database import Base


class VendorCategory(str, enum.Enum):
    """Vendor category enumeration."""
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


class Vendor(Base):
    """Vendor model for storing vendor profiles."""

    __tablename__ = "vendors"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True, nullable=False)
    owner_user_id = Column(String, nullable=True, index=True)   # nullable – admins can seed vendors
    business_name = Column(String(255), nullable=False, index=True)
    description = Column(Text, nullable=True)
    category = Column(Enum(VendorCategory), nullable=False, index=True)
    location = Column(String(255), nullable=False, index=True)
    city = Column(String(100), nullable=True, index=True)
    state = Column(String(100), nullable=True)
    country = Column(String(100), nullable=True, default="India")
    email = Column(String(255), nullable=True)
    phone = Column(String(30), nullable=True)
    website = Column(String(500), nullable=True)
    # Pricing
    starting_price = Column(Numeric(12, 2), nullable=True, index=True)
    currency = Column(String(10), default="INR")
    # Ratings
    rating = Column(Float, default=0.0, index=True)
    review_count = Column(Integer, default=0)
    # Metadata
    verified = Column(Boolean, default=False, index=True)
    active = Column(Boolean, default=True, index=True)
    # Supported event types stored as comma-separated string for SQLite compat
    supported_event_types = Column(String(500), nullable=True)
    # Primary image cached here for card rendering without JOIN
    primary_image_url = Column(String(500), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    deleted_at = Column(DateTime, nullable=True)

    # Relationships
    services = relationship("VendorService", back_populates="vendor", cascade="all, delete-orphan")
    images = relationship("VendorImage", back_populates="vendor", cascade="all, delete-orphan")
    reviews = relationship("VendorReview", back_populates="vendor", cascade="all, delete-orphan")

    def __repr__(self) -> str:
        return f"<Vendor(id={self.id}, name={self.business_name})>"


class VendorService(Base):
    """Services offered by a vendor."""

    __tablename__ = "vendor_services"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True, nullable=False)
    vendor_id = Column(UUID(as_uuid=True), ForeignKey("vendors.id"), nullable=False, index=True)
    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    price = Column(Numeric(12, 2), nullable=True)
    unit = Column(String(50), nullable=True)      # "per person", "flat rate", "per hour", etc.
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    vendor = relationship("Vendor", back_populates="services")

    def __repr__(self) -> str:
        return f"<VendorService(id={self.id}, name={self.name})>"


class VendorImage(Base):
    """Portfolio images for a vendor."""

    __tablename__ = "vendor_images"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True, nullable=False)
    vendor_id = Column(UUID(as_uuid=True), ForeignKey("vendors.id"), nullable=False, index=True)
    url = Column(String(500), nullable=False)
    caption = Column(String(255), nullable=True)
    is_primary = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    vendor = relationship("Vendor", back_populates="images")

    def __repr__(self) -> str:
        return f"<VendorImage(id={self.id}, vendor_id={self.vendor_id})>"


class SavedVendor(Base):
    """Vendors saved by a user for a specific event."""

    __tablename__ = "saved_vendors"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True, nullable=False)
    event_id = Column(UUID(as_uuid=True), ForeignKey("events.id"), nullable=False, index=True)
    vendor_id = Column(UUID(as_uuid=True), ForeignKey("vendors.id"), nullable=False, index=True)
    user_id = Column(String, nullable=False, index=True)
    notes = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    __table_args__ = (
        UniqueConstraint("event_id", "vendor_id", name="uq_saved_vendor_event"),
    )

    def __repr__(self) -> str:
        return f"<SavedVendor(event_id={self.event_id}, vendor_id={self.vendor_id})>"


class VendorReview(Base):
    """Reviews and ratings for vendors."""

    __tablename__ = "vendor_reviews"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True, nullable=False)
    vendor_id = Column(UUID(as_uuid=True), ForeignKey("vendors.id"), nullable=False, index=True)
    user_id = Column(String, nullable=False, index=True)
    event_id = Column(UUID(as_uuid=True), ForeignKey("events.id"), nullable=True)
    rating = Column(Integer, nullable=False)     # 1-5
    review_text = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    vendor = relationship("Vendor", back_populates="reviews")

    def __repr__(self) -> str:
        return f"<VendorReview(id={self.id}, vendor_id={self.vendor_id}, rating={self.rating})>"
