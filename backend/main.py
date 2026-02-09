"""
ARIA Backend - Main Application Entry Point

This is the main FastAPI application for ARIA.
It initializes all services, registers tools, and mounts API routes.
"""
import sys
from pathlib import Path
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Ensure the backend directory is in the path
sys.path.insert(0, str(Path(__file__).parent))

from config.settings import settings
from utils.logger import setup_logging, get_logger

# --- Initialize Logging ---
setup_logging()
logger = get_logger(__name__)


# --- Application State ---
class AppState:
    """Holds all the service instances for the application."""

    def __init__(self):
        self.ai_engine = None
        self.short_term_memory = None
        self.long_term_memory = None
        self.semantic_memory = None
        self.context_manager = None
        self.event_processor = None
        self.tool_parser = None
        self.tool_executor = None
        self.autonomous_loop = None


_app_state = AppState()


def get_app_state() -> AppState:
    """Returns the global application state."""
    return _app_state


# --- Lifespan Management ---
@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Manages the application lifecycle.
    Initializes services on startup and cleans up on shutdown.
    """
    logger.info("=" * 50)
    logger.info("ARIA Backend Starting...")
    logger.info("=" * 50)

    # Ensure data directories exist
    Path("./data/memory").mkdir(parents=True, exist_ok=True)
    Path("./data/logs").mkdir(parents=True, exist_ok=True)

    # --- Initialize Core Services ---
    from core.ai_engine import AIEngine
    from memory.short_term import ShortTermMemory
    from memory.long_term import LongTermMemory
    from memory.semantic import SemanticMemory
    from services.context_manager import ContextManager
    from services.event_processor import EventProcessor
    from tools.parser import ToolParser
    from tools.executor import ToolExecutor
    from core.autonomous_loop import AutonomousLoop

    # Initialize AI Engine
    _app_state.ai_engine = AIEngine()

    # Initialize Memory Systems
    _app_state.short_term_memory = ShortTermMemory()
    _app_state.long_term_memory = LongTermMemory()
    await _app_state.long_term_memory.initialize_db()
    _app_state.semantic_memory = SemanticMemory()

    # Initialize Services
    _app_state.context_manager = ContextManager(
        short_term_memory=_app_state.short_term_memory,
        semantic_memory=_app_state.semantic_memory,
    )
    _app_state.event_processor = EventProcessor(
        short_term_memory=_app_state.short_term_memory,
        long_term_memory=_app_state.long_term_memory,
        semantic_memory=_app_state.semantic_memory,
    )

    # Initialize Tool System
    _app_state.tool_parser = ToolParser()
    _app_state.tool_executor = ToolExecutor()

    # Register Tools
    from tools.web_search import WebSearchTool
    from tools.home_control import HomeControlTool
    from tools.notification import NotificationTool
    from tools.camera import CameraTool

    _app_state.tool_executor.register(WebSearchTool())
    _app_state.tool_executor.register(HomeControlTool())
    _app_state.tool_executor.register(NotificationTool())
    _app_state.tool_executor.register(CameraTool())

    # Initialize Autonomous Loop
    _app_state.autonomous_loop = AutonomousLoop(
        ai_engine=_app_state.ai_engine,
        context_manager=_app_state.context_manager,
        event_processor=_app_state.event_processor,
    )
    await _app_state.autonomous_loop.start()

    logger.info("ARIA Backend Ready!")
    logger.info(f"API running at http://{settings.api_host}:{settings.api_port}")
    logger.info(f"Ollama model: {settings.ollama_model}")
    logger.info(f"Registered tools: {_app_state.tool_executor.tool_names}")

    yield  # Application is running

    # --- Shutdown ---
    logger.info("ARIA Backend Shutting Down...")
    await _app_state.autonomous_loop.stop()
    await _app_state.ai_engine.close()
    logger.info("Goodbye!")


# --- Create FastAPI App ---
app = FastAPI(
    title="ARIA API",
    description="Adaptive Residential Intelligence Assistant - Backend API",
    version="1.0.0",
    lifespan=lifespan,
)

# --- CORS Middleware ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, restrict this
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Mount API Routes ---
from api.routes import (
    chat_router,
    system_router,
    devices_router,
    events_router,
    memory_router,
    context_router,
)

app.include_router(chat_router, prefix="/api")
app.include_router(system_router, prefix="/api")
app.include_router(devices_router, prefix="/api")
app.include_router(events_router, prefix="/api")
app.include_router(memory_router, prefix="/api")
app.include_router(context_router, prefix="/api")


# --- Root Endpoint ---
@app.get("/")
async def root():
    """Root endpoint - API welcome message."""
    return {
        "name": "ARIA API",
        "version": "1.0.0",
        "status": "online",
        "docs": "/docs",
    }


# --- Run with Uvicorn (for development) ---
if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "main:app",
        host=settings.api_host,
        port=settings.api_port,
        reload=True,
    )
