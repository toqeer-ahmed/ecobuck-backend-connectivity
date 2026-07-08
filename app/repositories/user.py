from typing import Optional, Dict, Any
from datetime import datetime
from app.repositories.base import BaseRepository


class UserRepository(BaseRepository):
    """Encapsulates transactional operations on the root `/users` collection."""

    def get_by_id(self, user_id: str) -> Optional[Dict[str, Any]]:
        """Retrieves user profile by Firebase Auth UID."""
        doc = self.db.collection("users").document(user_id).get()
        if doc.exists:
            data = doc.to_dict()
            data["id"] = doc.id
            return data
        return None

    def get_by_email(self, email: str) -> Optional[Dict[str, Any]]:
        """Retrieves user profile by registered email."""
        docs = self.db.collection("users").where("email", "==", email.lower()).limit(1).get()
        for doc in docs:
            data = doc.to_dict()
            data["id"] = doc.id
            return data
        return None

    def create_user(
        self, user_id: str, email: str, display_name: str, password_hash: str
    ) -> Dict[str, Any]:
        """Creates user profile document linked to Auth credentials."""
        user_data = {
            "email": email.lower(),
            "displayName": display_name,
            "passwordHash": password_hash,
            "deviceIds": [],
            "fcmTokens": [],
            "createdAt": datetime.utcnow(),
            "updatedAt": datetime.utcnow(),
        }
        self.db.collection("users").document(user_id).set(user_data)
        user_data["id"] = user_id
        return user_data

    def register_fcm_token(self, user_id: str, fcm_token: str) -> None:
        """Appends FCM token list for user notifications routing."""
        user_ref = self.db.collection("users").document(user_id)
        doc = user_ref.get()
        if doc.exists:
            current_tokens = doc.to_dict().get("fcmTokens", [])
            if fcm_token not in current_tokens:
                current_tokens.append(fcm_token)
                user_ref.update({"fcmTokens": current_tokens, "updatedAt": datetime.utcnow()})
