# app/api/deps.py
# ---------------
# Dependency Injection utilities for FastAPI controllers.

from app.db.firestore import db

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
