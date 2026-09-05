"""Standardized error envelope and exception classes for TruePixels.rgb.

Conforms strictly to Module Interface Contract v1.0 Section 3.4 and SRS F.20 / NF.7.
"""
from typing import Optional
import uuid
from fastapi import Request
from fastapi.responses import JSONResponse


class AppException(Exception):
    """Base application exception with standardized code and status code."""

    def __init__(
        self,
        code: str,
        message: str,
        status_code: int = 400,
        request_id: Optional[str] = None,
    ):
        self.code = code
        self.message = message
        self.status_code = status_code
        self.request_id = request_id or str(uuid.uuid4())
        super().__init__(message)

    def to_dict(self) -> dict:
        return {
            "error": {
                "code": self.code,
                "message": self.message,
                "request_id": self.request_id,
            }
        }


# --- M1 Auth & Access Exceptions ---
class AuthEmailTakenException(AppException):
    def __init__(self, message: str = "An account with this email already exists.", request_id: Optional[str] = None):
        super().__init__(code="AUTH_EMAIL_TAKEN", message=message, status_code=409, request_id=request_id)


class AuthInvalidCredentialsException(AppException):
    def __init__(self, message: str = "Invalid email or password.", request_id: Optional[str] = None):
        super().__init__(code="AUTH_INVALID_CREDENTIALS", message=message, status_code=401, request_id=request_id)


class AuthTokenInvalidException(AppException):
    def __init__(self, message: str = "Missing, invalid or expired session token.", request_id: Optional[str] = None):
        super().__init__(code="AUTH_TOKEN_INVALID", message=message, status_code=401, request_id=request_id)


class AuthForbiddenException(AppException):
    def __init__(self, message: str = "You do not have permission to access this resource.", request_id: Optional[str] = None):
        super().__init__(code="AUTH_FORBIDDEN", message=message, status_code=403, request_id=request_id)


class AuthAccountDisabledException(AppException):
    def __init__(self, message: str = "Account is disabled or removed.", request_id: Optional[str] = None):
        super().__init__(code="AUTH_ACCOUNT_DISABLED", message=message, status_code=403, request_id=request_id)


# --- M1 Image & Upload Exceptions ---
class ImgFormatUnsupportedException(AppException):
    def __init__(self, message: str = "Only JPG, JPEG and PNG images are accepted.", request_id: Optional[str] = None):
        super().__init__(code="IMG_FORMAT_UNSUPPORTED", message=message, status_code=415, request_id=request_id)


class ImgTooLargeException(AppException):
    def __init__(self, message: str = "File exceeds the configured maximum upload size.", request_id: Optional[str] = None):
        super().__init__(code="IMG_TOO_LARGE", message=message, status_code=413, request_id=request_id)


class ImgCorruptedException(AppException):
    def __init__(self, message: str = "Decoder could not open the file, or image is corrupted/truncated.", request_id: Optional[str] = None):
        super().__init__(code="IMG_CORRUPTED", message=message, status_code=422, request_id=request_id)


class ImgNotFoundException(AppException):
    def __init__(self, message: str = "Image does not exist or is not accessible.", request_id: Optional[str] = None):
        super().__init__(code="IMG_NOT_FOUND", message=message, status_code=404, request_id=request_id)


# --- M3 Admin Exceptions ---
class AdmActionNotPermittedException(AppException):
    def __init__(self, message: str = "Administrative action rejected by policy.", request_id: Optional[str] = None):
        super().__init__(code="ADM_ACTION_NOT_PERMITTED", message=message, status_code=409, request_id=request_id)


async def app_exception_handler(request: Request, exc: AppException) -> JSONResponse:
    """Exception handler for custom AppException."""
    return JSONResponse(status_code=exc.status_code, content=exc.to_dict())


async def global_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    """Fallback 500 handler to ensure no tracebacks or internal paths leak to users (F.20/NF.7)."""
    req_id = getattr(request.state, "request_id", str(uuid.uuid4()))
    return JSONResponse(
        status_code=500,
        content={
            "error": {
                "code": "INTERNAL_SERVER_ERROR",
                "message": "An unexpected server error occurred. Please contact administrator.",
                "request_id": str(req_id),
            }
        },
    )
