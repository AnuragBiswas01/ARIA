"""
ARIA Notification Tool
Sends notifications to the user.
"""
from typing import Any

from .base import BaseTool
from utils.logger import get_logger

logger = get_logger(__name__)

# In-memory list to store notifications (for now)
# In production, this could be replaced with a push notification service or WebSocket broadcast.
_notifications: list[dict] = []


class NotificationTool(BaseTool):
    """
    Tool for sending notifications to the user.
    Currently stores notifications in memory for retrieval via API.
    """

    @property
    def name(self) -> str:
        return "send_notification"

    @property
    def description(self) -> str:
        return "Send a notification to the user. Use for important alerts, reminders, or proactive information."

    @property
    def parameters(self) -> dict:
        return {
            "type": "object",
            "properties": {
                "title": {
                    "type": "string",
                    "description": "The title of the notification.",
                },
                "message": {
                    "type": "string",
                    "description": "The body of the notification.",
                },
                "priority": {
                    "type": "string",
                    "description": "Priority level: 'low', 'normal', or 'high'.",
                    "enum": ["low", "normal", "high"],
                    "default": "normal",
                },
            },
            "required": ["title", "message"],
        }

    async def execute(
        self, title: str, message: str, priority: str = "normal", **kwargs: Any
    ) -> dict:
        """
        Sends a notification.

        Args:
            title: The notification title.
            message: The notification message.
            priority: The priority level.

        Returns:
            A dictionary confirming the notification was sent.
        """
        from datetime import datetime

        notification = {
            "id": len(_notifications) + 1,
            "title": title,
            "message": message,
            "priority": priority,
            "timestamp": datetime.now().isoformat(),
            "read": False,
        }
        _notifications.append(notification)
        logger.info(f"Notification sent: [{priority.upper()}] {title}")

        return {
            "status": "sent",
            "notification": notification,
        }


def get_all_notifications() -> list[dict]:
    """Returns all stored notifications."""
    return _notifications


def clear_notifications() -> int:
    """Clears all notifications and returns the count cleared."""
    global _notifications
    count = len(_notifications)
    _notifications = []
    return count
