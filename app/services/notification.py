import logging

logger = logging.getLogger("ecobuck-notifications")


class NotificationService:
    """
    Simulates gateway communications with the Google Firebase Cloud Messaging service.
    In local prototyping, this print-logs notification payloads.
    """
    def send_push_notification(self, user_id: str, title: str, message: str) -> bool:
        logger.info(
            f"[FCM MOCK GATEWAY] Target User ID: {user_id} | "
            f"Title: '{title}' | Message: '{message}'"
        )
        return True


# Instantiate singleton push dispatcher
notification_service = NotificationService()
