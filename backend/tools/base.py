"""
ARIA Base Tool Definition
Abstract base class for all ARIA tools.
"""
from abc import ABC, abstractmethod
from typing import Any


class BaseTool(ABC):
    """
    Abstract base class for all tools that ARIA can use.
    Each tool must define its name, description, parameters, and an execute method.
    """

    @property
    @abstractmethod
    def name(self) -> str:
        """The unique name of the tool."""
        ...

    @property
    @abstractmethod
    def description(self) -> str:
        """A short description of what the tool does. Used by the LLM to decide when to use it."""
        ...

    @property
    @abstractmethod
    def parameters(self) -> dict:
        """
        A JSON Schema-like dictionary describing the parameters of the tool.
        Example:
        {
            "type": "object",
            "properties": {
                "query": {"type": "string", "description": "The search query."}
            },
            "required": ["query"]
        }
        """
        ...

    @abstractmethod
    async def execute(self, **kwargs: Any) -> Any:
        """
        Executes the tool with the given parameters.

        Args:
            **kwargs: The parameters for the tool.

        Returns:
            The result of the tool execution.
        """
        ...

    def to_dict(self) -> dict:
        """Returns a dictionary representation of the tool for the LLM."""
        return {
            "name": self.name,
            "description": self.description,
            "parameters": self.parameters,
        }
