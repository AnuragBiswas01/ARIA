"""
ARIA API Response Schemas
Pydantic models for API response serialization.
"""
from pydantic import BaseModel, Field
from typing import Any
from datetime import datetime


class ChatResponse(BaseModel):
    """Response from chat endpoint."""
    response: str = Field(..., description="The AI's response.")
    session_id: str = Field(..., description="The conversation session ID.")
    tool_calls: list[dict] | None = Field(default=None, description="Any tool calls made.")
    tool_results: list[dict] | None = Field(default=None, description="Results from tool calls.")


class SystemStatusResponse(BaseModel):
    """Response for system health check."""
    status: str = Field(..., description="Overall system status.")
    ollama_connected: bool = Field(..., description="Is Ollama reachable.")
    database_connected: bool = Field(..., description="Is database connected.")
    active_tools: list[str] = Field(..., description="List of registered tools.")
    uptime_seconds: float = Field(..., description="Server uptime in seconds.")


class DeviceActionResponse(BaseModel):
    """Response from device control."""
    entity_id: str
    action: str
    status: str
    message: str | None = None
    error: str | None = None


class EventResponse(BaseModel):
    """Response from event logging."""
    event_type: str
    source: str | None
    timestamp: str
    data: dict | None


class MemorySearchResponse(BaseModel):
    """Response from memory search."""
    query: str
    collection: str
    results: list[dict]
    count: int


class NotificationResponse(BaseModel):
    """A notification object."""
    id: int
    title: str
    message: str
    priority: str
    timestamp: str
    read: bool
