"""Core application modules."""

from app.core.config import settings
from app.core.database import SessionLocal, Base, get_db, init_db, close_db
from app.core.security import (
    get_current_user,
    get_current_user_id,
    get_current_user_email,
    create_access_token,
    verify_token,
)
from app.core.exceptions import (
    FestSyncException,
    NotFoundError,
    ValidationError,
    AuthenticationError,
    AuthorizationError,
    ConflictError,
    DatabaseError,
    ExternalServiceError,
    BadRequestError,
)

__all__ = [
    "settings",
    "SessionLocal",
    "Base",
    "get_db",
    "init_db",
    "close_db",
    "get_current_user",
    "get_current_user_id",
    "get_current_user_email",
    "create_access_token",
    "verify_token",
    "FestSyncException",
    "NotFoundError",
    "ValidationError",
    "AuthenticationError",
    "AuthorizationError",
    "ConflictError",
    "DatabaseError",
    "ExternalServiceError",
    "BadRequestError",
]
