"""
Custom exception classes for the chess game application.

This module provides a hierarchy of custom exceptions that can be used
throughout the application to provide meaningful error messages and
consistent error handling.
"""

from typing import Any, Dict, Optional


class ChessGameError(Exception):
    """
    Base exception class for all chess game related errors.

    This serves as the foundation for all custom exceptions in the application,
    providing a common interface for error handling and logging.
    """

    def __init__(
        self,
        message: str,
        error_code: Optional[str] = None,
        details: Optional[Dict[str, Any]] = None,
        status_code: int = 500,
    ):
        """
        Initialize the exception with message and optional metadata.

        Args:
            message: Human-readable error message
            error_code: Unique error code for programmatic handling
            details: Additional error details for debugging
            status_code: HTTP status code for API responses
        """
        super().__init__(message)
        self.message = message
        self.error_code = error_code
        self.details = details or {}
        self.status_code = status_code

    def to_dict(self) -> Dict[str, Any]:
        """
        Convert exception to dictionary for API responses.

        Returns:
            Dictionary representation of the exception
        """
        return {
            "error": True,
            "message": self.message,
            "error_code": self.error_code,
            "details": self.details,
            "status_code": self.status_code,
        }


class GameStateError(ChessGameError):
    """Raised when there's an issue with the game state."""

    def __init__(self, message: str, details: Optional[Dict[str, Any]] = None):
        super().__init__(
            message=message,
            error_code="GAME_STATE_ERROR",
            details=details,
            status_code=400,
        )


class InvalidMoveError(ChessGameError):
    """Raised when an invalid move is attempted."""

    def __init__(
        self,
        message: str,
        from_pos: str,
        to_pos: str,
        details: Optional[Dict[str, Any]] = None,
    ):
        move_details = {"from_pos": from_pos, "to_pos": to_pos, **(details or {})}
        super().__init__(
            message=message,
            error_code="INVALID_MOVE",
            details=move_details,
            status_code=400,
        )


class GameOverError(ChessGameError):
    """Raised when attempting to make a move on a finished game."""

    def __init__(
        self,
        message: str = "Game is over. No more moves allowed.",
        details: Optional[Dict[str, Any]] = None,
    ):
        super().__init__(
            message=message, error_code="GAME_OVER", details=details, status_code=409
        )


class InvalidPositionError(ChessGameError):
    """Raised when an invalid position is provided."""

    def __init__(self, position: str, details: Optional[Dict[str, Any]] = None):
        pos_details = {"position": position, **(details or {})}
        super().__init__(
            message=f"Invalid position: {position}",
            error_code="INVALID_POSITION",
            details=pos_details,
            status_code=400,
        )


class AIServiceError(ChessGameError):
    """Raised when there's an issue with the AI service."""

    def __init__(self, message: str, details: Optional[Dict[str, Any]] = None):
        super().__init__(
            message=message,
            error_code="AI_SERVICE_ERROR",
            details=details,
            status_code=503,
        )


class APIKeyError(ChessGameError):
    """Raised when API key is missing or invalid."""

    def __init__(self, service: str, details: Optional[Dict[str, Any]] = None):
        service_details = {"service": service, **(details or {})}
        super().__init__(
            message=f"API key not configured for {service}",
            error_code="API_KEY_ERROR",
            details=service_details,
            status_code=503,
        )


class RateLimitError(ChessGameError):
    """Raised when API rate limit is exceeded."""

    def __init__(
        self,
        service: str,
        retry_after: Optional[int] = None,
        details: Optional[Dict[str, Any]] = None,
    ):
        rate_details = {
            "service": service,
            "retry_after": retry_after,
            **(details or {}),
        }
        super().__init__(
            message=f"Rate limit exceeded for {service}",
            error_code="RATE_LIMIT_ERROR",
            details=rate_details,
            status_code=429,
        )


class ValidationError(ChessGameError):
    """Raised when input validation fails."""

    def __init__(
        self,
        field: str,
        value: Any,
        reason: str,
        details: Optional[Dict[str, Any]] = None,
    ):
        validation_details = {
            "field": field,
            "value": value,
            "reason": reason,
            **(details or {}),
        }
        super().__init__(
            message=f"Validation error for {field}: {reason}",
            error_code="VALIDATION_ERROR",
            details=validation_details,
            status_code=400,
        )


class ConfigurationError(ChessGameError):
    """Raised when there's a configuration issue."""

    def __init__(self, message: str, details: Optional[Dict[str, Any]] = None):
        super().__init__(
            message=message,
            error_code="CONFIGURATION_ERROR",
            details=details,
            status_code=500,
        )


class DatabaseError(ChessGameError):
    """Raised when there's a database operation error."""

    def __init__(
        self, message: str, operation: str, details: Optional[Dict[str, Any]] = None
    ):
        db_details = {"operation": operation, **(details or {})}
        super().__init__(
            message=message,
            error_code="DATABASE_ERROR",
            details=db_details,
            status_code=500,
        )
