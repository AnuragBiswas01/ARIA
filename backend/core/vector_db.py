"""
ARIA Vector Database Configuration
Sets up the ChromaDB client for vector embeddings.
"""
import chromadb
from chromadb.config import Settings
from config.settings import settings
from utils.logger import get_logger

logger = get_logger(__name__)


def get_chroma_client():
    """
    Returns a persistent ChromaDB client.
    """
    logger.info(f"Initializing ChromaDB at {settings.chroma_path}")
    client = chromadb.PersistentClient(
        path=settings.chroma_path,
        settings=Settings(allow_reset=True, anonymized_telemetry=False)
    )
    return client
