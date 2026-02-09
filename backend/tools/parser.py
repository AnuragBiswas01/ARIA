"""
ARIA Tool Call Parser
Parses tool calls from LLM responses.
"""
import json
import re
from typing import Any

from utils.logger import get_logger

logger = get_logger(__name__)


class ToolParser:
    """
    Parses tool calls from the LLM's response text.
    Supports JSON format for tool calls.
    """

    # Regex to find JSON blocks in the response
    # This handles both ```json ... ``` and bare JSON objects.
    JSON_PATTERN = re.compile(
        r"```(?:json)?\s*(\{.*?\})\s*```|(\{[^{}]*\"tool\"[^{}]*\})",
        re.DOTALL | re.IGNORECASE,
    )

    def parse(self, response_text: str) -> list[dict[str, Any]]:
        """
        Parses the LLM response for tool calls.

        Args:
            response_text: The raw text from the LLM.

        Returns:
            A list of parsed tool call dictionaries, each with 'tool' and 'parameters'.
        """
        tool_calls = []
        matches = self.JSON_PATTERN.findall(response_text)

        for match_groups in matches:
            # match_groups is a tuple of groups; pick the non-empty one
            json_str = next((g for g in match_groups if g), None)
            if not json_str:
                continue

            try:
                data = json.loads(json_str)
                if self._is_valid_tool_call(data):
                    tool_calls.append({
                        "tool": data["tool"],
                        "parameters": data.get("parameters", {}),
                    })
                    logger.debug(f"Parsed tool call: {data['tool']}")
            except json.JSONDecodeError as e:
                logger.warning(f"Failed to parse JSON: {e}")
                continue

        return tool_calls

    def _is_valid_tool_call(self, data: Any) -> bool:
        """Checks if the parsed data is a valid tool call structure."""
        return isinstance(data, dict) and "tool" in data
