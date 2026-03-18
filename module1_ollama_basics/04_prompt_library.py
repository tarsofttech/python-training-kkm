"""
Module 1, Script 4: Prompt Library and Template Patterns

This script demonstrates different prompt engineering patterns that you can reuse
across your projects. Each pattern serves a different purpose and produces
different types of outputs.
"""

import httpx
import os
from dotenv import load_dotenv

load_dotenv()

OLLAMA_HOST = os.getenv("OLLAMA_HOST", "http://localhost:11434")
MODEL_NAME = os.getenv("MODEL_NAME", "llama3.1")


PROMPT_TEMPLATES = {
    "system_hr_assistant": {
        "description": "Role-based prompting - set the LLM's behavior and expertise",
        "system": "You are an expert HR assistant with 10 years of experience in employee relations and company policies. You provide clear, professional, and empathetic responses to HR-related questions.",
        "template": "{question}"
    },
    
    "system_concise": {
        "description": "Output control - force brief, focused responses",
        "system": "You are a helpful assistant. Always respond in exactly 2-3 sentences. Be direct and concise.",
        "template": "{question}"
    },
    
    "few_shot_qa": {
        "description": "Few-shot learning - teach by example",
        "system": "",
        "template": """Answer the question based on the pattern shown in the examples.

        Example 1:
        Q: What is the capital of France?
        A: The capital of France is Paris.

        Example 2:
        Q: What is the capital of Japan?
        A: The capital of Japan is Tokyo.

        Example 3:
        Q: What is the capital of Brazil?
        A: The capital of Brazil is Brasília.

        Now answer this question:
        Q: {question}
        A:"""
    },
    
    "structured_json_output": {
        "description": "Structured output - get responses in JSON format",
        "system": "You are a helpful assistant that always responds in valid JSON format.",
        "template": """Analyze the following question and provide a response in this exact JSON format:
    {{
        "question": "{question}",
        "answer": "your answer",
        "confidence": "high/medium/low",
        "category": "the topic category"
    }}

    JSON Response:"""
    }
}


def generate_with_template(template_name: str, question: str) -> str:
    """
    Generate a response using a specific prompt template.
    
    Args:
        template_name: Name of the template from PROMPT_TEMPLATES
        question: The user's question to insert into the template
    
    Returns:
        str: The generated response
    """
    if template_name not in PROMPT_TEMPLATES:
        return f"Error: Template '{template_name}' not found"
    
    template = PROMPT_TEMPLATES[template_name]
    prompt = template["template"].format(question=question)
    
    url = f"{OLLAMA_HOST}/api/generate"
    
    payload = {
        "model": MODEL_NAME,
        "prompt": prompt,
        "stream": False
    }
    
    if template["system"]:
        payload["system"] = template["system"]
    
    try:
        response = httpx.post(url, json=payload, timeout=120.0)
        response.raise_for_status()
        return response.json()["response"]
    except Exception as e:
        return f"Error: {str(e)}"


def main():
    """Demonstrate all prompt templates with the same question."""
    
    question = "How many vacation days do new employees get?"
    
    print("=" * 80)
    print("📚 PROMPT LIBRARY DEMONSTRATION")
    print("=" * 80)
    print(f"\n📝 Question: {question}\n")
    print("We'll ask the same question using 4 different prompt patterns:\n")
    
    for i, (template_name, template_info) in enumerate(PROMPT_TEMPLATES.items(), 1):
        print("=" * 80)
        print(f"Pattern {i}: {template_name.upper().replace('_', ' ')}")
        print("=" * 80)
        print(f"💡 Purpose: {template_info['description']}\n")
        
        if template_info['system']:
            print(f"🎭 System Prompt:")
            print(f"   {template_info['system']}\n")
        
        print(f"🔄 Generating response...")
        response = generate_with_template(template_name, question)
        
        print(f"\n🤖 Response:")
        print("─" * 80)
        print(response)
        print("─" * 80)
        print()
    
    print("\n" + "=" * 80)
    print("💡 KEY TAKEAWAYS:")
    print("=" * 80)
    print("""
1. SYSTEM PROMPTS (Role-Based):
   • Set the LLM's persona, expertise, and behavior
   • Great for: customer service bots, domain experts, specific tones
   • Example: "You are a professional HR assistant..."

2. OUTPUT CONTROL (Concise):
   • Control response length, format, or style
   • Great for: UI constraints, quick answers, summaries
   • Example: "Always respond in 2-3 sentences"

3. FEW-SHOT LEARNING (Examples):
   • Teach the LLM by showing examples
   • Great for: specific formats, patterns, consistent structure
   • Example: Show 3 Q&A pairs, then ask a new question

4. STRUCTURED OUTPUT (JSON):
   • Get responses in a specific data format
   • Great for: APIs, data processing, structured data extraction
   • Example: "Respond in JSON format with these fields..."
    """)
    
    print("\n🔬 TODO: Experiment with these ideas:")
    print("   • Create a 'system_technical_writer' template for documentation")
    print("   • Make a few-shot template for sentiment analysis")
    print("   • Build a JSON template that extracts dates and names from text")
    print("   • Combine multiple patterns (e.g., system + few-shot)")
    
    print("\n📖 BEST PRACTICES:")
    print("   ✅ Be specific and clear in your instructions")
    print("   ✅ Use examples when you want consistent formatting")
    print("   ✅ Test different temperatures for different use cases")
    print("   ✅ Save successful prompts in a library for reuse")
    print("   ❌ Don't make prompts too long or complex")
    print("   ❌ Don't assume the LLM knows your specific context")


if __name__ == "__main__":
    main()
