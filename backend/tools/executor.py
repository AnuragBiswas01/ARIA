"""
ARIA Tool Executor
Executes parsed tool calls by routing to the appropriate tool.
"""
from typing import Any

from .base import BaseTool
from utils.logger import get_logger

logger = get_logger(__name__)


class ToolExecutor:
    """
    Manages registered tools and executes tool calls.
    """

    def __init__(self):
        self._tools: dict[str, BaseTool] = {}

    def register(self, tool: BaseTool) -> None:
        """
        Registers a tool with the executor.

        Args:
            tool: An instance of a BaseTool subclass.
        """
        if tool.name in self._tools:
            logger.warning(f"Tool '{tool.name}' is already registered. Overwriting.")
        self._tools[tool.name] = tool
        logger.info(f"Registered tool: {tool.name}")

    def get_tools_for_prompt(self) -> list[dict]:
        """
        Returns a list of tool definitions for including in the LLM prompt.

        Returns:
            A list of tool dictionaries.
        """
        return [tool.to_dict() for tool in self._tools.values()]

    async def execute(self, tool_name: str, parameters: dict[str, Any]) -> dict[str, Any]:
        """
        Executes a tool by name with the given parameters.

        Args:
            tool_name: The name of the tool to execute.
            parameters: The parameters to pass to the tool.

        Returns:
            A dictionary with 'success', 'result', and optionally 'error'.
        """
        if tool_name not in self._tools:
            error_msg = f"Unknown tool: {tool_name}"
            logger.error(error_msg)
            return {"success": False, "error": error_msg, "result": None}

        tool = self._tools[tool_name]
        logger.info(f"Executing tool: {tool_name} with params: {parameters}")

        try:
            result = await tool.execute(**parameters)
            return {"success": True, "result": result, "error": None}
        except Exception as e:
            logger.exception(f"Error executing tool '{tool_name}': {e}")
            return {"success": False, "result": None, "error": str(e)}

    @property
    def tool_names(self) -> list[str]:
        """Returns a list of registered tool names."""
        return list(self._tools.keys())
