"""
ARIA Event Processor
Processes incoming events from the home (sensors, devices, etc.).
"""
from typing import Any
from datetime import datetime

from memory import ShortTermMemory, LongTermMemory, SemanticMemory
from utils.logger import get_logger
from utils.helpers import utc_now

logger = get_logger(__name__)


class EventProcessor:
    """
    Processes and stores events from the smart home.
    Events can come from sensors, device state changes, or external systems.
    """

    def __init__(
        self,
        short_term_memory: ShortTermMemory,
        long_term_memory: LongTermMemory,
        semantic_memory: SemanticMemory,
    ):
        """
        Initializes the event processor.

        Args:
            short_term_memory: For quick access to recent events.
            long_term_memory: For persistent storage.
            semantic_memory: For semantic search over events.
        """
        self.short_term = short_term_memory
        self.long_term = long_term_memory
        self.semantic = semantic_memory
        logger.info("EventProcessor initialized.")

    async def process_event(
        self, event_type: str, source: str | None = None, data: dict[str, Any] | None = None
    ) -> dict:
        """
        Processes an incoming home event.

        Args:
            event_type: The type of event (e.g., 'motion_detected', 'door_opened').
            source: The source of the event (e.g., 'sensor.front_door').
            data: Additional event data.

        Returns:
            The processed event record.
        """
        timestamp = utc_now()
        event_key = f"{event_type}_{source}_{timestamp.timestamp()}"

        event_record = {
            "event_type": event_type,
            "source": source,
            "data": data or {},
            "timestamp": timestamp.isoformat(),
        }

        # Store in short-term memory for quick access
        self.short_term.add(
            key=event_key,
            data=event_record,
            category="event",
        )

        # Store in long-term memory for persistence
        await self.long_term.log_event(
            event_type=event_type,
            source=source,
            data=data,
        )

        # Store in semantic memory for search
        event_text = self._create_event_description(event_type, source, data, timestamp)
        self.semantic.add_event_memory(
            doc_id=event_key,
            text=event_text,
            metadata={"event_type": event_type, "source": source or "unknown"},
        )

        logger.info(f"Processed event: {event_type} from {source}")
        return event_record

    def _create_event_description(
        self, event_type: str, source: str | None, data: dict | None, timestamp: datetime
    ) -> str:
        """Creates a human-readable description of the event for semantic storage."""
        time_str = timestamp.strftime("%Y-%m-%d %H:%M:%S")
        parts = [f"At {time_str}, event '{event_type}' occurred"]

        if source:
            parts.append(f"from {source}")

        if data:
            # Add key details from data
            for key, value in data.items():
                parts.append(f"({key}: {value})")

        return " ".join(parts) + "."

    def get_recent_events(self, limit: int = 10) -> list[dict]:
        """Gets recent events from short-term memory."""
        return [item["data"] for item in self.short_term.get_recent(category="event", limit=limit)]
