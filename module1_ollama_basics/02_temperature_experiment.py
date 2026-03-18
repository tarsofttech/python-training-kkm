"""
Module 1, Script 2: Temperature Experiment

This script demonstrates how the temperature parameter affects LLM output randomness.
Temperature controls how "creative" or "deterministic" the model's responses are.
"""

import httpx
import os
from dotenv import load_dotenv

load_dotenv()

OLLAMA_HOST = os.getenv("OLLAMA_HOST", "http://localhost:11434")
MODEL_NAME = os.getenv("MODEL_NAME", "llama3.1")


def generate_with_temperature(prompt: str, temperature: float, model: str = MODEL_NAME) -> str:
    """
    Generate text with a specific temperature setting.
    
    Args:
        prompt: The text prompt
        temperature: Controls randomness (0.0 = deterministic, 2.0 = very random)
        model: Model name to use
    
    Returns:
        str: Generated text
    """
    url = f"{OLLAMA_HOST}/api/generate"
    
    payload = {
        "model": model,
        "prompt": prompt,
        "stream": False,
        "options": {
            "temperature": temperature
        }
    }
    
    try:
        response = httpx.post(url, json=payload, timeout=120.0)
        response.raise_for_status()
        return response.json()["response"]
    except Exception as e:
        return f"Error: {str(e)}"


def main():
    """Run the same prompt with different temperature values."""
    
    prompt = "Write a creative tagline for a coffee shop."
    
    temperatures = [0.1, 0.7, 1.5]
    
    print("=" * 80)
    print("🌡️  TEMPERATURE EXPERIMENT")
    print("=" * 80)
    print(f"\n📝 Prompt: {prompt}\n")
    print("We'll run this prompt 3 times with different temperatures:\n")
    
    results = {}
    
    for temp in temperatures:
        print(f"🔄 Running with temperature = {temp}...")
        response = generate_with_temperature(prompt, temp)
        results[temp] = response
        print(f"   ✅ Done\n")
    
    print("=" * 80)
    print("📊 RESULTS COMPARISON")
    print("=" * 80)
    
    for temp in temperatures:
        print(f"\n{'─' * 80}")
        print(f"🌡️  Temperature: {temp}")
        print(f"{'─' * 80}")
        print(results[temp])
    
    print("\n" + "=" * 80)
    print("💡 WHAT YOU SHOULD NOTICE:")
    print("=" * 80)
    print("""
Temperature = 0.1 (Low):
  • More deterministic and focused
  • Similar output if you run it multiple times
  • Good for: factual answers, consistency, predictable outputs
  
Temperature = 0.7 (Medium):
  • Balanced between creativity and coherence
  • Some variation between runs
  • Good for: general conversation, balanced responses
  
Temperature = 1.5 (High):
  • More creative and varied
  • Very different outputs each time
  • Good for: creative writing, brainstorming, diverse ideas
  • Warning: May be less coherent or go off-topic
    """)
    
    print("\n🔬 TODO: Try running this script multiple times and observe:")
    print("   • Does the low temperature (0.1) give similar results each time?")
    print("   • Does the high temperature (1.5) give very different results?")
    print("   • Which temperature works best for your use case?")


if __name__ == "__main__":
    main()
