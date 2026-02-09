"""
ARIA Short-term Memory
In-memory cache for recent events and conversation turns.
Fast access for time-sensitive context (last few hours).
"""
from datetime import datetime, timedelta
from typing import Any
from collections import OrderedDict
import threading

from config.settings import settings
from utils.logger import get_logger
from utils.helpers import utc_now

logger = get_logger(__name__)


class ShortTermMemory:
    """
    A time-based, LRU-like in-memory cache.
    Items expire after a configurable TTL.
    """

    def __init__(self, ttl_hours: int | None = None, max_items: int = 1000):
        """
        Initializes the short-term memory.

        Args:
            ttl_hours: Time-to-live for items in hours. Defaults to settings value.
            max_items: Maximum number of items to store.
        """
        self.ttl = timedelta(hours=ttl_hours or settings.short_term_memory_ttl_hours)
        self.max_items = max_items
        self._store: OrderedDict[str, dict[str, Any]] = OrderedDict()
        self._lock = threading.Lock()
        logger.info(f"ShortTermMemory initialized (TTL: {self.ttl}, Max: {max_items})")

    def add(self, key: str, data: Any, category: str = "general") -> None:
        """
        Adds an item to the short-term memory.

        Args:
            key: A unique identifier for the item.
            data: The data to store.
            category: A category for filtering (e.g., 'conversation', 'event').
        """
        with self._lock:
            # Remove old entry if key exists to update timestamp and move to end
            if key in self._store:
                del self._store[key]

            self._store[key] = {
                "data": data,
                "category": category,
                "timestamp": utc_now(),
            }

            # Enforce max items
            while len(self._store) > self.max_items:
                self._store.popitem(last=False)

    def get(self, key: str) -> Any | None:
        """
        Retrieves an item by key, returning None if not found or expired.

        Args:
            key: The identifier of the item.

        Returns:
            The stored data or None.
        """
        with self._lock:
            item = self._store.get(key)
            if item is None:
                return None

            if self._is_expired(item["timestamp"]):
                del self._store[key]
                return None

            return item["data"]

    def get_recent(self, category: str | None = None, limit: int = 10) -> list[dict]:
        """
        Gets the most recent items, optionally filtered by category.

        Args:
            category: Optional category to filter by.
            limit: Maximum number of items to return.

        Returns:
            A list of the most recent items (newest first).
        """
        with self._lock:
            self._cleanup_expired()

            items = list(self._store.values())

            if category:
                items = [item for item in items if item["category"] == category]

            # Sort by timestamp descending (newest first)
            items.sort(key=lambda x: x["timestamp"], reverse=True)

            return items[:limit]

    def clear(self, category: str | None = None) -> int:
        """
        Clears items from memory, optionally filtered by category.

        Args:
            category: If provided, only clear items of this category.

        Returns:
            The number of items cleared.
        """
        with self._lock:
            if category is None:
                count = len(self._store)
                self._store.clear()
                return count

            keys_to_delete = [
                key for key, item in self._store.items()
                if item["category"] == category
            ]
            for key in keys_to_delete:
                del self._store[key]
            return len(keys_to_delete)

    def _is_expired(self, timestamp: datetime) -> bool:
        """Checks if a timestamp has exceeded the TTL."""
        return utc_now() - timestamp > self.ttl

    def _cleanup_expired(self) -> None:
        """Removes all expired items from the store."""
        keys_to_delete = [
            key for key, item in self._store.items()
            if self._is_expired(item["timestamp"])
        ]
        for key in keys_to_delete:
            del self._store[key]

    def __len__(self) -> int:
        """Returns the current number of items in memory."""
        with self._lock:
            self._cleanup_expired()
            return len(self._store)
