import uuid
import logging
from fastapi import Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException

logger = logging.getLogger(__name__)

# -------------------------------------------------------
# Custom App Exceptions
# -------------------------------------------------------
class AppException(Exception):
    """Base class for custom app exceptions"""
    def __init__(self, error_code: str, message: str, details: dict = None):
        self.error_code = error_code
        self.message = message
        self.details = details or {}
        super().__init__(message)


class UserNotFoundException(AppException):
    def __init__(self, user_id: int):
        super().__init__(
            error_code="USER_NOT_FOUND",
            message=f"User with id {user_id} not found",
            details={"user_id": user_id}
        )


class UnauthorizedException(AppException):
    def __init__(self):
        super().__init__(
            error_code="UNAUTHORIZED",
            message="You are not authorized to perform this action"
        )

# -------------------------------------------------------
# Exception Handlers
# -------------------------------------------------------
async def app_exception_handler(request: Request, exc: AppException):
    trace_id = str(uuid.uuid4())
    logger.error(f"[{trace_id}] {exc.error_code}: {exc.message} | Details: {exc.details}")
    return JSONResponse(
        status_code=400,
        content={
            "error_code": exc.error_code,
            "message": exc.message,
            "details": exc.details,
            "trace_id": trace_id
        }
    )


async def http_exception_handler(request: Request, exc: StarletteHTTPException):
    trace_id = str(uuid.uuid4())
    logger.warning(f"[{trace_id}] HTTP {exc.status_code}: {exc.detail}")
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error_code": "HTTP_ERROR",
            "message": exc.detail,
            "details": {},
            "trace_id": trace_id
        }
    )

async def validation_exception_handler(request: Request, exc: RequestValidationError):
    trace_id = str(uuid.uuid4())
    logger.warning(f"[{trace_id}] Validation error: {exc.errors()}")
    return JSONResponse(
        status_code=422,
        content={
            "error_code": "VALIDATION_ERROR",
            "message": "Invalid request data",
            "details": exc.errors(),
            "trace_id": trace_id
        }
    )

async def global_exception_handler(request: Request, exc: Exception):
    trace_id = str(uuid.uuid4())
    logger.exception(f"[{trace_id}] Unexpected error: {exc}")
    return JSONResponse(
        status_code=500,
        content={
            "error_code": "INTERNAL_SERVER_ERROR",
            "message": "An unexpected error occurred",
            "details": {},
            "trace_id": trace_id
        }
    )
