"""
ARIA Home Control Tool
Controls smart home devices via Home Assistant.
"""
import httpx
from typing import Any

from .base import BaseTool
from config.settings import settings
from utils.logger import get_logger

logger = get_logger(__name__)


class HomeControlTool(BaseTool):
    """
    Tool for controlling smart home devices via Home Assistant.
    Supports turning devices on/off and setting states.
    """

    @property
    def name(self) -> str:
        return "home_control"

    @property
    def description(self) -> str:
        return "Control smart home devices. Turn lights on/off, adjust thermostats, lock doors, etc."

    @property
    def parameters(self) -> dict:
        return {
            "type": "object",
            "properties": {
                "entity_id": {
                    "type": "string",
                    "description": "The Home Assistant entity ID (e.g., 'light.living_room', 'switch.fan').",
                },
                "action": {
                    "type": "string",
                    "description": "The action to perform: 'turn_on', 'turn_off', 'toggle', or 'set'.",
                    "enum": ["turn_on", "turn_off", "toggle", "set"],
                },
                "value": {
                    "type": "string",
                    "description": "Optional value for 'set' action (e.g., brightness, temperature).",
                },
            },
            "required": ["entity_id", "action"],
        }

    async def execute(
        self, entity_id: str, action: str, value: str | None = None, **kwargs: Any
    ) -> dict:
        """
        Executes a home control action.

        Args:
            entity_id: The Home Assistant entity ID.
            action: The action to perform.
            value: Optional value for the action.

        Returns:
            A dictionary with the result of the action.
        """
        if not settings.hass_url or not settings.hass_token:
            # Simulation mode if Home Assistant is not configured
            logger.warning("Home Assistant not configured. Simulating action.")
            return {
                "entity_id": entity_id,
                "action": action,
                "value": value,
                "status": "simulated",
                "message": f"[SIMULATED] {action} on {entity_id}" + (f" with value {value}" if value else ""),
            }

        # Determine the service to call
        domain = entity_id.split(".")[0]
        service = action if action in ["turn_on", "turn_off", "toggle"] else "set_value"

        url = f"{settings.hass_url}/api/services/{domain}/{service}"
        headers = {
            "Authorization": f"Bearer {settings.hass_token}",
            "Content-Type": "application/json",
        }
        payload: dict[str, Any] = {"entity_id": entity_id}
        if value is not None:
            # Common attributes based on domain
            if domain == "light":
                payload["brightness_pct"] = int(value)
            elif domain == "climate":
                payload["temperature"] = float(value)
            else:
                payload["value"] = value

        logger.info(f"Home control: {action} on {entity_id}")

        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                response = await client.post(url, headers=headers, json=payload)
                response.raise_for_status()

            return {
                "entity_id": entity_id,
                "action": action,
                "value": value,
                "status": "success",
                "message": f"Successfully executed {action} on {entity_id}",
            }
        except httpx.RequestError as e:
            logger.error(f"Home control error: {e}")
            return {
                "entity_id": entity_id,
                "action": action,
                "status": "error",
                "error": str(e),
            }
