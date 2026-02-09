"""
ARIA Web Search Tool
Performs web searches using DuckDuckGo (no API key required).
"""
import httpx
from typing import Any

from .base import BaseTool
from utils.logger import get_logger

logger = get_logger(__name__)


class WebSearchTool(BaseTool):
    """
    Tool for performing web searches.
    Uses DuckDuckGo's HTML interface for simplicity (no API key needed).
    """

    @property
    def name(self) -> str:
        return "web_search"

    @property
    def description(self) -> str:
        return "Search the web for information. Use this when you need current news, facts, or information not in your knowledge base."

    @property
    def parameters(self) -> dict:
        return {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "The search query.",
                },
            },
            "required": ["query"],
        }

    async def execute(self, query: str, **kwargs: Any) -> dict:
        """
        Executes a web search.

        Args:
            query: The search query.

        Returns:
            A dictionary with search results.
        """
        logger.info(f"Web search: {query}")

        # Using DuckDuckGo Instant Answer API (limited, but no key needed)
        # For production, consider integrating SearXNG or a paid API.
        url = "https://api.duckduckgo.com/"
        params = {
            "q": query,
            "format": "json",
            "no_html": 1,
            "skip_disambig": 1,
        }

        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                response = await client.get(url, params=params)
                response.raise_for_status()
                data = response.json()

            results = []
            # Abstract (main answer)
            if data.get("Abstract"):
                results.append({
                    "title": data.get("Heading", "Result"),
                    "snippet": data.get("Abstract"),
                    "url": data.get("AbstractURL"),
                })

            # Related topics
            for topic in data.get("RelatedTopics", [])[:5]:
                if isinstance(topic, dict) and "Text" in topic:
                    results.append({
                        "title": topic.get("Text", "")[:50],
                        "snippet": topic.get("Text"),
                        "url": topic.get("FirstURL"),
                    })

            return {
                "query": query,
                "results": results if results else [{"snippet": "No results found."}],
            }

        except httpx.RequestError as e:
            logger.error(f"Web search error: {e}")
            return {"query": query, "error": str(e), "results": []}
