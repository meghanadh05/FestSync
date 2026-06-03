"""Authentication API routes."""

from fastapi import APIRouter

router = APIRouter()


@router.post("/login")
async def login(email: str, password: str):
    """Login endpoint - to be implemented."""
    pass


@router.post("/signup")
async def signup(email: str, password: str, full_name: str):
    """Signup endpoint - to be implemented."""
    pass


@router.post("/logout")
async def logout():
    """Logout endpoint - to be implemented."""
    pass
