"""
Database configuration and session management.
"""

from sqlalchemy import create_engine, event
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.pool import NullPool

from app.core.config import settings

# Create SQLAlchemy engine
engine = create_engine(
    settings.DATABASE_URL,
    echo=settings.DEBUG,
    pool_pre_ping=True,
    poolclass=NullPool if settings.is_production else None,
)

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
