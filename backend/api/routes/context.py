"""
ARIA Context API Routes
Endpoints for managing home context and state.
"""
from fastapi import APIRouter
from typing import Any

from utils.logger import get_logger

logger = get_logger(__name__)

router = APIRouter(prefix="/context", tags=["Context"])


@router.get("/home-state")
async def get_home_state():
    """
    Get the current known state of the home.
    """
    from main import get_app_state
    state = get_app_state()

    return {"home_state": state.context_manager.get_home_state()}


@router.put("/home-state/{entity_id}")
async def update_entity_state(entity_id: str, state_value: Any):
    """
    Manually update the state of an entity.
    Useful for testing or manual overrides.
    """
    from main import get_app_state
    state = get_app_state()

    state.context_manager.update_home_state(entity_id, state_value)
    return {"entity_id": entity_id, "new_state": state_value}


@router.get("/working-memory")
async def get_working_memory():
    """
    Get the current working memory (conversation context).
    """
    from main import get_app_state
    state = get_app_state()

    return {"working_memory": state.context_manager.get_working_memory()}


@router.get("/full-context")
async def get_full_context(query: str = "current state"):
    """
    Get the full built context as it would be passed to the LLM.
    """
    from main import get_app_state
    state = get_app_state()

    context = await state.context_manager.build_context_for_prompt(query)
    return context
