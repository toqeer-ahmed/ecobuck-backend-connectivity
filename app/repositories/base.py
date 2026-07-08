from app.db.firestore import db


class BaseRepository:
    """
    Abstract base repository isolating the active database connection pool.
    Inherited by concrete repositories to implement custom CRUD operators.
    """
    def __init__(self):
        self.db = db
