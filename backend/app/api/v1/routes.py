"""
Aggregator for all API v1 routes.
"""

from fastapi import APIRouter

# Import routers from modules
from app.modules.events.routes import router as events_router

router = APIRouter()

# Include routers from different modules
router.include_router(events_router)
# router.include_router(auth_router, prefix="/auth", tags=["auth"])
# router.include_router(users_router, prefix="/users", tags=["users"])
# router.include_router(tasks_router, prefix="/tasks", tags=["tasks"])
# router.include_router(vendors_router, prefix="/vendors", tags=["vendors"])
# router.include_router(budget_router, prefix="/budget", tags=["budget"])
# router.include_router(guests_router, prefix="/guests", tags=["guests"])
# router.include_router(bookings_router, prefix="/bookings", tags=["bookings"])
# router.include_router(plans_router, prefix="/plans", tags=["plans"])
# router.include_router(ai_router, prefix="/ai", tags=["ai"])
# router.include_router(notifications_router, prefix="/notifications", tags=["notifications"])


@router.get("/status")
async def api_status():
    """
    Get API v1 status.

    Returns:
        API status information
    """
    return {
        "status": "operational",
        "version": "1.0.0",
        "message": "FestSync API v1 is running",
    }
