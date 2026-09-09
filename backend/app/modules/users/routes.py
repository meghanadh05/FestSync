"""Users API routes."""

from fastapi import APIRouter

router = APIRouter()


@router.get("/me")
async def get_current_user():
    """Get current user profile - to be implemented."""
    pass


@router.patch("/me")
async def update_profile():
    """Update user profile - to be implemented."""
    pass


@router.get("/{user_id}")
async def get_user(user_id: str):
    """Get user details - to be implemented."""
    pass
