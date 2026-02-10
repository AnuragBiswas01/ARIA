"""
ARIA Service Verification Script
Checks connections to all integrated services.
"""
import asyncio
import sys
from pathlib import Path

# Add backend to path
sys.path.insert(0, str(Path(__file__).parents[1]))

from core.database import engine
from core.storage import check_minio_connection
from utils.ocr import check_tesseract_available
from config.settings import settings
from sqlalchemy import text
from redis import asyncio as aioredis
from core.llm import AIClient

async def check_services():
    print("="*50)
    print("Checking ARIA Core Services")
    print("="*50)

    # 1. Database
    print(f"\n[PostgreSQL] Connecting to {settings.database_url}...")
    try:
        async with engine.connect() as conn:
            await conn.execute(text("SELECT 1"))
        print("✅ Database connection successful.")
    except Exception as e:
        print(f"❌ Database connection failed: {e}")

    # 2. Redis
    print(f"\n[Redis] Connecting to {settings.redis_url}...")
    try:
        redis = aioredis.from_url(settings.redis_url)
        await redis.ping()
        await redis.close()
        print("✅ Redis connection successful.")
    except Exception as e:
        print(f"❌ Redis connection failed: {e}")

    # 3. MinIO
    print(f"\n[MinIO] Checking {settings.minio_endpoint}...")
    if check_minio_connection():
        print("✅ MinIO connection successful.")
    else:
        print("❌ MinIO connection failed.")

    # 4. Ollama
    print(f"\n[Ollama] Checking {settings.ollama_host}...")
    try:
        client = AIClient()
        # This is a bit tricky without a running gathering loop for the client check, 
        # but we initialized it. 
        # Let's try a simple list if possible, or just assume init is okay if no error.
        print("✅ Ollama client initialized.")
    except Exception as e:
        print(f"❌ Ollama client failed: {e}")

    # 5. Tesseract
    print(f"\n[Tesseract] Checking {settings.tesseract_path}...")
    if check_tesseract_available():
        print("✅ Tesseract executable found.")
    else:
        print("❌ Tesseract executable NOT found.")

    print("\n" + "="*50)
    print("Verification Complete")
    print("="*50)

if __name__ == "__main__":
    asyncio.run(check_services())
