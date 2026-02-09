"""
ARIA Chat API Routes
Handles chat interactions with the AI.
"""
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import StreamingResponse
import uuid
import json

from api.models.requests import ChatRequest
from api.models.responses import ChatResponse
from utils.logger import get_logger

logger = get_logger(__name__)

router = APIRouter(prefix="/chat", tags=["Chat"])


# Dependency injection will be set up in main.py
# For now, these are placeholders that will be replaced


@router.post("", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """
    Send a message to ARIA and get a response.
    """
    from main import get_app_state
    state = get_app_state()

    session_id = request.session_id or str(uuid.uuid4())

    # Add user message to context
    state.context_manager.add_to_working_memory("user", request.message)

    # Get context for prompt
    context = await state.context_manager.build_context_for_prompt(request.message)

    # Generate response
    try:
        response_text = await state.ai_engine.generate(
            prompt=request.message,
            context=context.get("working_memory", []),
            stream=False,
        )
    except Exception as e:
        logger.error(f"AI generation error: {e}")
        raise HTTPException(status_code=503, detail="AI service unavailable")

    # Parse for tool calls
    tool_calls = state.tool_parser.parse(response_text)
    tool_results = []

    # Execute tool calls
    for call in tool_calls:
        result = await state.tool_executor.execute(call["tool"], call["parameters"])
        tool_results.append(result)

    # Add assistant response to context
    state.context_manager.add_to_working_memory("assistant", response_text)

    return ChatResponse(
        response=response_text,
        session_id=session_id,
        tool_calls=tool_calls if tool_calls else None,
        tool_results=tool_results if tool_results else None,
    )


@router.post("/stream")
async def chat_stream(request: ChatRequest):
    """
    Stream a response from ARIA.
    """
    from main import get_app_state
    state = get_app_state()

    session_id = request.session_id or str(uuid.uuid4())
    state.context_manager.add_to_working_memory("user", request.message)
    context = await state.context_manager.build_context_for_prompt(request.message)

    async def generate():
        full_response = ""
        try:
            async for chunk in await state.ai_engine.generate(
                prompt=request.message,
                context=context.get("working_memory", []),
                stream=True,
            ):
                full_response += chunk
                yield f"data: {json.dumps({'chunk': chunk})}\n\n"

            # After streaming, add to memory
            state.context_manager.add_to_working_memory("assistant", full_response)
            yield f"data: {json.dumps({'done': True, 'session_id': session_id})}\n\n"

        except Exception as e:
            logger.error(f"Stream error: {e}")
            yield f"data: {json.dumps({'error': str(e)})}\n\n"

    return StreamingResponse(generate(), media_type="text/event-stream")
