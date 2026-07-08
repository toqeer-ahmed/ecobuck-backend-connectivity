import os
import logging
from firebase_admin import credentials, initialize_app, firestore
from app.core.config import settings

logger = logging.getLogger("ecobuck-db")


# ------------------------------------------------------------------
# Mock DB Fallback Client for Local Prototyping
# ------------------------------------------------------------------

class MockDocument:
    def __init__(self, data=None, exists=True):
        self.exists = exists
        self._data = data or {}
        self.id = "mock-id-001"

    def to_dict(self):
        return self._data


class MockDocumentReference:
    def __init__(self, id=None):
        self.id = id or "mock-id-001"

    def get(self):
        return MockDocument(exists=False)

    def set(self, data, merge=False):
        logger.info(f"[MOCK DB WRITE] set() doc={self.id} merge={merge} payload={data}")
        return None

    def update(self, data):
        logger.info(f"[MOCK DB UPDATE] update() doc={self.id} payload={data}")
        return None

    def delete(self):
        logger.info(f"[MOCK DB DELETE] delete() doc={self.id}")
        return None

    def collection(self, name):
        return MockCollection()


class MockCollection:
    def document(self, id=None):
        return MockDocumentReference(id)

    def where(self, *args, **kwargs):
        return self

    def order_by(self, *args, **kwargs):
        return self

    def limit(self, *args, **kwargs):
        return self

    def get(self):
        logger.info("[MOCK DB QUERY] get() executed on collection query")
        return []

    def stream(self):
        logger.info("[MOCK DB STREAM] stream() executed on collection query")
        return []

    def add(self, data):
        logger.info(f"[MOCK DB WRITE] add() collection payload={data}")
        return None, MockDocumentReference()


class MockFirestoreClient:
    def collection(self, name):
        return MockCollection()


# ------------------------------------------------------------------
# Singleton Connection Initialization
# ------------------------------------------------------------------

db = None

if os.path.exists(settings.FIREBASE_CREDENTIALS_PATH):
    try:
        cred = credentials.Certificate(settings.FIREBASE_CREDENTIALS_PATH)
        initialize_app(cred)
        db = firestore.client()
        logger.info("Successfully initialized production Firestore connection singleton.")
    except Exception as e:
        logger.error(f"Error initializing real Firestore client: {e}. Falling back to mock client.")
        db = MockFirestoreClient()
else:
    logger.warning(
        f"Firebase credentials not found at '{settings.FIREBASE_CREDENTIALS_PATH}'. "
        "EcoBuck is running in MOCK DATABASE mode. Real database writes will be print-logged."
    )
    db = MockFirestoreClient()
