import asyncio
import sys
from pathlib import Path
# Add backend to path to import config
sys.path.insert(0, str(Path(__file__).parents[1]))
from config.settings import settings
from google import genai

# Get key from settings
api_key = settings.gemini_api_key
if not api_key:
    print("WARNING: GEMINI_API_KEY not found in settings.")

print(f"Python version: {sys.version}")
try:
    import google.genai
    print(f"google.genai imported successfully.")
    # Attempt to print version if available
    try:
        print(f"google.genai version: {google.genai.__version__}")
    except AttributeError:
        print("google.genai version not found in __version__")
except ImportError as e:
    print(f"Failed to import google.genai: {e}")
    sys.exit(1)

async def test_generation():
    if not api_key:
        print("Skipping generation test due to missing API key.")
        return

    client = genai.Client(api_key=api_key)
    
    print("\nListing available models...")
    try:
        # Pager is iterable
        for m in client.models.list():
            if "gemini" in m.name:
                print(f" - {m.name}")
    except Exception as e:
        print(f"Failed to list models: {e}")

    models_to_test = ["gemini-1.5-flash", "models/gemini-1.5-flash", "gemini-2.0-flash-exp"]
    
    for model in models_to_test:
        print(f"\nTesting model: {model}")
        try:
            response = await client.aio.models.generate_content(
                model=model,
                contents="Hello, this is a test."
            )
            print(f"Success! Response: {response.text[:50]}...")
            return # Exit after first success
        except Exception as e:
            print(f"Failed: {e}")

if __name__ == "__main__":
    asyncio.run(test_generation())
