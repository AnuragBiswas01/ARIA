"""
ARIA Events API Routes
WebSocket and REST endpoints for home events.
"""
from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from typing import List

from api.models.requests import EventRequest
from api.models.responses import EventResponse
from utils.logger import get_logger

logger = get_logger(__name__)

router = APIRouter(prefix="/events", tags=["Events"])

# Active WebSocket connections for broadcasting events
_active_connections: List[WebSocket] = []


@router.post("", response_model=EventResponse)
async def log_event(request: EventRequest):
    """
    Log a home event (e.g., from a sensor or device).
    """
    from main import get_app_state
    state = get_app_state()

    event = await state.event_processor.process_event(
        event_type=request.event_type,
        source=request.source,
        data=request.data,
    )

    # Broadcast to connected WebSocket clients
    await _broadcast_event(event)

    return EventResponse(
        event_type=event["event_type"],
        source=event["source"],
        timestamp=event["timestamp"],
        data=event.get("data"),
    )


@router.get("/recent")
async def get_recent_events(limit: int = 20):
    """
    Get recent events.
    """
    from main import get_app_state
    state = get_app_state()

    events = state.event_processor.get_recent_events(limit=limit)
    return {"events": events, "count": len(events)}


@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """
    WebSocket endpoint for real-time event streaming.
    """
    await websocket.accept()
    _active_connections.append(websocket)
    logger.info(f"WebSocket client connected. Total: {len(_active_connections)}")

    try:
        while True:
            # Keep connection alive, handle incoming messages if needed
            data = await websocket.receive_text()
            # Could handle client commands here
            logger.debug(f"Received from WebSocket: {data}")
    except WebSocketDisconnect:
        _active_connections.remove(websocket)
        logger.info(f"WebSocket client disconnected. Remaining: {len(_active_connections)}")


async def _broadcast_event(event: dict):
    """Broadcasts an event to all connected WebSocket clients."""
    import json

    if not _active_connections:
        return

    message = json.dumps({"type": "event", "payload": event})
    for connection in _active_connections:
        try:
            await connection.send_text(message)
        except Exception as e:
            logger.error(f"Error broadcasting to WebSocket: {e}")
