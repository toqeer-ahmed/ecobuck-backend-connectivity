# app/api/deps.py
# ---------------
# Dependency Injection utilities for FastAPI controllers.

def get_db():
    """
    Placeholder generator yielding the database client.
    Will be populated during the database/Firestore integration stage.
    """
    pass


def get_current_user():
    """
    Placeholder dependency for OAuth2 JWT user authentication checks.
    Will be populated during the security & authorization stage.
    """
    pass
