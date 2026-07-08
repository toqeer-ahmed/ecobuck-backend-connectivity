from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import List


class Settings(BaseSettings):
    """
    Application settings loader mapping to env variables or fallbacks.
    Loads and validates system-wide config variables using Pydantic.
    """
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore",
    )

    # Server Parameters
    DEBUG: bool = True
    PORT: int = 8000
    HOST: str = "127.0.0.1"

    # Database / Firestore
    FIREBASE_CREDENTIALS_PATH: str = "credentials/firebase_service_account.json"
    FIRESTORE_DATABASE_ID: str = "(default)"

    # Auth & Tokens
    JWT_SECRET_KEY: str = "ecobuck_very_secure_jwt_signing_secret_key_here"
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60

    # Rate Limiting & Safety Parameters
    RATE_LIMIT_PER_MINUTE: int = 60
    DEVICE_INGESTION_RATE_LIMIT: int = 2
    HEARTBEAT_TIMEOUT_SECONDS: int = 900

    # CORS Configurations
    CORS_ORIGINS: List[str] = ["*"]


# Instantiate singleton settings loader
settings = Settings()
