import httpx

# Define our guardrail configuration
# In a real government system, this list could be extensive or managed in a database.
BANNED_TOPICS = ["politics", "election", "crypto", "hack", "vote"]

def check_input_guardrail(prompt: str) -> bool:
    """Returns True if the prompt is safe, False if it violates guardrails."""
    prompt_lower = prompt.lower()
    for topic in BANNED_TOPICS:
        if topic in prompt_lower:
            return False
    return True

def generate_response(prompt: str):
    print(f"User Prompt: '{prompt}'")
    
    # 1. Apply Input Guardrail
    if not check_input_guardrail(prompt):
        print(f"🛑 GUARDRAIL TRIGGERED: Request blocked. Topic is restricted by agency policy.\n")
        return

    # 2. Proceed to LLM if safe
    print("✅ Input passed guardrails. Generating response...")
    try:
        response = httpx.post(
            "http://localhost:11434/api/generate",
            json={
                "model": "llama3.2:1b",
                "prompt": prompt,
                "stream": False
            },
            timeout=30.0
        )
        print(f"🤖 AI: {response.json()['response']}\n")
    except Exception as e:
        print(f"Error connecting to Ollama: {e}")

if __name__ == "__main__":
    print("--- Testing Safe Prompt ---")
    generate_response("How do I renew my passport at the immigration office?")
    
    print("--- Testing Unsafe Prompt ---")
    generate_response("Who should I vote for in the next general election?")
