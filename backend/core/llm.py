"""
ARIA AI Engine Configuration
Sets up the AI client (Ollama or Gemini) for LLM inference.
"""
from ollama import AsyncClient as OllamaAsyncClient
from google import genai
from config.settings import settings
from utils.logger import get_logger

logger = get_logger(__name__)
_ai_client_instance = None

class GeminiClient:
    """Wrapper for Google Gemini API (google-genai SDK)."""
    def __init__(self):
        if not settings.gemini_api_key:
            logger.error("GEMINI_API_KEY is not set.")
            raise ValueError("GEMINI_API_KEY is required for Gemini provider.")
            
        self.client = genai.Client(api_key=settings.gemini_api_key)
        self.model_name = settings.gemini_model

    async def generate(self, prompt: str, system: str = None, model: str = None) -> str:
        try:
            target_model = model if model else self.model_name
            
            config = None
            if system:
                # In google-genai, system instructions are part of config
                config = {'system_instruction': system}

            # Asynchronous generation
            response = await self.client.aio.models.generate_content(
                model=target_model,
                contents=prompt,
                config=config
            )
            return response.text
        except Exception as e:
            logger.error(f"Gemini generation failed: {e}")
            raise

    async def chat(self, messages: list[dict], model: str = None) -> str:
        try:
            target_model = model if model else self.model_name
            
            # Convert OpenAI-style messages to Gemini history
            # User -> user, Assistant -> model
            chat_history = []
            system_instruction = None
            
            for msg in messages:
                role = msg['role']
                content = msg['content']
                
                if role == 'system':
                    system_instruction = content
                    continue
                
                gemini_role = 'user' if role == 'user' else 'model'
                chat_history.append({'role': gemini_role, 'parts': [{'text': content}]})

            # Debug: Verify context size
            print(f"DEBUG: Sending context with {len(chat_history)-1} past messages to Gemini.")

            # New SDK chat interface
            chat = self.client.aio.chats.create(
                model=target_model,
                history=chat_history[:-1], # all but last
                config={'system_instruction': system_instruction} if system_instruction else None
            )
            
            last_msg = chat_history[-1]['parts'][0]['text']
            response = await chat.send_message(last_msg)
            return response.text
        except Exception as e:
            logger.error(f"Gemini chat failed: {e}")
            raise

    async def get_available_models(self) -> list[str]:
        # Hardcoded list based on available models for the key
        return ["gemini-2.0-flash", "gemini-2.5-flash", "gemini-2.5-pro"]
        
    async def check_connection(self) -> bool:
        try:
            await self.generate("test")
            return True
        except Exception:
            return False


class OllamaClient:
    """Wrapper for Ollama AsyncClient."""
    def __init__(self):
        self.host = settings.ollama_host
        self.model = settings.ollama_model
        self.client = OllamaAsyncClient(host=self.host)

    async def get_available_models(self) -> list[str]:
        print(f"======== fetching available models =========")
        try:
            response = await self.client.list()
            if 'models' in response:
                return [model['model'] for model in response['models']]
            return []
        except Exception as e:
            logger.error(f"Ollama model list failed: {e}")
            return []

    async def chat(self, messages: list[dict], model: str = None) -> str:
        try:
            target_model = model if model else self.model
            response = await self.client.chat(model=target_model, messages=messages, stream=False)
            return response['message']['content']
        except Exception as e:
            logger.error(f"Ollama chat failed: {e}")
            raise

    async def generate(self, prompt: str, system: str = None, model: str = None) -> str:
        try:
            target_model = model if model else self.model
            response = await self.client.generate(model=target_model, prompt=prompt, system=system, stream=False)
            return response['response']
        except Exception as e:
            logger.error(f"Ollama generation failed: {e}")
            raise

    async def check_connection(self) -> bool:
        try:
            await self.client.list()
            return True
        except Exception as e:
            logger.error(f"Ollama connection check failed: {e}")
            return False


class AIClient:
    """Factory wrapper that delegates to the configured provider."""
    def __init__(self):
        self.provider = settings.ai_provider.lower()
        if self.provider == "gemini":
            self.client = GeminiClient()
            self.model = settings.gemini_model # expose for clients checking default
            self.host = "google-generativeai"
        else:
            self.client = OllamaClient()
            self.model = settings.ollama_model
            self.host = settings.ollama_host

    async def generate(self, prompt: str, system: str = None, model: str = None) -> str:
        return await self.client.generate(prompt, system, model)

    async def chat(self, messages: list[dict], model: str = None) -> str:
        return await self.client.chat(messages, model)
        
    async def get_available_models(self) -> list[str]:
        return await self.client.get_available_models()

    async def check_connection(self) -> bool:
        return await self.client.check_connection()


def get_ai_client() -> AIClient:
    """Returns a singleton AIClient."""
    global _ai_client_instance
    if _ai_client_instance is None:
        _ai_client_instance = AIClient()
    return _ai_client_instance
