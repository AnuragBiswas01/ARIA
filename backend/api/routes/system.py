"""
ARIA System API Routes
System health, status, and management endpoints.
"""
from fastapi import APIRouter
import time

from api.models.responses import SystemStatusResponse
from utils.logger import get_logger

logger = get_logger(__name__)

router = APIRouter(prefix="/system", tags=["System"])

# Track server start time
_start_time = time.time()


@router.get("/health")
async def health_check():
    """Simple health check endpoint."""
    return {"status": "ok"}


@router.get("/status", response_model=SystemStatusResponse)
async def system_status():
    """
    Get detailed system status including Ollama connectivity and tools.
    """
    from main import get_app_state
    state = get_app_state()

    # Check Ollama
    ollama_ok = await state.ai_engine.check_health()

    # Check database (simple check - can we access it?)
    db_ok = True  # Assume OK if we got this far

    return SystemStatusResponse(
        status="online" if ollama_ok else "degraded",
        ollama_connected=ollama_ok,
        database_connected=db_ok,
        active_tools=state.tool_executor.tool_names,
        uptime_seconds=time.time() - _start_time,
    )


@router.post("/restart-autonomous-loop")
async def restart_autonomous_loop():
    """Restarts the autonomous loop."""
    from main import get_app_state
    state = get_app_state()

    await state.autonomous_loop.stop()
    await state.autonomous_loop.start()

    return {"status": "restarted"}


@router.get("/logs")
async def get_logs(lines: int = 100):
    """
    Get the last N lines of the log file.
    """
    from pathlib import Path

    log_file = Path("./data/logs/aria.log")
    if not log_file.exists():
        return {"logs": [], "message": "Log file not found."}

    try:
        with open(log_file, "r", encoding="utf-8") as f:
            all_lines = f.readlines()
            return {"logs": all_lines[-lines:]}
    except Exception as e:
        logger.error(f"Error reading logs: {e}")
        return {"logs": [], "error": str(e)}
