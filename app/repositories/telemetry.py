from typing import Dict, Any, List
from app.repositories.base import BaseRepository


class TelemetryRepository(BaseRepository):
    """Encapsulates time-series writes and query ranges under the `/devices/{id}/telemetry` subcollection."""

    def add_telemetry_reading(self, device_id: str, payload: Dict[str, Any]) -> None:
        """Stores a telemetry data point under the target device subcollection."""
        (
            self.db.collection("devices")
            .document(device_id)
            .collection("telemetry")
            .add(payload)
        )

    def get_history(
        self, device_id: str, start_timestamp: int, end_timestamp: int
    ) -> List[Dict[str, Any]]:
        """
        Retrieves historical telemetry logs filtered by timestamp boundaries,
        ordered by timestamp descending.
        """
        docs = (
            self.db.collection("devices")
            .document(device_id)
            .collection("telemetry")
            .where("timestamp", ">=", start_timestamp)
            .where("timestamp", "<=", end_timestamp)
            .order_by("timestamp", "desc")
            .get()
        )
        results = []
        for doc in docs:
            data = doc.to_dict()
            results.append(data)
        return results
