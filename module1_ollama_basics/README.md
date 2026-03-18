# Module 1: Ollama Basics

Learn how to interact with Ollama directly using Python and the httpx library. This module covers the fundamentals of calling Ollama's REST API, understanding tokens, temperature settings, embeddings, and prompt engineering.

---

## What You'll Learn

- How to call Ollama's `/api/generate` endpoint using httpx
- The effect of temperature on LLM output randomness
- How to generate embeddings using `nomic-embed-text`
- Building a reusable prompt template library

---

## Prerequisites

1. **Ollama installed and running**
   ```bash
   # Check if Ollama is running
   curl http://localhost:11434/api/version
   ```

2. **Required models pulled**
   ```bash
   ollama pull llama3.1
   ollama pull nomic-embed-text
   ```

---

## Setup

### Option 1: Using uv run (Simplest - Zero setup!)

```bash
# Just create .env and run!
cp .env.example .env

# Run any script - uv handles everything automatically
uv run python 01_basic_generate.py
uv run python 02_temperature_experiment.py
uv run python 03_embeddings.py
uv run python 04_prompt_library.py
```

**💡 This is the easiest way!** `uv run` automatically creates a virtual environment and installs dependencies on first run.

### Option 2: Using uv sync (If you want a persistent venv)

```bash
# Create .env file
cp .env.example .env

# One command to create venv + install everything
uv sync

# Then run scripts normally
uv run python 01_basic_generate.py
# Or activate and run without uv
source .venv/bin/activate
python 01_basic_generate.py
```

### Option 3: Using pip (Traditional)

```bash
# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -e .

# Create .env file
cp .env.example .env

# Run scripts
python 01_basic_generate.py
```

---

## Scripts

### 01_basic_generate.py
Basic text generation using Ollama's generate endpoint.

```bash
python 01_basic_generate.py
```

**What it does:**
- Sends a simple prompt to Ollama
- Uses `stream=False` to get the complete response at once
- Prints the full response with explanations

### 02_temperature_experiment.py
Demonstrates how temperature affects output randomness.

```bash
python 02_temperature_experiment.py
```

**What it does:**
- Runs the same prompt 3 times with different temperatures (0.1, 0.7, 1.5)
- Shows side-by-side comparison of outputs
- Helps you understand when to use low vs high temperature

### 03_embeddings.py
Generate vector embeddings for text.

```bash
python 03_embeddings.py
```

**What it does:**
- Calls Ollama's embeddings endpoint
- Shows the first 10 values of the embedding vector
- Explains what embeddings are and why they're useful

### 04_prompt_library.py
Reusable prompt templates for different use cases.

```bash
python 04_prompt_library.py
```

**What it does:**
- Demonstrates 4 different prompt patterns:
  - System HR Assistant (role-based prompting)
  - Concise responses (output control)
  - Few-shot Q&A (learning from examples)
  - Structured JSON output (formatted responses)

---

## Sample Data

- `data/sample_questions.txt` - 10 HR-related questions for testing

---

## Key Concepts

### Temperature
- **Low (0.1-0.3)**: Deterministic, focused, consistent
- **Medium (0.7-0.9)**: Balanced creativity and coherence
- **High (1.0-2.0)**: Creative, varied, less predictable

### Embeddings
Vector representations of text that capture semantic meaning. Used for:
- Similarity search
- Clustering
- Classification
- RAG (Retrieval-Augmented Generation)

### Prompt Engineering
Crafting effective prompts to get better LLM outputs:
- System prompts (set behavior/role)
- Few-shot examples (teach by example)
- Output formatting (JSON, lists, etc.)

---

## Troubleshooting

**Connection refused:**
```bash
# Make sure Ollama is running
ollama serve
```

**Model not found:**
```bash
# Pull the required models
ollama pull llama3.1
ollama pull nomic-embed-text
```

---

## Next Steps

After completing this module, proceed to **Module 2: FastAPI Foundations** to learn how to build a structured API server.

---

## Experimentation Ideas

- Try different models (e.g., `llama2`, `mistral`)
- Experiment with different temperature values
- Create your own prompt templates
- Compare embeddings of similar vs different texts
