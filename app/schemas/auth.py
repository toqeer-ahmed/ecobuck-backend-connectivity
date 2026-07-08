import re
from datetime import datetime
from pydantic import BaseModel, EmailStr, Field, field_validator


class UserRegister(BaseModel):
    """Schema for validating user registration payloads."""
    email: EmailStr
    password: str = Field(..., min_length=8)
    display_name: str = Field(..., min_length=1, max_length=100)

    @field_validator("password")
    @classmethod
    def validate_password_strength(cls, value: str) -> str:
        """
        Validates password strength: requires at least 1 uppercase letter,
        1 digit, and 1 special character.
        """
        if not re.search(r"[A-Z]", value):
            raise ValueError("Password must contain at least one uppercase letter.")
        if not re.search(r"\d", value):
            raise ValueError("Password must contain at least one digit.")
        if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", value):
            raise ValueError("Password must contain at least one special character.")
        return value


class UserLogin(BaseModel):
    """Schema for validating user login credentials."""
    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    """Schema for returning access tokens."""
    access_token: str
    token_type: str = "Bearer"
    expires_in: int
    refresh_token: str


class UserResponse(BaseModel):
    """Schema for returning user registration/profile records."""
    id: str
    email: EmailStr
    created_at: datetime
