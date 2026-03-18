# FastAPI + Local LLM Training Lab

A comprehensive 2-day Python training course for building RAG (Retrieval-Augmented Generation) applications using **FastAPI**, **Ollama**, **LlamaIndex**, and **FAISS** — all running locally without any cloud API keys.

This is a **learning project** designed for beginner-to-intermediate developers. Every module prioritizes clarity, simplicity, and readability over performance or scalability.

---

## Prerequisites

Before starting, ensure you have the following installed:

- **Python 3.11+** — [Download here](https://www.python.org/downloads/)
- **uv** (recommended) or pip — [Install uv](https://github.com/astral-sh/uv)
- **Ollama** — [Install from ollama.ai](https://ollama.ai)
- **Docker Desktop** (for Module 8 only) — [Download here](https://www.docker.com/products/docker-desktop)

---

## Quick Setup

### 1. Install uv (Recommended Package Manager)

```bash
# Install uv (fast Python package manager)
curl -LsSf https://astral.sh/uv/install.sh | sh

# Or on macOS with Homebrew
brew install uv

# Or on Windows with PowerShell
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"

# Verify installation
uv --version
```

### 2. Install Ollama and Pull Required Models

```bash
# Install Ollama first (see https://ollama.ai)

# Pull the LLM model (llama3.1)
ollama pull llama3.1

# Pull the embedding model (nomic-embed-text)
ollama pull nomic-embed-text

# Verify Ollama is running
curl http://localhost:11434/api/version

# Check Ollama logs
log stream --predicate 'process == "ollama"'
```


### 3. Clone This Repository

```bash
git clone <your-repo-url>
cd fastapi-llm-training
```

---

## Course Modules

This repository contains 8 progressive modules, each building on the previous ones:

| Module | Name | Description |
|--------|------|-------------|
| **1** | `module1_ollama_basics` | Interact with Ollama via Python using httpx. Learn about tokens, temperature, embeddings, and prompt templates. |
| **2** | `module2_fastapi_foundations` | Build a structured FastAPI app with Pydantic v2 schemas, routing, CORS middleware, and Swagger docs. |
| **3** | `module3_fastapi_ollama` | Connect FastAPI to Ollama. Implement both standard and streaming LLM responses with proper error handling. |
| **4** | `module4_document_ingestion` | Load and chunk documents using LlamaIndex. Experiment with different chunking strategies and metadata. |
| **5** | `module5_rag_pipeline` | Build the complete RAG pipeline: embed documents, store in FAISS, and query with source attribution. |
| **6** | `module6_chat_memory` | Add multi-turn conversation support with session-based memory and metadata filtering. |
| **7** | `module7_evaluation` | Evaluate RAG quality using faithfulness and relevancy metrics. Build a test harness with automated evaluation. |
| **8** | `module8_docker` | Containerize the complete application using Docker and Docker Compose for easy deployment. |

---

## How to Run Each Module

Each module is self-contained with its own dependencies and instructions. Navigate to any module directory and follow these steps:

### Option 1: Using uv sync (Recommended - Simplest!)

```bash
# Example: Running Module 1
cd module1_ollama_basics

# One command to create venv + install everything!
uv sync

# Run a script
uv run python 01_basic_generate.py
```

For FastAPI modules (2, 3, 4, 5, 6, 7, 8), start the server with:

```bash
# Example: Running Module 2
cd module2_fastapi_foundations

# One command setup
uv sync

# Start the FastAPI server
uv run uvicorn main:app --reload

# Access Swagger docs at http://localhost:8000/docs
```

### Option 2: Using pip (Traditional)

```bash
# Example: Running Module 1
cd module1_ollama_basics

# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -e .

# Run a script
python 01_basic_generate.py
```

### Option 3: Using uv run (Zero setup - Just run!)

```bash
# Example: Running Module 1
cd module1_ollama_basics

# No setup needed - uv handles everything automatically!
uv run python 01_basic_generate.py

# For FastAPI modules
cd module2_fastapi_foundations
uv run uvicorn main:app --reload
```

**💡 Tip**: `uv run` is the fastest way - it automatically creates a venv, installs dependencies, and runs your script. No `uv sync` or activation needed!

---

## Module Dependencies

Modules build progressively on each other:

- **Modules 1-2**: Standalone, no dependencies
- **Module 3**: Uses concepts from Module 2
- **Module 4**: Uses concepts from Module 3
- **Module 5**: Combines code from Modules 3 and 4
- **Module 6**: Extends Module 5
- **Module 7**: Extends Module 5/6
- **Module 8**: Complete application from Module 5/6

---

## Tech Stack

| Layer | Tool |
|-------|------|
| **Language** | Python 3.11+ |
| **API Framework** | FastAPI + Uvicorn |
| **LLM Runtime** | Ollama (local, http://localhost:11434) |
| **LLM Model** | llama3.1 |
| **Embedding Model** | nomic-embed-text (via Ollama) |
| **RAG Framework** | LlamaIndex |
| **Vector Store** | FAISS (faiss-cpu) |
| **Validation** | Pydantic v2 |
| **HTTP Client** | httpx |
| **PDF Parsing** | pypdf, pdfplumber |
| **Containerization** | Docker + Docker Compose |

---

## Learning Approach

This is a **hands-on lab project**. Each module contains:

- ✅ **Complete working solution code** (no placeholders)
- ✅ **Detailed inline comments** explaining what each part does
- ✅ **README with instructions** on how to run the module
- ✅ **Sample data files** for testing
- ✅ **TODO comments** encouraging you to experiment and extend

---

## Troubleshooting

### Ollama Connection Issues

If you see errors about connecting to Ollama:

```bash
# Check if Ollama is running
curl http://localhost:11434/api/version

# If not running, start Ollama
ollama serve
```

### Port Already in Use

If port 8000 is already in use:

```bash
# Use a different port
uvicorn main:app --reload --port 8001
```

### Module Not Found Errors

Make sure you've installed the module dependencies:

```bash
pip install -e .
```

---

## Project Structure

```
fastapi-llm-training/
│
├── README.md                          # This file
├── .gitignore                         # Python, venv, FAISS indices
│
├── module1_ollama_basics/             # Direct Ollama API interaction
├── module2_fastapi_foundations/       # FastAPI basics with Pydantic
├── module3_fastapi_ollama/            # FastAPI + Ollama integration
├── module4_document_ingestion/        # Document loading and chunking
├── module5_rag_pipeline/              # Complete RAG with FAISS
├── module6_chat_memory/               # Multi-turn conversations
├── module7_evaluation/                # RAG quality evaluation
└── module8_docker/                    # Docker deployment
```

---

## Contributing

This is a training project. Feel free to:

- Experiment with different models
- Try different chunking strategies
- Add new endpoints
- Improve error handling
- Extend the evaluation metrics

---

## License

This project is for educational purposes. Use it freely for learning and teaching.

---

## Support

For questions or issues:

1. Check the module-specific README
2. Review the inline code comments
3. Consult the [LlamaIndex documentation](https://docs.llamaindex.ai)
4. Check the [FastAPI documentation](https://fastapi.tiangolo.com)
5. Visit the [Ollama documentation](https://ollama.ai/docs)

---

**Happy Learning! 🚀**
