import asyncio
import sys
from pathlib import Path

# Add backend to path
sys.path.insert(0, str(Path(__file__).parents[1]))

from core.llm import AIClient

async def run_chat_session():
    # Debug info
    from config.settings import settings
    print(f"DEBUG: AI_PROVIDER={settings.ai_provider}")
    print(f"DEBUG: GEMINI_API_KEY={settings.gemini_api_key[:5]}..." if settings.gemini_api_key else "DEBUG: GEMINI_API_KEY=None")
    
    client = AIClient()
    print(f"DEBUG: Initialized client for provider: {client.provider}")
    
    # Get available models and let user choose, or default
    try:
        models = await client.get_available_models()
    except Exception as e:
        print(f"Error fetching models: {e}")
        models = []
    selected_model = client.model # Default from env
    
    print("\nAvailable Models:")
    for i, m in enumerate(models):
        print(f"{i+1}. {m}")
    
    choice = input(f"\nSelect model (default: {selected_model}): ")
    if choice.isdigit() and 1 <= int(choice) <= len(models):
        selected_model = models[int(choice)-1]
    
    print(f"\nStarting chat with {selected_model}...")
    print("Type 'exit' or 'quit' to stop.\n")
    
    # Initialize chat history
    history = []
    
    # Optional: Add a system prompt
    system_prompt = "You are ARIA, a helpful AI assistant."
    history.append({'role': 'system', 'content': system_prompt})
    
    while True:
        user_input = input("You: ")
        if user_input.lower() in ['exit', 'quit']:
            break
            
        # Add user message to history
        history.append({'role': 'user', 'content': user_input})
        
        print("ARIA: ", end="", flush=True)
        try:
            # Send entire history to context
            response_content = await client.chat(messages=history, model=selected_model)
            print(response_content)
            
            # Add assistant response to history
            history.append({'role': 'assistant', 'content': response_content})
            
        except Exception as e:
            print(f"\nError: {e}")
            break

if __name__ == "__main__":
    try:
        asyncio.run(run_chat_session())
    except KeyboardInterrupt:
        print("\nChat finished.")
