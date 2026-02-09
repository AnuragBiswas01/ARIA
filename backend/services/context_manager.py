"""
ARIA Context Manager
Manages the current state of the home and conversation context.
"""
from typing import Any

from config.settings import settings
from memory import ShortTermMemory, SemanticMemory
from utils.logger import get_logger

logger = get_logger(__name__)


class ContextManager:
    """
    Manages the context for ARIA's interactions.
    Combines working memory (current conversation) with short-term and semantic memory.
    """

    def __init__(
        self,
        short_term_memory: ShortTermMemory,
        semantic_memory: SemanticMemory,
    ):
        """
        Initializes the context manager.

        Args:
            short_term_memory: The short-term memory instance.
            semantic_memory: The semantic memory instance.
        """
        self.short_term = short_term_memory
        self.semantic = semantic_memory
        self.working_memory_size = settings.working_memory_size

        # Working memory: the immediate conversation context
        self._working_memory: list[dict] = []

        # Home state: current status of devices, etc.
        self._home_state: dict[str, Any] = {}

        logger.info("ContextManager initialized.")

    def add_to_working_memory(self, role: str, content: str) -> None:
        """
        Adds a message to the working memory.

        Args:
            role: The role ('user' or 'assistant').
            content: The message content.
        """
        self._working_memory.append({"role": role, "content": content})

        # Trim to keep only the last N messages
        if len(self._working_memory) > self.working_memory_size:
            self._working_memory = self._working_memory[-self.working_memory_size:]

    def get_working_memory(self) -> list[dict]:
        """Returns the current working memory (conversation context)."""
        return list(self._working_memory)

    def clear_working_memory(self) -> None:
        """Clears the working memory."""
        self._working_memory = []
        logger.info("Working memory cleared.")

    def update_home_state(self, entity_id: str, state: Any) -> None:
        """
        Updates the state of a home entity.

        Args:
            entity_id: The entity ID.
            state: The current state.
        """
        self._home_state[entity_id] = state

    def get_home_state(self) -> dict[str, Any]:
        """Returns the current home state."""
        return dict(self._home_state)

    def get_entity_state(self, entity_id: str) -> Any:
        """Gets the state of a specific entity."""
        return self._home_state.get(entity_id)

    async def build_context_for_prompt(self, current_query: str) -> dict:
        """
        Builds a rich context for the LLM prompt.
        
        Combines:
        - Working memory (recent conversation)
        - Relevant semantic memories
        - Current home state

        Args:
            current_query: The user's current query.

        Returns:
            A dictionary with context sections.
        """
        # Get relevant memories from semantic search
        relevant_memories = self.semantic.search_conversations(current_query, n_results=3)
        relevant_events = self.semantic.search_events(current_query, n_results=2)

        # Get recent events from short-term memory
        recent_events = self.short_term.get_recent(category="event", limit=5)

        return {
            "working_memory": self.get_working_memory(),
            "relevant_memories": [m["document"] for m in relevant_memories],
            "relevant_events": [e["document"] for e in relevant_events],
            "recent_events": [e["data"] for e in recent_events],
            "home_state": self.get_home_state(),
        }
