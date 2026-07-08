from typing import Optional, Dict, Any, List
from datetime import datetime
from app.repositories.base import BaseRepository


class DeviceRepository(BaseRepository):
    """Encapsulates transactions on the `/devices` and `/devices/{id}/latest` paths."""

    def get_by_id(self, device_id: str) -> Optional[Dict[str, Any]]:
        """Reads device profile by hardware ID key."""
        doc = self.db.collection("devices").document(device_id).get()
        if doc.exists:
            data = doc.to_dict()
            data["id"] = doc.id
            return data
        return None

    def list_by_owner(self, owner_id: str) -> List[Dict[str, Any]]:
        """Lists metadata of all devices paired to the user."""
        docs = self.db.collection("devices").where("ownerId", "==", owner_id).get()
        results = []
        for doc in docs:
            data = doc.to_dict()
            data["id"] = doc.id
            results.append(data)
        return results

    def claim_device(self, device_id: str, owner_id: str, label: str) -> Dict[str, Any]:
        """Maps an unowned device to a user profile registry."""
        device_ref = self.db.collection("devices").document(device_id)
        update_data = {
            "ownerId": owner_id,
            "label": label,
            "status": "boot_self_test",
            "lastSeen": datetime.utcnow(),
            "cycleStart": datetime.utcnow(),
        }
        device_ref.update(update_data)

        # Append device mapping inside user document
        user_ref = self.db.collection("users").document(owner_id)
        doc = user_ref.get()
        if doc.exists:
            devices_list = doc.to_dict().get("deviceIds", [])
            if device_id not in devices_list:
                devices_list.append(device_id)
                user_ref.update({"deviceIds": devices_list, "updatedAt": datetime.utcnow()})

        return {**update_data, "id": device_id}

    def update_config(self, device_id: str, config_data: Dict[str, Any]) -> Dict[str, Any]:
        """Modifies device offsets and reading frequencies in database config map."""
        device_ref = self.db.collection("devices").document(device_id)
        device_ref.update({"config": config_data})
        return config_data

    def update_status(self, device_id: str, status: str) -> None:
        """Modifies FSM status field."""
        self.db.collection("devices").document(device_id).update({
            "status": status,
            "lastSeen": datetime.utcnow()
        })

    def update_latest_status(self, device_id: str, payload: Dict[str, Any]) -> None:
        """
        Critical optimization write-duplication updates on `/latest/status`.
        Enables dashboard to read single document instead of full query scans.
        """
        status_ref = (
            self.db.collection("devices")
            .document(device_id)
            .collection("latest")
            .document("status")
        )
        status_ref.set(payload)
