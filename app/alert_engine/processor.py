import logging
from app.repositories.alert import AlertRepository
from app.services.notification import notification_service
from app.alert_engine.rules import (
    evaluate_temperature_bounds,
    evaluate_humidity_bounds,
    evaluate_hardware_flags,
    evaluate_state_transitions,
)

logger = logging.getLogger("ecobuck-alert-engine")


def evaluate_telemetry(payload: dict) -> None:
    """
    Main evaluation pipeline running inline inside FastAPI background tasks.
    Scans temp, moisture, quality, and status variables. If warnings trigger,
    saves the alert to database and invokes FCM notification services.
    """
    device_id = payload.get("device_id")
    readings = payload.get("readings", {})
    temp_val = readings.get("temperature_c", {}).get("filtered")
    humidity_val = readings.get("humidity_pct", {}).get("raw")
    quality_flag = payload.get("quality_flag")
    status = payload.get("status")

    alert_repo = AlertRepository()

    # 1. Temperature Hazard Check
    if temp_val is not None:
        is_alert, msg = evaluate_temperature_bounds(temp_val)
        if is_alert:
            _trigger_alert_flow(device_id, "temp_extreme", msg, alert_repo)

    # 2. Moisture Extremes Check
    if humidity_val is not None:
        is_alert, msg = evaluate_humidity_bounds(humidity_val)
        if is_alert:
            _trigger_alert_flow(device_id, "moisture_extreme", msg, alert_repo)

    # 3. Hardware Failures Check
    if quality_flag:
        is_alert, msg = evaluate_hardware_flags(quality_flag)
        if is_alert:
            _trigger_alert_flow(device_id, "sensor_error", msg, alert_repo)

    # 4. FSM Status Check
    if status:
        is_alert, msg = evaluate_state_transitions(status)
        if is_alert:
            alert_type = (
                "ready_candidate"
                if status == "ready_candidate"
                else "needs_attention"
            )
            _trigger_alert_flow(device_id, alert_type, msg, alert_repo)


def _trigger_alert_flow(
    device_id: str, alert_type: str, message: str, repo: AlertRepository
) -> None:
    """Helper method to log warning records and trigger FCM notifications."""
    logger.warning(f"ALERT DETECTED [device={device_id} type={alert_type}]: {message}")

    # Check if duplicate active alert exists to prevent alert duplication spam
    active_alerts = repo.list_alerts(device_id, resolved=False)
    for alert in active_alerts:
        if alert["alert_type"] == alert_type:
            logger.info("Active alert of this type already exists. Skipping notification.")
            return

    # Write alert record
    repo.create_alert(device_id, alert_type, message)

    # Dispatch notification via FCM services
    notification_service.send_push_notification(
        user_id="device-owner-id",  # Resolves dynamically in production
        title="EcoBuck Environmental Alert" if alert_type != "ready_candidate" else "Compost Ready!",
        message=message,
    )
