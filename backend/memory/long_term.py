"""
ARIA Long-term Memory (SQLite)
Persistent storage for conversations, events, and structured data.
"""
from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, DateTime, JSON, create_engine, ForeignKey
from sqlalchemy.orm import sessionmaker, declarative_base, relationship
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.ext.asyncio import async_sessionmaker

from config.settings import settings
from utils.logger import get_logger
from utils.helpers import utc_now

logger = get_logger(__name__)

Base = declarative_base()


# --- ORM Models ---

class Conversation(Base):
    """A conversation session with ARIA."""
    __tablename__ = "conversations"

    id = Column(Integer, primary_key=True, autoincrement=True)
    session_id = Column(String(64), unique=True, index=True, nullable=False)
    title = Column(String(255), nullable=True)
    created_at = Column(DateTime, default=utc_now)
    updated_at = Column(DateTime, default=utc_now, onupdate=utc_now)

    messages = relationship("Message", back_populates="conversation", cascade="all, delete-orphan")


class Message(Base):
    """A single message in a conversation."""
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True, autoincrement=True)
    conversation_id = Column(Integer, ForeignKey("conversations.id"), nullable=False)
    role = Column(String(16), nullable=False)  # 'user', 'assistant', 'system'
    content = Column(Text, nullable=False)
    meta_data = Column(JSON, nullable=True)  # For tool calls, etc.
    created_at = Column(DateTime, default=utc_now)

    conversation = relationship("Conversation", back_populates="messages")


class HomeEvent(Base):
    """A significant event in the home (e.g., motion detected, door opened)."""
    __tablename__ = "home_events"

    id = Column(Integer, primary_key=True, autoincrement=True)
    event_type = Column(String(64), nullable=False, index=True)
    source = Column(String(128), nullable=True)  # e.g., 'sensor.front_door', 'camera.living_room'
    data = Column(JSON, nullable=True)
    created_at = Column(DateTime, default=utc_now, index=True)


class UserPreference(Base):
    """Stores user preferences learned by ARIA."""
    __tablename__ = "user_preferences"

    id = Column(Integer, primary_key=True, autoincrement=True)
    key = Column(String(128), unique=True, nullable=False, index=True)
    value = Column(Text, nullable=False)
    updated_at = Column(DateTime, default=utc_now, onupdate=utc_now)


# --- Long-term Memory Service ---

class LongTermMemory:
    """
    Service for interacting with the SQLite database for persistent storage.
    """

    def __init__(self, db_url: str | None = None):
        """
        Initializes the database connection.

        Args:
            db_url: The database connection string. Defaults to settings value.
        """
        self.db_url = db_url or settings.database_url
        self.engine = create_async_engine(self.db_url, echo=False)
        self.async_session = async_sessionmaker(self.engine, expire_on_commit=False)
        logger.info(f"LongTermMemory initialized with DB: {self.db_url}")

    async def initialize_db(self):
        """Creates all tables if they don't exist."""
        async with self.engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
        logger.info("Database tables initialized.")

    async def get_session(self) -> AsyncSession:
        """Returns a new async database session."""
        return self.async_session()

    # --- Conversation Methods ---

    async def create_conversation(self, session_id: str, title: str | None = None) -> Conversation:
        """Creates a new conversation record."""
        async with self.async_session() as session:
            convo = Conversation(session_id=session_id, title=title)
            session.add(convo)
            await session.commit()
            await session.refresh(convo)
            return convo

    async def add_message(
        self, conversation_id: int, role: str, content: str, metadata: dict | None = None
    ) -> Message:
        """Adds a message to an existing conversation."""
        async with self.async_session() as session:
            msg = Message(
                conversation_id=conversation_id,
                role=role,
                content=content,
                meta_data=metadata,
            )
            session.add(msg)
            await session.commit()
            await session.refresh(msg)
            return msg

    # --- Event Methods ---

    async def log_event(
        self, event_type: str, source: str | None = None, data: dict | None = None
    ) -> HomeEvent:
        """Logs a home event."""
        async with self.async_session() as session:
            event = HomeEvent(event_type=event_type, source=source, data=data)
            session.add(event)
            await session.commit()
            await session.refresh(event)
            return event

    # --- Preference Methods ---

    async def set_preference(self, key: str, value: str) -> UserPreference:
        """Sets or updates a user preference."""
        async with self.async_session() as session:
            from sqlalchemy import select
            result = await session.execute(select(UserPreference).where(UserPreference.key == key))
            pref = result.scalar_one_or_none()

            if pref:
                pref.value = value
            else:
                pref = UserPreference(key=key, value=value)
                session.add(pref)

            await session.commit()
            await session.refresh(pref)
            return pref

    async def get_preference(self, key: str) -> str | None:
        """Gets a user preference by key."""
        async with self.async_session() as session:
            from sqlalchemy import select
            result = await session.execute(select(UserPreference).where(UserPreference.key == key))
            pref = result.scalar_one_or_none()
            return pref.value if pref else None
