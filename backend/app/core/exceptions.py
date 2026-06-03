"""
Custom exception classes for FestSync API.
"""

from fastapi import HTTPException, status


class FestSyncException(HTTPException):
    """Base exception for FestSync API."""

    def __init__(
        self,
        detail: str,
        status_code: int = status.HTTP_400_BAD_REQUEST,
        headers: dict | None = None,
    ):
        super().__init__(status_code=status_code, detail=detail, headers=headers)


class NotFoundError(FestSyncException):
    """Resource not found."""

    def __init__(self, resource: str, resource_id: str | int):
        detail = f"{resource} with ID {resource_id} not found"
        super().__init__(detail=detail, status_code=status.HTTP_404_NOT_FOUND)


class ValidationError(FestSyncException):
    """Validation error."""

    def __init__(self, detail: str):
        super().__init__(detail=detail, status_code=status.HTTP_422_UNPROCESSABLE_ENTITY)


class AuthenticationError(FestSyncException):
    """Authentication failed."""

    def __init__(self, detail: str = "Authentication failed"):
        super().__init__(detail=detail, status_code=status.HTTP_401_UNAUTHORIZED)


class AuthorizationError(FestSyncException):
    """User not authorized to perform action."""

    def __init__(self, detail: str = "Not authorized to perform this action"):
        super().__init__(detail=detail, status_code=status.HTTP_403_FORBIDDEN)


class ConflictError(FestSyncException):
    """Resource already exists or conflict occurred."""

    def __init__(self, detail: str):
        super().__init__(detail=detail, status_code=status.HTTP_409_CONFLICT)


class DatabaseError(FestSyncException):
    """Database operation failed."""

    def __init__(self, detail: str = "Database operation failed"):
        super().__init__(detail=detail, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ExternalServiceError(FestSyncException):
    """External service (OpenAI, etc) call failed."""

    def __init__(self, service: str, detail: str):
        message = f"{service} service error: {detail}"
        super().__init__(
            detail=message, status_code=status.HTTP_503_SERVICE_UNAVAILABLE
        )


class BadRequestError(FestSyncException):
    """Bad request."""

    def __init__(self, detail: str):
        super().__init__(detail=detail, status_code=status.HTTP_400_BAD_REQUEST)


class UnprocessableEntityError(FestSyncException):
    """Unprocessable entity."""

    def __init__(self, detail: str):
        super().__init__(
            detail=detail, status_code=status.HTTP_422_UNPROCESSABLE_ENTITY
        )
