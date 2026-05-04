import httpx
import re

def redact_pii(text: str) -> str:
    """
    Redacts sensitive information from text BEFORE it goes to the LLM.
    """
    # Redact Malaysian NRIC
    nric_pattern = r'\b\d{6}-\d{2}-\d{4}\b'
    text = re.sub(nric_pattern, '[REDACTED NRIC]', text)
    
    # Redact generic Malaysian mobile numbers
    phone_pattern = r'\b01\d-\d{7,8}\b'
    text = re.sub(phone_pattern, '[REDACTED PHONE]', text)
    
    # Redact Emails
    email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
    text = re.sub(email_pattern, '[REDACTED EMAIL]', text)
    
    return text

def generate_with_anonymized_input(prompt: str):
    print("👤 ORIGINAL USER PROMPT (Contains PII):")
    print("-" * 40)
    print(prompt)
    print("-" * 40, "\n")
    
    # 1. Apply Input Guardrail (Redaction BEFORE sending to LLM)
    safe_prompt = redact_pii(prompt)
    
    print("🛡️ SANITIZED PROMPT (What the LLM actually sees):")
    print("-" * 40)
    print(safe_prompt)
    print("-" * 40, "\n")
    
    # 2. Send the SANITIZED prompt to the LLM
    try:
        print("⏳ Generating response from Ollama...\n")
        response = httpx.post(
            "http://localhost:11434/api/generate",
            json={
                "model": "llama3.2:1b",
                "prompt": safe_prompt,
                "stream": False
            },
            timeout=30.0
        )
        llm_output = response.json()["response"]
        
        print("🤖 LLM RESPONSE:")
        print("-" * 40)
        print(llm_output)
        print("-" * 40)

    except Exception as e:
        print(f"Error connecting to Ollama: {e}")

if __name__ == "__main__":
    print("--- Testing Input PII Redaction ---\n")
    
    test_prompt = """
    Hello, my name is Siti. I am having trouble logging into the government portal.
    Can you check my tax status? My IC number is 880202-14-5566 and my email is siti.tax@gmail.com.
    """
    
    generate_with_anonymized_input(test_prompt)
