"""
Security utilities including JWT token handling and Supabase auth verification.
"""

from datetime import datetime, timedelta
from typing import Optional, Dict, Any
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

try:
    from jose import ExpiredSignatureError, JWTError, jwt
except ModuleNotFoundError:
    import jwt  # type: ignore[no-redef]

    ExpiredSignatureError = jwt.ExpiredSignatureError
    JWTError = jwt.InvalidTokenError

from app.core.config import settings

security = HTTPBearer()


def create_access_token(
    data: Dict[str, Any], expires_delta: Optional[timedelta] = None
) -> str:
    """
    Create a JWT access token.

    Args:
        data: Dictionary containing token payload
        expires_delta: Optional timedelta for token expiration

    Returns:
        Encoded JWT token
    """
    to_encode = data.copy()

    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(hours=settings.JWT_EXPIRATION_HOURS)

    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(
        to_encode,
        settings.SECRET_KEY,
        algorithm=settings.JWT_ALGORITHM
    )
    return encoded_jwt


def verify_token(token: str) -> Dict[str, Any]:
    """
    Verify and decode JWT token.

    Args:
        token: JWT token to verify

    Returns:
        Decoded token payload

    Raises:
        HTTPException: If token is invalid or expired
    """
    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.JWT_ALGORITHM]
        )
        return payload
    except ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has expired",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication token",
            headers={"WWW-Authenticate": "Bearer"},
        )


def verify_supabase_token(token: str) -> Dict[str, Any]:
    """
    Verify Supabase JWT token.

    In production, this should verify against Supabase's JWT secret.
    For now, it performs basic JWT validation.

    Args:
        token: Supabase JWT token

    Returns:
        Decoded token payload

    Raises:
        HTTPException: If token is invalid
    """
    try:
        # In a real app, you'd verify against Supabase's public key
        # For now, we decode and validate the structure
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.JWT_ALGORITHM],
            options={
                "verify_signature": False,  # For local development only.
                "verify_aud": False,
            },
        )

        # Verify required claims
        if "sub" not in payload:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token: missing user ID",
            )

        return payload
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication token",
        )


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
) -> Dict[str, Any]:
    """
    Dependency to verify JWT token and get current user.

    Usage in route: async def my_route(user: Dict = Depends(get_current_user))

    Args:
        credentials: HTTP Bearer credentials from request header

    Returns:
        Decoded JWT payload containing user info

    Raises:
        HTTPException: If token is invalid or missing
    """
    token = credentials.credentials

    try:
        payload = verify_supabase_token(token)
        user_id: str = payload.get("sub")
        if user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )
        return payload
    except HTTPException:
        raise


async def get_current_user_id(
    user: Dict[str, Any] = Depends(get_current_user),
) -> str:
    """
    Get current user's ID from token.

    Usage in route: async def my_route(user_id: str = Depends(get_current_user_id))

    Args:
        user: Current user dict from get_current_user

    Returns:
        User ID (sub claim from JWT)
    """
    return user.get("sub")


async def get_current_user_email(
    user: Dict[str, Any] = Depends(get_current_user),
) -> str:
    """
    Get current user's email from token.

    Usage in route: async def my_route(email: str = Depends(get_current_user_email))

    Args:
        user: Current user dict from get_current_user

    Returns:
        User email from JWT claims
    """
    return user.get("email", "")
