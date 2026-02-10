"""
ARIA Database Configuration
Sets up the asynchronous SQLAlchemy engine and session factory for PostgreSQL.
"""
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import DeclarativeBase

from config.settings import settings

# --- Database Engine ---
engine = create_async_engine(
    settings.database_url,
    echo=settings.debug,
    future=True,
)

# --- Session Factory ---
AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autoflush=False,
)


# --- Base Model ---
class Base(DeclarativeBase):
    """Base class for all database models."""
    pass


# --- Dependency ---
async def get_db() -> AsyncSession:
    """
    Dependency that yields a database session.
    Used in FastAPI routes.
    """
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()
