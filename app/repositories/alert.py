from typing import Dict, Any, List, Optional
from datetime import datetime
from app.repositories.base import BaseRepository


class AlertRepository(BaseRepository):
    """Encapsulates transactions on the `/devices/{id}/alerts` subcollection."""

    def create_alert(self, device_id: str, alert_type: str, message: str) -> Dict[str, Any]:
        """Creates a new active warning alert record."""
        alert_data = {
            "alert_type": alert_type,
            "message": message,
            "resolved": False,
            "triggered_at": datetime.utcnow(),
            "resolved_at": None,
        }
        _, ref = (
            self.db.collection("devices")
            .document(device_id)
            .collection("alerts")
            .add(alert_data)
        )
        alert_data["alert_id"] = ref.id
        alert_data["device_id"] = device_id
        return alert_data

    def list_alerts(self, device_id: str, resolved: Optional[bool] = None) -> List[Dict[str, Any]]:
        """Lists warnings matching resolution filter sorted by triggered_at descending."""
        query = (
            self.db.collection("devices")
            .document(device_id)
            .collection("alerts")
        )
        if resolved is not None:
            query = query.where("resolved", "==", resolved)

        docs = query.order_by("triggered_at", "desc").get()
        results = []
        for doc in docs:
            data = doc.to_dict()
            data["alert_id"] = doc.id
            data["device_id"] = device_id
            results.append(data)
        return results

    def resolve_alert(self, device_id: str, alert_id: str) -> Optional[Dict[str, Any]]:
        """Acknowledges and marks an alert as resolved in the database."""
        alert_ref = (
            self.db.collection("devices")
            .document(device_id)
            .collection("alerts")
            .document(alert_id)
        )
        doc = alert_ref.get()
        if doc.exists:
            resolved_at = datetime.utcnow()
            alert_ref.update({
                "resolved": True,
                "resolved_at": resolved_at
            })
            return {
                "alert_id": alert_id,
                "resolved": True,
                "resolved_at": resolved_at
            }
        return None
