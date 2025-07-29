"""
Error handling middleware for the chess game application.

This module provides middleware and exception handlers to ensure
consistent error responses across the API.
"""

import logging
import traceback
from typing import Any, Dict, Union

from app.core.exceptions import ChessGameError
from fastapi import Request, status
from fastapi.exceptions import HTTPException, RequestValidationError
from fastapi.responses import JSONResponse
from pydantic import ValidationError as PydanticValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException

logger = logging.getLogger(__name__)


async def chess_game_exception_handler(
    request: Request, exc: ChessGameError
) -> JSONResponse:
    """
    Handle custom chess game exceptions.

    Args:
        request: The incoming request
        exc: The custom exception that was raised

    Returns:
        JSONResponse with standardized error format
    """
    logger.error(
        f"ChessGameError: {exc.message} (Code: {exc.error_code}, Status: {exc.status_code})",
        extra={
            "error_code": exc.error_code,
            "status_code": exc.status_code,
            "details": exc.details,
            "path": request.url.path,
            "method": request.method,
        },
    )

    return JSONResponse(
        status_code=exc.status_code,
        content=exc.to_dict(),
        headers={"x-error-handled": "true", "x-request-id": str(id(request))},
    )


async def http_exception_handler(request: Request, exc: HTTPException) -> JSONResponse:
    """
    Handle FastAPI HTTPExceptions and convert them to standardized format.

    Args:
        request: The incoming request
        exc: The HTTPException that was raised

    Returns:
        JSONResponse with standardized error format
    """
    logger.error(
        f"HTTPException: {exc.detail} (Status: {exc.status_code})",
        extra={
            "status_code": exc.status_code,
            "path": request.url.path,
            "method": request.method,
        },
    )

    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": True,
            "message": exc.detail,
            "error_code": f"HTTP_{exc.status_code}",
            "status_code": exc.status_code,
            "details": {},
        },
        headers={"x-error-handled": "true", "x-request-id": str(id(request))},
    )


async def not_found_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    """
    Handle 404 Not Found errors specifically.

    Args:
        request: The incoming request
        exc: The exception that was raised

    Returns:
        JSONResponse with standardized error format
    """
    logger.error(
        f"404 Not Found: {request.url.path}",
        extra={
            "status_code": 404,
            "path": request.url.path,
            "method": request.method,
        },
    )

    return JSONResponse(
        status_code=404,
        content={
            "error": True,
            "message": "Not Found",
            "error_code": "HTTP_404",
            "status_code": 404,
            "details": {"path": request.url.path, "method": request.method},
        },
        headers={"x-error-handled": "true", "x-request-id": str(id(request))},
    )


async def validation_exception_handler(
    request: Request, exc: Union[RequestValidationError, PydanticValidationError]
) -> JSONResponse:
    """
    Handle validation errors from FastAPI and Pydantic.

    Args:
        request: The incoming request
        exc: The validation exception that was raised

    Returns:
        JSONResponse with standardized error format
    """
    # Extract validation errors
    if isinstance(exc, RequestValidationError):
        errors = exc.errors()
    else:
        errors = exc.errors()

    # Format validation errors
    formatted_errors = []
    for error in errors:
        formatted_errors.append(
            {
                "field": " -> ".join(str(loc) for loc in error["loc"]),
                "message": error["msg"],
                "type": error["type"],
            }
        )

    logger.error(
        f"ValidationError: {len(errors)} validation errors",
        extra={
            "validation_errors": formatted_errors,
            "path": request.url.path,
            "method": request.method,
        },
    )

    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "error": True,
            "message": "Validation error",
            "error_code": "VALIDATION_ERROR",
            "status_code": status.HTTP_422_UNPROCESSABLE_ENTITY,
            "details": {"validation_errors": formatted_errors},
        },
        headers={"x-error-handled": "true", "x-request-id": str(id(request))},
    )


async def generic_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    """
    Handle any unhandled exceptions and provide a safe error response.

    Args:
        request: The incoming request
        exc: The unhandled exception

    Returns:
        JSONResponse with standardized error format
    """
    # Log the full exception with traceback
    logger.error(
        f"Unhandled exception: {str(exc)}",
        extra={
            "exception_type": type(exc).__name__,
            "path": request.url.path,
            "method": request.method,
            "traceback": traceback.format_exc(),
        },
        exc_info=True,
    )

    # In production, don't expose internal error details
    is_development = request.app.debug if hasattr(request.app, "debug") else False

    if is_development:
        error_details = {
            "exception_type": type(exc).__name__,
            "traceback": traceback.format_exc(),
        }
    else:
        error_details = {}

    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "error": True,
            "message": "Internal server error",
            "error_code": "INTERNAL_SERVER_ERROR",
            "status_code": status.HTTP_500_INTERNAL_SERVER_ERROR,
            "details": error_details,
        },
        headers={"x-error-handled": "true", "x-request-id": str(id(request))},
    )


def setup_error_handlers(app):
    """
    Set up all error handlers for the FastAPI application.

    Args:
        app: The FastAPI application instance
    """
    # Register custom exception handlers
    app.add_exception_handler(ChessGameError, chess_game_exception_handler)
    app.add_exception_handler(HTTPException, http_exception_handler)
    app.add_exception_handler(StarletteHTTPException, http_exception_handler)
    app.add_exception_handler(RequestValidationError, validation_exception_handler)
    app.add_exception_handler(PydanticValidationError, validation_exception_handler)
    app.add_exception_handler(Exception, generic_exception_handler)

    logger.info("Error handlers have been set up successfully")


class ErrorResponseMiddleware:
    """
    Middleware to add error response headers and logging.
    """

    def __init__(self, app):
        self.app = app

    async def __call__(self, scope, receive, send):
        if scope["type"] != "http":
            await self.app(scope, receive, send)
            return

        # Add error tracking headers
        async def send_with_headers(message):
            if message["type"] == "http.response.start":
                # Add custom headers for error tracking
                headers = message.get("headers", [])
                headers.extend(
                    [
                        (b"x-error-handled", b"true"),
                        (b"x-request-id", str(id(scope)).encode()),
                    ]
                )
                message["headers"] = headers
            await send(message)

        try:
            await self.app(scope, receive, send_with_headers)
        except Exception as e:
            # Log any unhandled exceptions in middleware
            logger.error(
                f"Middleware error: {str(e)}",
                extra={
                    "path": scope.get("path", "unknown"),
                    "method": scope.get("method", "unknown"),
                    "exception_type": type(e).__name__,
                },
                exc_info=True,
            )
            raise
