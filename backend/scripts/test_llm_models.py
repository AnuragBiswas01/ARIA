import asyncio
import sys
from pathlib import Path

# Add backend to path
sys.path.insert(0, str(Path(__file__).parents[1]))

from core.llm import AIClient

async def test_get_models():
    print("Initializing AI Client...")
    try:
        client = AIClient()
        print(f"Configured Host: {client.host}")
        
        print("Fetching available models...")
        models = await client.get_available_models()
        
        print("\nAvailable Ollama Models:")
        if models:
            for model in models:
                print(f" - {model}")
        else:
            print("No models found or list failed.")
            
    except Exception as e:
        print(f"Client init failed: {e}")

async def test_generate():
    print("\n" + "="*50)
    print("Testing Generation...")
    print("="*50)
    
    try:
        # 'self' is implicit when you create an instance
        client = AIClient() 
        
        # 'system': Sets the behavior/persona
        system_instruction = "You are a helpful assistant who speaks like a professional."
        print(f"\nSystem Instruction: {system_instruction}")
        
        # 'prompt': The specific request
        prompt = "Explain what is time."
        print(f"User Prompt: {prompt}")
        
        print("\nGenerating response...")
        response = await client.generate(prompt=prompt, system=system_instruction)
        print(f"\nResponse:\n{response}")

        # Test 3: Specific Model (Optional)
        # Check available models first to avoid error
        models = await client.get_available_models()
        if models:
            target_model = models[0] # Pick the first available one
            print(f"\nTesting with specific model: {target_model}")
            response = await client.generate(prompt="Say hello!", model=target_model)
            print(f"Response from {target_model}: {response}")
        
    except Exception as e:
        print(f"Generation failed: {e}")

if __name__ == "__main__":
    asyncio.run(test_get_models())
    asyncio.run(test_generate())
