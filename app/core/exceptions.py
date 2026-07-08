from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse


class EcoBuckException(Exception):
    """Base exception class for all domain-specific errors."""
    def __init__(self, message: str, status_code: int = 400):
        self.message = message
        self.status_code = status_code
        super().__init__(self.message)


class DeviceAccessDeniedException(EcoBuckException):
    """Raised when a user attempts to access a device they do not own."""
    def __init__(self, message: str = "Access denied to this device"):
        super().__init__(message, status_code=403)


class DeviceNotFoundException(EcoBuckException):
    """Raised when a specified hardware identifier is not registered."""
    def __init__(self, message: str = "Device not found"):
        super().__init__(message, status_code=404)


class InvalidCompostStateException(EcoBuckException):
    """Raised when state transition parameters violate state machine rules."""
    def __init__(self, message: str = "Invalid compost state transition"):
        super().__init__(message, status_code=400)


class AuthenticationException(EcoBuckException):
    """Raised when authentication credentials or device tokens are invalid."""
    def __init__(self, message: str = "Authentication failed"):
        super().__init__(message, status_code=401)


def register_exception_handlers(app: FastAPI):
    """
    Registers global exception hooks to format all custom domain errors
    into structured JSON envelopes: {"error": "...", "status_code": ...}.
    """
    @app.exception_handler(EcoBuckException)
    async def ecobuck_exception_handler(request: Request, exc: EcoBuckException):
        return JSONResponse(
            status_code=exc.status_code,
            content={
                "status": "error",
                "error": exc.message,
                "status_code": exc.status_code
            }
        )
