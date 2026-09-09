"""
Application configuration settings using Pydantic settings.
"""

from pathlib import Path
from typing import Any, Optional

from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


BACKEND_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_SQLITE_URL = f"sqlite:///{BACKEND_ROOT / 'festsync.db'}"


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=True,
        extra="ignore",
    )

    # Environment
    ENVIRONMENT: str = "development"
    DEBUG: bool = True

    # Database
    DATABASE_URL: str = DEFAULT_SQLITE_URL

    # Supabase
    SUPABASE_URL: str = "http://localhost"
    SUPABASE_KEY: str = "dev-supabase-key"
    SUPABASE_SERVICE_KEY: str = "dev-supabase-service-key"

    # JWT
    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRATION_HOURS: int = 24
    SECRET_KEY: str = "dev-secret-key"

    # Cache / background services
    REDIS_URL: Optional[str] = None

    # CORS
    ALLOWED_ORIGINS: str = "http://localhost:3000"
    ALLOWED_CREDENTIALS: bool = True

    # API
    API_TITLE: str = "FestSync API"
    API_VERSION: str = "0.1.0"
    API_DESCRIPTION: str = "AI-powered event planning platform"

    # AI Provider — "openai" | "gemini" | "mock"
    AI_PROVIDER: str = "mock"
    OPENAI_API_KEY: Optional[str] = None
    GEMINI_API_KEY: Optional[str] = None
    OPENAI_MODEL: str = "gpt-4o-mini"
    GEMINI_MODEL: str = "gemini-1.5-flash"

    # Logging
    LOG_LEVEL: str = "INFO"

    @field_validator("DEBUG", mode="before")
    @classmethod
    def normalize_debug(cls, value: Any) -> Any:
        """Accept common deployment strings in addition to strict booleans."""
        if isinstance(value, str):
            normalized = value.strip().lower()
            if normalized in {"release", "prod", "production", "false", "0", "no", "off"}:
                return False
            if normalized in {"debug", "dev", "development", "true", "1", "yes", "on"}:
                return True
        return value

    @field_validator("DATABASE_URL", mode="before")
    @classmethod
    def default_database_url(cls, value: Any) -> str:
        """Fall back to a local SQLite database when DATABASE_URL is blank."""
        if value is None:
            return DEFAULT_SQLITE_URL
        if isinstance(value, str) and not value.strip():
            return DEFAULT_SQLITE_URL
        return value

    @property
    def allowed_origins_list(self) -> list[str]:
        """Parse comma-separated origins into list."""
        return [origin.strip() for origin in self.ALLOWED_ORIGINS.split(",")]

    @property
    def is_production(self) -> bool:
        """Check if running in production."""
        return self.ENVIRONMENT.strip().lower() in {"production", "prod", "release"}


# Load settings from environment
settings = Settings()
