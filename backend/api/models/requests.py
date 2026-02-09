"""
ARIA API Request Schemas
Pydantic models for API request validation.
"""
from pydantic import BaseModel, Field
from typing import Any


class ChatRequest(BaseModel):
    """Request body for chat endpoint."""
    message: str = Field(..., min_length=1, description="The user's message.")
    session_id: str | None = Field(default=None, description="Optional conversation session ID.")
    stream: bool = Field(default=False, description="Whether to stream the response.")


class DeviceActionRequest(BaseModel):
    """Request body for device control."""
    entity_id: str = Field(..., description="The Home Assistant entity ID.")
    action: str = Field(..., description="Action: turn_on, turn_off, toggle, set.")
    value: str | None = Field(default=None, description="Optional value for set action.")


class EventRequest(BaseModel):
    """Request body for logging an event."""
    event_type: str = Field(..., description="The type of event.")
    source: str | None = Field(default=None, description="The source of the event.")
    data: dict[str, Any] | None = Field(default=None, description="Additional event data.")


class MemorySearchRequest(BaseModel):
    """Request body for semantic memory search."""
    query: str = Field(..., min_length=1, description="The search query.")
    n_results: int = Field(default=5, ge=1, le=20, description="Number of results.")
    collection: str = Field(default="conversations", description="Which collection to search.")
