"""
ARIA Semantic Memory (ChromaDB)
Vector database for semantic search over conversations and events.
"""
import chromadb
from chromadb.config import Settings as ChromaSettings

from config.settings import settings
from utils.logger import get_logger

logger = get_logger(__name__)


class SemanticMemory:
    """
    Service for semantic search using ChromaDB.
    Allows ARIA to find relevant past conversations and events based on meaning.
    """

    COLLECTION_CONVERSATIONS = "aria_conversations"
    COLLECTION_EVENTS = "aria_events"
    COLLECTION_KNOWLEDGE = "aria_knowledge"

    def __init__(self, persist_dir: str | None = None):
        """
        Initializes the ChromaDB client.

        Args:
            persist_dir: The directory to persist data. Defaults to settings value.
        """
        self.persist_dir = persist_dir or settings.chroma_persist_dir
        self.client = chromadb.PersistentClient(
            path=self.persist_dir,
            settings=ChromaSettings(anonymized_telemetry=False),
        )
        self._init_collections()
        logger.info(f"SemanticMemory initialized at: {self.persist_dir}")

    def _init_collections(self):
        """Initializes the required collections."""
        self.conversations = self.client.get_or_create_collection(
            name=self.COLLECTION_CONVERSATIONS,
            metadata={"hnsw:space": "cosine"}
        )
        self.events = self.client.get_or_create_collection(
            name=self.COLLECTION_EVENTS,
            metadata={"hnsw:space": "cosine"}
        )
        self.knowledge = self.client.get_or_create_collection(
            name=self.COLLECTION_KNOWLEDGE,
            metadata={"hnsw:space": "cosine"}
        )

    def add_conversation_memory(
        self, doc_id: str, text: str, metadata: dict | None = None
    ) -> None:
        """
        Adds a piece of conversation to the semantic memory.

        Args:
            doc_id: A unique ID for this document (e.g., message_id).
            text: The text content to embed and store.
            metadata: Optional metadata for filtering.
        """
        self.conversations.add(
            ids=[doc_id],
            documents=[text],
            metadatas=[metadata] if metadata else None,
        )
        logger.debug(f"Added conversation memory: {doc_id[:20]}...")

    def add_event_memory(
        self, doc_id: str, text: str, metadata: dict | None = None
    ) -> None:
        """
        Adds a home event description to semantic memory.

        Args:
            doc_id: A unique ID for this document.
            text: The textual description of the event.
            metadata: Optional metadata for filtering.
        """
        self.events.add(
            ids=[doc_id],
            documents=[text],
            metadatas=[metadata] if metadata else None,
        )
        logger.debug(f"Added event memory: {doc_id[:20]}...")

    def search_conversations(
        self, query: str, n_results: int = 5, filter_metadata: dict | None = None
    ) -> list[dict]:
        """
        Searches for relevant past conversations.

        Args:
            query: The search query.
            n_results: Number of results to return.
            filter_metadata: Optional metadata filter.

        Returns:
            A list of matching documents with their metadata and distances.
        """
        results = self.conversations.query(
            query_texts=[query],
            n_results=n_results,
            where=filter_metadata,
        )
        return self._format_results(results)

    def search_events(
        self, query: str, n_results: int = 5, filter_metadata: dict | None = None
    ) -> list[dict]:
        """
        Searches for relevant past events.

        Args:
            query: The search query.
            n_results: Number of results to return.
            filter_metadata: Optional metadata filter.

        Returns:
            A list of matching documents with their metadata and distances.
        """
        results = self.events.query(
            query_texts=[query],
            n_results=n_results,
            where=filter_metadata,
        )
        return self._format_results(results)

    def search_knowledge(
        self, query: str, n_results: int = 5, filter_metadata: dict | None = None
    ) -> list[dict]:
        """
        Searches the general knowledge base.

        Args:
            query: The search query.
            n_results: Number of results to return.
            filter_metadata: Optional metadata filter.

        Returns:
            A list of matching documents with metadata and distances.
        """
        results = self.knowledge.query(
            query_texts=[query],
            n_results=n_results,
            where=filter_metadata,
        )
        return self._format_results(results)

    def _format_results(self, results: dict) -> list[dict]:
        """Formats ChromaDB query results into a cleaner list."""
        formatted = []
        if not results or not results.get("ids"):
            return formatted

        ids = results["ids"][0]
        documents = results["documents"][0] if results.get("documents") else [None] * len(ids)
        metadatas = results["metadatas"][0] if results.get("metadatas") else [None] * len(ids)
        distances = results["distances"][0] if results.get("distances") else [None] * len(ids)

        for i, doc_id in enumerate(ids):
            formatted.append({
                "id": doc_id,
                "document": documents[i],
                "metadata": metadatas[i],
                "distance": distances[i],
            })

        return formatted

    def delete_memory(self, collection_name: str, doc_ids: list[str]) -> None:
        """
        Deletes documents from a collection.

        Args:
            collection_name: The name of the collection.
            doc_ids: A list of document IDs to delete.
        """
        collection = self.client.get_collection(collection_name)
        collection.delete(ids=doc_ids)
        logger.info(f"Deleted {len(doc_ids)} documents from {collection_name}")
