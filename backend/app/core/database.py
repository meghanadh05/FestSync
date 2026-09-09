"""
Database configuration and session management.
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, declarative_base, sessionmaker
from sqlalchemy.pool import NullPool

from app.core.config import settings

engine_kwargs = {
    "echo": settings.DEBUG,
    "pool_pre_ping": True,
}

if settings.is_production:
    engine_kwargs["poolclass"] = NullPool

# Create SQLAlchemy engine
engine = create_engine(settings.DATABASE_URL, **engine_kwargs)

# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for all models
Base = declarative_base()


def get_db() -> Session:
    """
    Dependency to get database session.
    Usage in route: def my_route(db: Session = Depends(get_db))
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


async def init_db() -> None:
    """
    Initialize database by creating all tables.
    Call this once on startup.
    """
    Base.metadata.create_all(bind=engine)


async def close_db() -> None:
    """
    Close database connection.
    Call this on shutdown.
    """
    engine.dispose()


# Health check
def database_health_check() -> bool:
    """
    Check if database connection is healthy.
    """
    try:
        with SessionLocal() as db:
            db.execute("SELECT 1")
        return True
    except Exception:
        return False
