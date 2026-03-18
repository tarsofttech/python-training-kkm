"""
Basic Text Generation with Ollama

This script demonstrates how to:
- Make HTTP requests to Ollama's API
- Send a prompt for text generation
- Handle the response and display results
"""

from operator import truediv
import httpx
import json
import os
from dotenv import load_dotenv

load_dotenv()

OLLAMA_HOST = os.getenv("OLLAMA_HOST", "http://localhost:11434")
MODEL_NAME = os.getenv("MODEL_NAME", "llama3.1")


def generate_text(prompt: str, model: str = MODEL_NAME) -> dict:
    """
    Generate text using Ollama's generate endpoint.
    
    Args:
        prompt: The text prompt to send to the model
        model: The model name to use (default from .env)
    
    Returns:
        dict: The full response from Ollama
    """
    url = f"{OLLAMA_HOST}/api/generate"
    
    payload = {
        "model": model,
        "prompt": prompt,
        "stream": False,
        "think": False
    }
    
    print(f"📤 Sending request to: {url}")
    print(f"📝 Prompt: {prompt}\n")
    
    try:
        response = httpx.post(url, json=payload, timeout=60.0)
        response.raise_for_status()
        
        result = response.json()
        
        print("✅ Response received!")
        print(f"📊 Model: {result.get('model', 'unknown')}")
        print(f"⏱️  Total duration: {result.get('total_duration', 0) / 1e9:.2f} seconds")
        print(f"🔢 Tokens generated: {result.get('eval_count', 0)}")
        print(f"\n💬 Generated text:\n{'-' * 80}")
        print(result.get('response', ''))
        print('-' * 80)
        
        return result
    
    except httpx.HTTPStatusError as e:
        print(f"❌ HTTP Error: {e}")
        print(f"   Status code: {e.response.status_code}")
        print(f"   Response: {e.response.text}")
        raise
    except httpx.RequestError as e:
        print(f"❌ Request Error: {e}")
        print(f"   Is Ollama running? Check with: curl {OLLAMA_HOST}/api/version")
        raise
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        raise


def main():
    """
    Main function to demonstrate basic text generation.
    """
    print("=" * 80)
    print("OLLAMA BASIC TEXT GENERATION")
    print("=" * 80)
    print(f"Using model: {MODEL_NAME}")
    print(f"Ollama host: {OLLAMA_HOST}\n")
    
    prompt = "Explain what a Large Language Model is in 2-3 sentences."
    
    result = generate_text(prompt)
    
    print("\n" + "=" * 80)
    print("💡 KEY OBSERVATIONS:")
    print("=" * 80)
    print("""
1. The response is non-streaming (stream=False)
   • We get the complete response at once
   • Easier to work with for simple use cases

2. Response includes metadata
   • total_duration: Time taken to generate
   • eval_count: Number of tokens generated
   • model: Confirms which model was used

3. The API is simple HTTP POST
   • No authentication needed (local only)
   • JSON request and response
   • Easy to integrate with any language
    """)
    
    print("\n🔬 TODO: Try these experiments:")
    print("   • Change the prompt to ask a different question")
    print("   • Try a different model (if you have others installed)")
    print("   • Add 'temperature' parameter to control randomness")
    print("   • Measure response time for different prompt lengths")


if __name__ == "__main__":
    main()
