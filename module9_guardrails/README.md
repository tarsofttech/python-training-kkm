# Module 9: AI Guardrails

Learn how to implement safety boundaries around your LLM applications. This module covers how to intercept, evaluate, and filter both user inputs and LLM outputs to ensure government applications remain secure, on-topic, and compliant.

---

## What You'll Learn

- **Input Guardrails**: Filtering malicious or off-topic prompts before they hit the LLM.
- **Output Guardrails**: Redacting sensitive Personal Identifiable Information (PII) before showing the response.
- **LLM-as-a-Judge**: Using the LLM itself to evaluate the safety and context of a prompt.

---

## Prerequisites

1. **Ollama installed and running**
2. **Required models pulled**
   ```bash
   ollama pull llama3.1
   ```

---

## Setup

```bash
# Create .env file
cp .env.example .env

# Run scripts directly (uv run handles dependencies like httpx)
uv run python 01_input_guardrail.py
uv run python 02_output_guardrail.py
uv run python 03_llm_as_judge_guardrail.py
uv run python 04_input_pii_redaction.py
```

---

## Scripts

### 01_input_guardrail.py
Demonstrates rule-based input filtering.

```bash
uv run python 01_input_guardrail.py
```
**What it does:**
- Uses a predefined list of banned topics (e.g., politics, elections).
- Checks the user's prompt *before* making the API call.
- Blocks the request entirely if a violation is detected, saving compute costs and preventing off-topic generations.

### 02_output_guardrail.py
Demonstrates output redaction (PII Masking).

```bash
uv run python 02_output_guardrail.py
```
**What it does:**
- Allows the LLM to generate a response.
- Uses Regular Expressions (Regex) to scan the raw output for sensitive data (like Malaysian NRICs and phone numbers).
- Replaces the sensitive data with `[REDACTED NRIC]` before the final user sees it.

### 03_llm_as_judge_guardrail.py
Demonstrates using a secondary LLM as a security filter.

```bash
uv run python 03_llm_as_judge_guardrail.py
```
**What it does:**
- Sends the user's prompt to a "Judge LLM" with a strict system prompt.
- The Judge evaluates if the prompt is a jailbreak attempt or violates government safety policies.
- Only proceeds to answer if the Judge returns "SAFE".

### 04_input_pii_redaction.py
Demonstrates sanitizing citizen data *before* it reaches the LLM.

```bash
uv run python 04_input_pii_redaction.py
```
**What it does:**
- Scans the user's input prompt for sensitive data (NRIC, emails, etc.).
- Strips and replaces the data with placeholders.
- Sends the *sanitized* prompt to the LLM, ensuring the AI never processes real citizen data. This is critical when using external/cloud LLMs.

---

## Key Concepts

### Why Guardrails are Non-Negotiable for Government Systems
1. **Data Privacy (PDPA Compliance)**: Preventing citizen data from leaking through AI chats.
2. **Reputational Risk**: Ensuring the AI does not generate inappropriate, biased, or politically sensitive statements.
3. **Resource Protection**: Blocking prompt-injection attacks that try to use government servers for unrelated tasks.

### Where Guardrails Sit in the Architecture
```text
User Request -> [Input Guardrail] -> LLM Generation -> [Output Guardrail] -> Final Response
                     |                                         |
               (Blocks if Bad)                         (Masks/Filters PII)
```

---

## Experimentation Ideas

- **Advanced PII Regex**: Expand the output guardrail to catch emails, credit cards, or internal government file references.
- **Tone Guardrail**: Write an output guardrail that uses `llm_judge` to ensure the response sounds formal and professional.
- **Integrate with FastAPI**: Try turning these scripts into FastAPI dependency injections so they automatically protect all your endpoints.
