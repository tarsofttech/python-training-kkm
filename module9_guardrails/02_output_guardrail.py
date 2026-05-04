import httpx
import re

def redact_pii(text: str) -> str:
    """
    Redacts sensitive information from text.
    For this example, we focus on Malaysian formats.
    """
    # Redact Malaysian NRIC (e.g., 900101-14-5555)
    nric_pattern = r'\b\d{6}-\d{2}-\d{4}\b'
    text = re.sub(nric_pattern, '[REDACTED NRIC]', text)
    
    # Redact generic Malaysian mobile numbers (e.g., 012-3456789)
    phone_pattern = r'\b01\d-\d{7,8}\b'
    text = re.sub(phone_pattern, '[REDACTED PHONE]', text)
    
    # Redact Emails
    email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
    text = re.sub(email_pattern, '[REDACTED EMAIL]', text)
    
    return text

def generate_safe_response(prompt: str):
    print(f"User Prompt: '{prompt}'\n")
    
    # 1. Ask the LLM to generate the output
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
        raw_output = response.json()["response"]
        
        print("⚠️ RAW OUTPUT (Pre-Guardrail):")
        print("-" * 40)
        print(raw_output)
        print("-" * 40)
        
        # 2. Apply Output Guardrail
        safe_output = redact_pii(raw_output)
        
        print("\n🛡️ SAFE OUTPUT (Post-Guardrail):")
        print("-" * 40)
        print(safe_output)
        print("-" * 40)

    except Exception as e:
        print(f"Error connecting to Ollama: {e}")

if __name__ == "__main__":
    print("--- 1. Testing PII Redaction Logic Directly ---")
    raw_text = "The suspect, Ahmad, can be reached at ahmad@gov.my or 012-9876543. His IC is 880101-14-5678."
    print(f"Original : {raw_text}")
    print(f"Redacted : {redact_pii(raw_text)}\n")
    
    print("--- 2. Testing Output Guardrail with LLM ---")
    # Instead of asking the 1B model to CREATE fake PII (which triggers its refusal),
    # we ask it to summarize a text that ALREADY has PII.
    test_prompt = """
    Please extract the user details exactly as written from this ticket:
    'User Ali (NRIC: 920303-10-5555) reported a bug. Contact him at 019-3334444 or ali.test@gmail.com.'
    """
    
    generate_safe_response(test_prompt)
