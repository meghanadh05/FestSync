"""
FastAPI application entry point for FestSync.
"""

from contextlib import asynccontextmanager
from fastapi import FastAPI, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.core.config import settings
from app.core.database import init_db, close_db, database_health_check
from app.api.v1.routes import router as api_v1_router


# Lifespan context manager for startup/shutdown
@asynccontextmanager
async def lifespan(app: FastAPI):
    """Handle startup and shutdown events."""
    # Startup
    print("🚀 Starting FestSync API...")
    await init_db()
    yield
    # Shutdown
    print("🛑 Shutting down FestSync API...")
    await close_db()


# Create FastAPI app
app = FastAPI(
    title=settings.API_TITLE,
    description=settings.API_DESCRIPTION,
    version=settings.API_VERSION,
    debug=settings.DEBUG,
    lifespan=lifespan,
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins_list,
    allow_credentials=settings.ALLOWED_CREDENTIALS,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Health check endpoints
@app.get("/health", status_code=status.HTTP_200_OK)
async def health_check():
    """
    Basic health check endpoint.

    Returns:
        Health status of the API
    """
    return {
        "status": "healthy",
        "service": "FestSync API",
        "version": settings.API_VERSION,
        "environment": settings.ENVIRONMENT,
    }


@app.get("/health/db", status_code=status.HTTP_200_OK)
async def database_health():
    """
    Database health check endpoint.

    Returns:
        Database connection status
    """
    db_healthy = database_health_check()

    if not db_healthy:
        return JSONResponse(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            content={
                "status": "unhealthy",
                "service": "FestSync API Database",
                "message": "Database connection failed",
            },
        )

    return {
        "status": "healthy",
        "service": "FestSync API Database",
        "database": "PostgreSQL",
    }


@app.get("/", status_code=status.HTTP_200_OK)
async def root():
    """
    Root endpoint with API information.

    Returns:
        API information and available endpoints
    """
    return {
        "message": "Welcome to FestSync API",
        "version": settings.API_VERSION,
        "docs": "/docs",
        "endpoints": {
            "health": "/health",
            "database": "/health/db",
            "api_v1": "/api/v1",
        },
    }


# Include API v1 routes
app.include_router(api_v1_router, prefix="/api/v1", tags=["v1"])


# Exception handlers
@app.exception_handler(Exception)
async def general_exception_handler(request, exc):
    """Handle unexpected exceptions."""
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "detail": "Internal server error",
            "message": str(exc) if settings.DEBUG else "An error occurred",
        },
    )


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.DEBUG,
        log_level=settings.LOG_LEVEL.lower(),
    )
