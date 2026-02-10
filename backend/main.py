"""
ARIA Backend - Main Application Entry Point

This is the main FastAPI application for ARIA.
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


# --- Lifespan Management ---
@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Manages the application lifecycle.
    """
    logger.info("=" * 50)
    logger.info("ARIA Backend Starting...")
    logger.info("=" * 50)

    logger.info("ARIA Backend Ready!")
    logger.info(f"API running at http://{settings.api_host}:{settings.api_port}")

    yield  # Application is running

    # --- Shutdown ---
    logger.info("ARIA Backend Shutting Down...")
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

from core.database import engine
from core.storage import check_minio_connection
from utils.ocr import check_tesseract_available
from sqlalchemy import text
from config.settings import settings

# --- Health Check ---
@app.get("/health")
async def health_check():
    """Checks the status of all core services."""
    status = {
        "database": "unknown",
        "redis": "unknown",
        "minio": "unknown",
        "ollama": "unknown",
        "tesseract": "unknown",
    }

    # 1. Database Check
    try:
        async with engine.connect() as conn:
            await conn.execute(text("SELECT 1"))
            status["database"] = "connected"
    except Exception as e:
        status["database"] = f"error: {str(e)}"

    # 2. Redis Check (via Celery Broker URL)
    try:
        from redis import asyncio as aioredis
        redis = aioredis.from_url(settings.redis_url)
        await redis.ping()
        await redis.close()
        status["redis"] = "connected"
    except Exception as e:
        status["redis"] = f"error: {str(e)}"

    # 3. MinIO Check
    if check_minio_connection():
        status["minio"] = "connected"
    else:
        status["minio"] = "failed"

    # 4. Ollama Check
    try:
        from core.llm import AIClient
        # We instantiate directly to check connection
        client = AIClient()
        # Simple verify if host is set, real check needs asyncio run
        status["ollama"] = f"configured ({settings.ollama_host})"
    except Exception as e:
         status["ollama"] = f"error: {str(e)}"

    # 5. Tesseract Check
    if check_tesseract_available():
         status["tesseract"] = "available"
    else:
         status["tesseract"] = "not found"

    return status

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
        # reload_excludes=["./data/logs"],
    )
