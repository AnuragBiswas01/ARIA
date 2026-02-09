"""
ARIA AI Engine
Handles all communication with the Ollama LLM.
"""
import httpx
from pathlib import Path
from typing import AsyncIterator

from config.settings import settings
from utils.logger import get_logger

logger = get_logger(__name__)

# Load personality prompt
PERSONALITY_PATH = Path(__file__).parent / "personality.txt"
try:
    SYSTEM_PROMPT = PERSONALITY_PATH.read_text(encoding="utf-8")
except FileNotFoundError:
    logger.warning("personality.txt not found. Using default system prompt.")
    SYSTEM_PROMPT = "You are ARIA, a helpful AI home assistant."


class AIEngine:
    """
    Interface for the Ollama LLM.
    Manages conversation context and tool calling.
    """

    def __init__(self):
        self.base_url = settings.ollama_base_url
        self.model = settings.ollama_model
        self.client = httpx.AsyncClient(base_url=self.base_url, timeout=120.0)
        logger.info(f"AIEngine initialized with model: {self.model}")

    async def generate(
        self,
        prompt: str,
        system_prompt: str | None = None,
        context: list[dict] | None = None,
        stream: bool = False,
    ) -> str | AsyncIterator[str]:
        """
        Generates a response from the LLM.

        Args:
            prompt: The user's message.
            system_prompt: Optional override for the system prompt.
            context: A list of previous messages for context.
            stream: Whether to stream the response.

        Returns:
            The full response string, or an async iterator of chunks if streaming.
        """
        messages = self._build_messages(prompt, system_prompt, context)

        if stream:
            return self._stream_generate(messages)
        else:
            return await self._sync_generate(messages)

    def _build_messages(
        self,
        prompt: str,
        system_prompt: str | None,
        context: list[dict] | None,
    ) -> list[dict]:
        """Builds the message list for the API call."""
        messages = [{"role": "system", "content": system_prompt or SYSTEM_PROMPT}]

        if context:
            messages.extend(context)

        messages.append({"role": "user", "content": prompt})
        return messages

    async def _sync_generate(self, messages: list[dict]) -> str:
        """Non-streaming generation."""
        payload = {
            "model": self.model,
            "messages": messages,
            "stream": False,
        }
        try:
            response = await self.client.post("/api/chat", json=payload)
            response.raise_for_status()
            data = response.json()
            return data.get("message", {}).get("content", "")
        except httpx.HTTPStatusError as e:
            logger.error(f"Ollama API error: {e.response.status_code} - {e.response.text}")
            raise
        except httpx.RequestError as e:
            logger.error(f"Ollama connection error: {e}")
            raise

    async def _stream_generate(self, messages: list[dict]) -> AsyncIterator[str]:
        """Streaming generation."""
        payload = {
            "model": self.model,
            "messages": messages,
            "stream": True,
        }
        try:
            async with self.client.stream("POST", "/api/chat", json=payload) as response:
                response.raise_for_status()
                async for line in response.aiter_lines():
                    if line:
                        import json
                        try:
                            data = json.loads(line)
                            content = data.get("message", {}).get("content", "")
                            if content:
                                yield content
                        except json.JSONDecodeError:
                            continue
        except httpx.HTTPStatusError as e:
            logger.error(f"Ollama API error: {e.response.status_code}")
            raise
        except httpx.RequestError as e:
            logger.error(f"Ollama connection error: {e}")
            raise

    async def check_health(self) -> bool:
        """Checks if the Ollama service is reachable."""
        try:
            response = await self.client.get("/api/tags")
            return response.status_code == 200
        except httpx.RequestError:
            return False

    async def close(self):
        """Closes the HTTP client."""
        await self.client.aclose()
