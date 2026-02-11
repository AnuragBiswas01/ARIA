import asyncio
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parents[1]))
from config.settings import settings
from google import genai

async def main():
    print(f"Using API Key: {settings.gemini_api_key[:5]}...")
    client = genai.Client(api_key=settings.gemini_api_key)
    
    print("Listing models...")
    found_model = None
    try:
        # Provide config if needed, but list() should work
        for m in client.models.list():
            print(f" - {m.name}")
            # Look for gemini-1.5-flash
            if "gemini-1.5-flash" in m.name:
                print(f"Found match: {m.name}")
                found_model = m.name
                break
    except Exception as e:
        print(f"Error listing: {e}")
        
    if found_model:
        print(f"Attempting generation with: {found_model}")
        try:
            response = await client.aio.models.generate_content(
                model=found_model,
                contents="Hello"
            )
            print(f"Success! Response: {response.text}")
        except Exception as e:
            print(f"Error generating: {e}")
    else:
        print("No matching model found to test.")

if __name__ == "__main__":
    asyncio.run(main())
