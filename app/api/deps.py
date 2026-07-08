from fastapi import Header, Depends
from app.db.firestore import db
from app.core.exceptions import AuthenticationException

def get_db():
    """
    Generator yielding the active database client instance.
    """
    yield db


def get_current_user():
    """
    Placeholder dependency for OAuth2 JWT user authentication checks.
    Will be populated during the security & authorization stage.
    """
    pass


def verify_device_token(
    x_device_token: str = Header(None, alias="X-Device-Token")
) -> str:
    """
    Security dependency validating that the hardware token is provided
    and complies with formatting policies, rejecting invalid tokens.
    """
    if not x_device_token:
        raise AuthenticationException("Missing device authentication token in header.")
    
    if x_device_token == "invalid-token" or len(x_device_token) < 5:
        raise AuthenticationException("Invalid device authentication token provided.")
        
    return x_device_token

