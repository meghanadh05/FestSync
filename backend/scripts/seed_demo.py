"""
Demo seed script — populates the database with realistic sample data.

Usage (from backend/ directory):
    python scripts/seed_demo.py

The script is idempotent: it checks for existing data before inserting.
"""

import sys
import os
from datetime import date, timedelta, datetime
from uuid import uuid4

# Add backend root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy.orm import Session
from app.core.database import SessionLocal, Base
from app.models.event import Event, EventType, EventStatus
from app.models.task import Task, TaskStatus, TaskPriority
from app.models.budget import BudgetItem
from app.models.vendor import Vendor, VendorService as VendorServiceModel, VendorCategory

# ── Config ──────────────────────────────────────────────────────────────────

DEMO_USER_ID = "demo-user-00000000-0000-0000-0000-000000000001"

TODAY = date.today()


# ── Helpers ─────────────────────────────────────────────────────────────────

def days(n: int) -> date:
    return TODAY + timedelta(days=n)


def already_seeded(db: Session) -> bool:
    return db.query(Event).filter(Event.user_id == DEMO_USER_ID).first() is not None


# ── Seed data ────────────────────────────────────────────────────────────────

def seed_events(db: Session) -> list[Event]:
    events = [
        Event(
            id=uuid4(),
            user_id=DEMO_USER_ID,
            title="Aisha & Rohan's Wedding",
            description="A grand traditional wedding celebration with 400 guests, featuring classical music, elaborate décor, and a 3-course dinner.",
            event_type=EventType.WEDDING,
            status=EventStatus.PLANNING,
            start_date=days(62),
            end_date=days(63),
            location="The Grand Palace, Mumbai",
            estimated_guests=400,
            budget=850000,
            currency="INR",
        ),
        Event(
            id=uuid4(),
            user_id=DEMO_USER_ID,
            title="Tech Horizons Conference 2026",
            description="Annual developer conference covering AI, cloud architecture, and open-source tooling. 3 stages, 30 speakers.",
            event_type=EventType.CONFERENCE,
            status=EventStatus.ACTIVE,
            start_date=days(28),
            end_date=days(29),
            location="Bangalore International Centre",
            estimated_guests=800,
            budget=1500000,
            currency="INR",
        ),
        Event(
            id=uuid4(),
            user_id=DEMO_USER_ID,
            title="Maya's 25th Birthday Bash",
            description="Intimate rooftop birthday celebration with a photo booth, DJ, and midnight cake cutting.",
            event_type=EventType.BIRTHDAY,
            status=EventStatus.PLANNING,
            start_date=days(14),
            end_date=days(14),
            location="Sky Lounge, Pune",
            estimated_guests=60,
            budget=85000,
            currency="INR",
        ),
        Event(
            id=uuid4(),
            user_id=DEMO_USER_ID,
            title="Engagemania College Fest 2026",
            description="Annual inter-college cultural festival featuring music, dance, debate, and hackathon competitions.",
            event_type=EventType.COLLEGE_FEST,
            status=EventStatus.PLANNING,
            start_date=days(45),
            end_date=days(47),
            location="NMIMS University, Mumbai",
            estimated_guests=2000,
            budget=300000,
            currency="INR",
        ),
    ]
    for e in events:
        db.add(e)
    db.flush()
    print(f"  ✓ {len(events)} events")
    return events


def seed_tasks(db: Session, events: list[Event]) -> None:
    wedding, conference, birthday, fest = events[0], events[1], events[2], events[3]

    tasks = [
        # Wedding tasks
        Task(id=uuid4(), event_id=wedding.id, title="Book wedding venue", priority=TaskPriority.URGENT, status=TaskStatus.COMPLETED, category="Venue", due_date=days(-10)),
        Task(id=uuid4(), event_id=wedding.id, title="Finalise catering menu", priority=TaskPriority.HIGH, status=TaskStatus.IN_PROGRESS, category="Catering", due_date=days(10)),
        Task(id=uuid4(), event_id=wedding.id, title="Send digital invitations", priority=TaskPriority.HIGH, status=TaskStatus.PENDING, category="Communications", due_date=days(20)),
        Task(id=uuid4(), event_id=wedding.id, title="Hire photographer & videographer", priority=TaskPriority.HIGH, status=TaskStatus.IN_PROGRESS, category="Photography", due_date=days(15)),
        Task(id=uuid4(), event_id=wedding.id, title="Arrange floral decorations", priority=TaskPriority.MEDIUM, status=TaskStatus.PENDING, category="Decoration", due_date=days(30)),
        Task(id=uuid4(), event_id=wedding.id, title="Organise guest transport", priority=TaskPriority.MEDIUM, status=TaskStatus.PENDING, category="Logistics", due_date=days(45)),
        Task(id=uuid4(), event_id=wedding.id, title="Order wedding cake", priority=TaskPriority.MEDIUM, status=TaskStatus.PENDING, category="Catering", due_date=days(50)),
        Task(id=uuid4(), event_id=wedding.id, title="Final venue walkthrough", priority=TaskPriority.HIGH, status=TaskStatus.PENDING, category="Venue", due_date=days(58)),

        # Conference tasks
        Task(id=uuid4(), event_id=conference.id, title="Confirm keynote speakers", priority=TaskPriority.URGENT, status=TaskStatus.COMPLETED, category="Content", due_date=days(-5)),
        Task(id=uuid4(), event_id=conference.id, title="Set up registration portal", priority=TaskPriority.HIGH, status=TaskStatus.COMPLETED, category="Logistics", due_date=days(-14)),
        Task(id=uuid4(), event_id=conference.id, title="Coordinate AV team", priority=TaskPriority.HIGH, status=TaskStatus.IN_PROGRESS, category="Technical", due_date=days(5)),
        Task(id=uuid4(), event_id=conference.id, title="Prepare speaker kits", priority=TaskPriority.MEDIUM, status=TaskStatus.PENDING, category="Content", due_date=days(20)),

        # Birthday tasks
        Task(id=uuid4(), event_id=birthday.id, title="Book rooftop venue", priority=TaskPriority.URGENT, status=TaskStatus.COMPLETED, category="Venue", due_date=days(-7)),
        Task(id=uuid4(), event_id=birthday.id, title="Hire DJ", priority=TaskPriority.HIGH, status=TaskStatus.IN_PROGRESS, category="Entertainment", due_date=days(5)),
        Task(id=uuid4(), event_id=birthday.id, title="Order custom birthday cake", priority=TaskPriority.HIGH, status=TaskStatus.PENDING, category="Catering", due_date=days(10)),
        Task(id=uuid4(), event_id=birthday.id, title="Set up photo booth backdrop", priority=TaskPriority.LOW, status=TaskStatus.PENDING, category="Decoration", due_date=days(13)),

        # Fest tasks
        Task(id=uuid4(), event_id=fest.id, title="Confirm stage design", priority=TaskPriority.HIGH, status=TaskStatus.IN_PROGRESS, category="Technical", due_date=days(15)),
        Task(id=uuid4(), event_id=fest.id, title="Coordinate volunteer teams", priority=TaskPriority.MEDIUM, status=TaskStatus.PENDING, category="Logistics", due_date=days(30)),
        Task(id=uuid4(), event_id=fest.id, title="Sponsor banner printing", priority=TaskPriority.LOW, status=TaskStatus.PENDING, category="Marketing", due_date=days(38)),
    ]
    for t in tasks:
        db.add(t)
    db.flush()
    print(f"  ✓ {len(tasks)} tasks")


def seed_budget_items(db: Session, events: list[Event]) -> None:
    wedding, conference, birthday = events[0], events[1], events[2]

    items = [
        BudgetItem(id=uuid4(), event_id=wedding.id, category="Venue", planned_amount=250000, actual_amount=240000, notes="Grand Palace booking confirmed"),
        BudgetItem(id=uuid4(), event_id=wedding.id, category="Catering", planned_amount=200000, actual_amount=0, notes="Menu finalised, payment pending"),
        BudgetItem(id=uuid4(), event_id=wedding.id, category="Photography", planned_amount=80000, actual_amount=40000, notes="50% advance paid"),
        BudgetItem(id=uuid4(), event_id=wedding.id, category="Decoration", planned_amount=120000, actual_amount=0),
        BudgetItem(id=uuid4(), event_id=wedding.id, category="Music & Entertainment", planned_amount=60000, actual_amount=30000),
        BudgetItem(id=uuid4(), event_id=wedding.id, category="Transport", planned_amount=40000, actual_amount=0),

        BudgetItem(id=uuid4(), event_id=conference.id, category="Venue", planned_amount=400000, actual_amount=400000, notes="Paid in full"),
        BudgetItem(id=uuid4(), event_id=conference.id, category="AV & Technical", planned_amount=250000, actual_amount=120000),
        BudgetItem(id=uuid4(), event_id=conference.id, category="Catering", planned_amount=300000, actual_amount=0),
        BudgetItem(id=uuid4(), event_id=conference.id, category="Marketing", planned_amount=150000, actual_amount=95000),
        BudgetItem(id=uuid4(), event_id=conference.id, category="Speaker Gifts", planned_amount=60000, actual_amount=0),

        BudgetItem(id=uuid4(), event_id=birthday.id, category="Venue", planned_amount=30000, actual_amount=30000, notes="Sky Lounge deposit paid"),
        BudgetItem(id=uuid4(), event_id=birthday.id, category="DJ", planned_amount=15000, actual_amount=0),
        BudgetItem(id=uuid4(), event_id=birthday.id, category="Catering", planned_amount=25000, actual_amount=0),
        BudgetItem(id=uuid4(), event_id=birthday.id, category="Decoration", planned_amount=10000, actual_amount=8500, notes="Slightly over — added extra lights"),
    ]
    for item in items:
        db.add(item)
    db.flush()
    print(f"  ✓ {len(items)} budget items")


def seed_vendors(db: Session) -> None:
    vendor_data = [
        # Catering
        dict(business_name="Spice Route Caterers", category=VendorCategory.CATERING, location="Mumbai, Maharashtra", city="Mumbai", starting_price=450, currency="INR", rating=4.8, review_count=142, verified=True, description="Premium pan-Indian catering for 50-2000 guests. Specialises in live counters and wedding menus.", supported_event_types="WEDDING,RECEPTION,ENGAGEMENT"),
        dict(business_name="Green Bowl Events", category=VendorCategory.CATERING, location="Bangalore, Karnataka", city="Bangalore", starting_price=350, currency="INR", rating=4.6, review_count=98, verified=True, description="Sustainable, organic catering. Popular with corporate clients for healthy buffet menus."),
        dict(business_name="Rajasthani Flavours", category=VendorCategory.CATERING, location="Jaipur, Rajasthan", city="Jaipur", starting_price=280, currency="INR", rating=4.5, review_count=67, verified=False, description="Authentic Rajasthani cuisine, specialising in royal thali setups and outdoor catering."),

        # Venue
        dict(business_name="The Grand Palace", category=VendorCategory.VENUE, location="Mumbai, Maharashtra", city="Mumbai", starting_price=150000, currency="INR", rating=4.9, review_count=85, verified=True, description="Iconic 5-star banquet facility with 3 halls seating 100-500 guests. Complete decor & catering available."),
        dict(business_name="Sky Lounge Pune", category=VendorCategory.VENUE, location="Pune, Maharashtra", city="Pune", starting_price=40000, currency="INR", rating=4.7, review_count=52, verified=True, description="Trendy rooftop venue for intimate events (20-80 guests). Best for birthday parties and engagements."),
        dict(business_name="Bangalore International Centre", category=VendorCategory.VENUE, location="Bangalore, Karnataka", city="Bangalore", starting_price=200000, currency="INR", rating=4.8, review_count=112, verified=True, description="Premier conference venue with 5 break-out rooms, 1000-seat auditorium, and full AV support."),

        # Photography
        dict(business_name="Lens & Light Studio", category=VendorCategory.PHOTOGRAPHY, location="Mumbai, Maharashtra", city="Mumbai", starting_price=50000, currency="INR", rating=4.9, review_count=203, verified=True, description="Award-winning wedding photographers. Cinematic video reels and drone shots included in premium packages."),
        dict(business_name="Frames by Priya", category=VendorCategory.PHOTOGRAPHY, location="Pune, Maharashtra", city="Pune", starting_price=30000, currency="INR", rating=4.6, review_count=78, verified=False, description="Candid photography specialist. Natural light, lifestyle approach, same-day highlight reel available."),

        # Music / DJ
        dict(business_name="DJ Arjun Official", category=VendorCategory.DJ, location="Bangalore, Karnataka", city="Bangalore", starting_price=25000, currency="INR", rating=4.7, review_count=91, verified=True, description="Top-tier DJ specialising in Bollywood, EDM, and live mashups. Full sound system included."),
        dict(business_name="Mumbai Strings Orchestra", category=VendorCategory.MUSIC, location="Mumbai, Maharashtra", city="Mumbai", starting_price=80000, currency="INR", rating=4.8, review_count=44, verified=True, description="12-piece classical and fusion orchestra. Performs Bollywood, ghazals, and Western classical."),

        # Decoration
        dict(business_name="Bloom & Drape", category=VendorCategory.DECORATION, location="Mumbai, Maharashtra", city="Mumbai", starting_price=60000, currency="INR", rating=4.7, review_count=115, verified=True, description="Luxury floral décor and event styling. Signature mandap designs and photo-booth setups."),
        dict(business_name="The Décor Factory", category=VendorCategory.DECORATION, location="Delhi, Delhi", city="Delhi", starting_price=40000, currency="INR", rating=4.5, review_count=88, verified=False, description="Budget-friendly full-event décor. LED setups, balloon arches, and stage backdrops."),

        # Event Planner
        dict(business_name="Perfect Moments Co.", category=VendorCategory.EVENT_PLANNER, location="Mumbai, Maharashtra", city="Mumbai", starting_price=120000, currency="INR", rating=4.9, review_count=56, verified=True, description="End-to-end wedding and corporate event management. Team of 15 with day-of coordination included."),
    ]

    for v in vendor_data:
        vendor = Vendor(
            id=uuid4(),
            owner_user_id=None,
            business_name=v["business_name"],
            description=v.get("description"),
            category=v["category"],
            location=v["location"],
            city=v["city"],
            state=None,
            country="India",
            starting_price=v.get("starting_price"),
            currency=v.get("currency", "INR"),
            rating=v.get("rating", 0),
            review_count=v.get("review_count", 0),
            verified=v.get("verified", False),
            active=True,
            supported_event_types=v.get("supported_event_types"),
        )
        db.add(vendor)

    db.flush()
    print(f"  ✓ {len(vendor_data)} vendors")


# ── Main ─────────────────────────────────────────────────────────────────────

def seed():
    print("🌱 Seeding demo data…")
    db: Session = SessionLocal()
    try:
        if already_seeded(db):
            print("  ⚠ Demo data already exists — skipping.")
            return

        events = seed_events(db)
        seed_tasks(db, events)
        seed_budget_items(db, events)
        seed_vendors(db)

        db.commit()
        print(f"\n✅ Done! Demo user ID: {DEMO_USER_ID}")
        print("   You can now log in and see populated data.")
    except Exception as e:
        db.rollback()
        print(f"❌ Seed failed: {e}")
        raise
    finally:
        db.close()


if __name__ == "__main__":
    seed()
