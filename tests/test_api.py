from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_health_check():
    """Verifies baseline health check route."""
    r = client.get("/health")
    assert r.status_code == 200
    assert r.json()["service"] == "ecobuck-backend"


def test_telemetry_valid_ingestion():
    """Verifies that post telemetry succeeds with a valid device token."""
    payload = {
        "device_id": "test-device",
        "firmware_version": "0.1.0",
        "schema_version": 1,
        "timestamp": 1783515600,
        "readings": {
            "temperature_c": {
                "raw": 44.5,
                "filtered": 44.7,
                "trend_avg": 44.2,
                "quality": "good",
                "error": False
            },
            "humidity_pct": {
                "raw": 55.2,
                "quality": "good",
                "error": False
            }
        },
        "status": "active_composting",
        "quality_flag": "good",
        "cycle_age_days": 1.25,
        "battery_pct": 87
    }
    r = client.post(
        "/api/v1/telemetry",
        json=payload,
        headers={"X-Device-Token": "valid-token"}
    )
    assert r.status_code == 202
    assert r.json()["status"] == "success"


def test_telemetry_missing_auth():
    """Verifies that telemetry post fails with HTTP 401 when header token is missing."""
    payload = {
        "device_id": "test-device",
        "firmware_version": "0.1.0",
        "schema_version": 1,
        "timestamp": 1783515600,
        "readings": {
            "temperature_c": {
                "raw": 44.5,
                "filtered": 44.7,
                "trend_avg": 44.2,
                "quality": "good",
                "error": False
            },
            "humidity_pct": {
                "raw": 55.2,
                "quality": "good",
                "error": False
            }
        },
        "status": "active_composting",
        "quality_flag": "good",
        "cycle_age_days": 1.25,
        "battery_pct": 87
    }
    r = client.post(
        "/api/v1/telemetry",
        json=payload
    )
    assert r.status_code == 401
    assert r.json()["status"] == "error"
    assert "Missing" in r.json()["error"]


def test_telemetry_invalid_auth():
    """Verifies telemetry post fails with HTTP 401 when an invalid token is supplied."""
    payload = {
        "device_id": "test-device",
        "firmware_version": "0.1.0",
        "schema_version": 1,
        "timestamp": 1783515600,
        "readings": {
            "temperature_c": {
                "raw": 44.5,
                "filtered": 44.7,
                "trend_avg": 44.2,
                "quality": "good",
                "error": False
            },
            "humidity_pct": {
                "raw": 55.2,
                "quality": "good",
                "error": False
            }
        },
        "status": "active_composting",
        "quality_flag": "good",
        "cycle_age_days": 1.25,
        "battery_pct": 87
    }
    r = client.post(
        "/api/v1/telemetry",
        json=payload,
        headers={"X-Device-Token": "invalid-token"}
    )
    assert r.status_code == 401
    assert r.json()["status"] == "error"
    assert "Invalid" in r.json()["error"]


def test_dashboard_devices_list():
    """Verifies listing of claimed devices."""
    r = client.get("/api/v1/devices")
    assert r.status_code == 200
    assert len(r.json()) > 0
    assert r.json()[0]["device_id"] == "ecobuck-dev-001"


def test_device_manual_validation():
    """Verifies user manual checks endpoint validation."""
    r = client.post("/api/v1/devices/ecobuck-dev-001/validate")
    assert r.status_code == 200
    assert r.json()["new_status"] == "ready_confirmed"
