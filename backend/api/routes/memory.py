"""
ARIA Memory API Routes
Endpoints for querying and managing ARIA's memory.
"""
from fastapi import APIRouter

from api.models.requests import MemorySearchRequest
from api.models.responses import MemorySearchResponse
from utils.logger import get_logger

logger = get_logger(__name__)

router = APIRouter(prefix="/memory", tags=["Memory"])


@router.post("/search", response_model=MemorySearchResponse)
async def search_memory(request: MemorySearchRequest):
    """
    Search semantic memory for relevant information.
    """
    from main import get_app_state
    state = get_app_state()

    if request.collection == "conversations":
        results = state.semantic_memory.search_conversations(
            request.query, n_results=request.n_results
        )
    elif request.collection == "events":
        results = state.semantic_memory.search_events(
            request.query, n_results=request.n_results
        )
    elif request.collection == "knowledge":
        results = state.semantic_memory.search_knowledge(
            request.query, n_results=request.n_results
        )
    else:
        results = []

    return MemorySearchResponse(
        query=request.query,
        collection=request.collection,
        results=results,
        count=len(results),
    )


@router.get("/stats")
async def memory_stats():
    """
    Get memory usage statistics.
    """
    from main import get_app_state
    state = get_app_state()

    return {
        "short_term": {
            "item_count": len(state.short_term_memory),
        },
        "semantic": {
            "conversations_count": state.semantic_memory.conversations.count(),
            "events_count": state.semantic_memory.events.count(),
            "knowledge_count": state.semantic_memory.knowledge.count(),
        },
    }


@router.post("/clear-short-term")
async def clear_short_term(category: str | None = None):
    """
    Clear short-term memory, optionally by category.
    """
    from main import get_app_state
    state = get_app_state()

    count = state.short_term_memory.clear(category=category)
    return {"cleared": count, "category": category or "all"}


@router.post("/clear-working")
async def clear_working_memory():
    """
    Clear the current conversation context (working memory).
    """
    from main import get_app_state
    state = get_app_state()

    state.context_manager.clear_working_memory()
    return {"status": "cleared"}
