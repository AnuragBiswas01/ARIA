"""
ARIA Utility Helpers
Common utility functions used throughout the application.
"""
from datetime import datetime, timezone
from typing import Any
import json


def utc_now() -> datetime:
    """Returns the current UTC time as a timezone-aware datetime."""
    return datetime.now(timezone.utc)


def format_timestamp(dt: datetime) -> str:
    """Formats a datetime object to an ISO 8601 string."""
    return dt.isoformat()


def safe_json_loads(data: str, default: Any = None) -> Any:
    """
    Safely parses a JSON string, returning a default value on failure.
    
    Args:
        data: The JSON string to parse.
        default: The value to return if parsing fails.
    
    Returns:
        The parsed JSON object or the default value.
    """
    try:
        return json.loads(data)
    except (json.JSONDecodeError, TypeError):
        return default


def truncate_string(text: str, max_length: int = 100, suffix: str = "...") -> str:
    """
    Truncates a string to a maximum length, adding a suffix if truncated.
    
    Args:
        text: The string to truncate.
        max_length: The maximum length of the resulting string (includes suffix).
        suffix: The suffix to add if the string is truncated.
    
    Returns:
        The truncated string.
    """
    if len(text) <= max_length:
        return text
    return text[:max_length - len(suffix)] + suffix
