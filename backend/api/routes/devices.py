"""
ARIA Device Control API Routes
Endpoints for controlling smart home devices.
"""
from fastapi import APIRouter

from api.models.requests import DeviceActionRequest
from api.models.responses import DeviceActionResponse
from utils.logger import get_logger

logger = get_logger(__name__)

router = APIRouter(prefix="/devices", tags=["Devices"])


@router.post("/action", response_model=DeviceActionResponse)
async def device_action(request: DeviceActionRequest):
    """
    Perform an action on a smart home device.
    """
    from main import get_app_state
    state = get_app_state()

    result = await state.tool_executor.execute(
        "home_control",
        {
            "entity_id": request.entity_id,
            "action": request.action,
            "value": request.value,
        },
    )

    if result["success"]:
        return DeviceActionResponse(
            entity_id=request.entity_id,
            action=request.action,
            status="success",
            message=result["result"].get("message"),
        )
    else:
        return DeviceActionResponse(
            entity_id=request.entity_id,
            action=request.action,
            status="error",
            error=result.get("error"),
        )


@router.get("/list")
async def list_devices():
    """
    List all known devices.
    Note: This returns simulated data unless Home Assistant is configured.
    """
    from main import get_app_state
    state = get_app_state()

    # Return current known state
    home_state = state.context_manager.get_home_state()

    # If no devices known, return example/simulated devices
    if not home_state:
        return {
            "devices": [
                {"entity_id": "light.living_room", "name": "Living Room Light", "state": "off"},
                {"entity_id": "light.bedroom", "name": "Bedroom Light", "state": "off"},
                {"entity_id": "switch.fan", "name": "Ceiling Fan", "state": "off"},
                {"entity_id": "lock.front_door", "name": "Front Door Lock", "state": "locked"},
            ],
            "source": "simulated",
        }

    return {
        "devices": [
            {"entity_id": k, "state": v} for k, v in home_state.items()
        ],
        "source": "context",
    }
