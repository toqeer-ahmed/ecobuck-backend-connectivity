# simulator/config.py
# -------------------
# Target parameters for mock device simulation client.

# Target ingestion server endpoint details
INGESTION_URL = "http://127.0.0.1:8000/api/v1/telemetry"

# Device registry simulation credentials
DEVICE_ID = "ecobuck-dev-001"
DEVICE_TOKEN = "valid-token"

# Sim loop upload intervals
INTERVAL_SECONDS = 5  # Accelerated step interval for developer testing (normally 300)
