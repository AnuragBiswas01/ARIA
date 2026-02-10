"""
ARIA AI Engine Configuration
Sets up the Ollama client for LLM inference.
"""
from ollama import AsyncClient
from config.settings import settings
from utils.logger import get_logger

logger = get_logger(__name__)


class AIClient:
    """Wrapper for Ollama AsyncClient."""

    def __init__(self):
        self.host = settings.ollama_host
        self.model = settings.ollama_model
        self.client = AsyncClient(host=self.host)

    async def generate(self, prompt: str, system: str = None) -> str:
        """
        Generates text using the configured Ollama model.
        """
        try:
            response = await self.client.generate(
                model=self.model,
                prompt=prompt,
                system=system,
                stream=False
            )
            return response['response']
        except Exception as e:
            logger.error(f"Ollama generation failed: {e}")
            raise

    async def check_connection(self) -> bool:
        """Checks if Ollama is reachable."""
        try:
            # List models to check connection
            await self.client.list()
            return True
        except Exception as e:
            logger.error(f"Ollama connection check failed: {e}")
            return False

_ai_client_instance = None

def get_ai_client() -> AIClient:
    """Returns a singleton AIClient."""
    global _ai_client_instance
    if _ai_client_instance is None:
        _ai_client_instance = AIClient()
    return _ai_client_instance
