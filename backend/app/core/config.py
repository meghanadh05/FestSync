"""
Application configuration settings using Pydantic settings.
"""

from typing import Optional
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    # Environment
    ENVIRONMENT: str = "development"
    DEBUG: bool = True

    # Database
    DATABASE_URL: str

    # Supabase
    SUPABASE_URL: str
    SUPABASE_KEY: str
    SUPABASE_SERVICE_KEY: str

    # JWT
    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRATION_HOURS: int = 24
    SECRET_KEY: str

    # CORS
    ALLOWED_ORIGINS: str = "http://localhost:3000"
    ALLOWED_CREDENTIALS: bool = True

    # API
    API_TITLE: str = "FestSync API"
    API_VERSION: str = "0.1.0"
    API_DESCRIPTION: str = "AI-powered event planning platform"

    # OpenAI/Gemini
    OPENAI_API_KEY: Optional[str] = None
    GEMINI_API_KEY: Optional[str] = None

    # Logging
    LOG_LEVEL: str = "INFO"

    class Config:
        env_file = ".env"
        case_sensitive = True

    @property
    def allowed_origins_list(self) -> list[str]:
        """Parse comma-separated origins into list."""
        return [origin.strip() for origin in self.ALLOWED_ORIGINS.split(",")]

    @property
    def is_production(self) -> bool:
        """Check if running in production."""
        return self.ENVIRONMENT == "production"


# Load settings from environment
settings = Settings()
