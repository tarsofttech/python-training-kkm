# Module 3: FastAPI + Ollama Integration

Learn how to connect FastAPI to Ollama for both standard and streaming LLM responses. This module covers async HTTP clients, error handling, and Server-Sent Events (SSE) for streaming.

---

## What You'll Learn

- Creating an async Ollama client with httpx
- Implementing standard (non-streaming) LLM generation
- Implementing streaming responses with Server-Sent Events (SSE)
- Proper error handling for external service dependencies
- Health checks for service availability
- Using FastAPI's lifespan for client initialization

---

## Prerequisites

1. **Ollama installed and running**
   ```bash
   ollama serve
   ```

2. **Required models pulled**
   ```bash
   ollama pull llama3.1
   ollama pull nomic-embed-text
   ```

3. **Completed Module 2** (FastAPI Foundations)

---

## Setup

1. **Install dependencies**
   ```bash
   pip install -e .
   ```

2. **Create .env file**
   ```bash
   cp .env.example .env
   ```

3. **Start the server**
   ```bash
   uvicorn main:app --reload
   ```

4. **Access the API**
   - Swagger UI: http://localhost:8000/docs
   - Health check: http://localhost:8000/api/v1/health

---

## Project Structure

```
module3_fastapi_ollama/
├── main.py              # FastAPI app with Ollama client initialization
├── schemas.py           # Extended Pydantic models from Module 2
├── ollama_client.py     # Async Ollama client with streaming support
├── routers/
│   └── generate.py      # Generation endpoints (standard & streaming)
└── data/
    └── test_prompts.txt # Sample prompts for testing
```

---

## API Endpoints

### GET /api/v1/health
Check if the API and Ollama are both healthy.

**Response:**
```json
{
  "status": "healthy",
  "ollama_reachable": true
}
```

### POST /api/v1/generate
Generate text using Ollama (standard or streaming).

**Request:**
```json
{
  "prompt": "Explain quantum computing in simple terms",
  "system": "You are a helpful science teacher",
  "temperature": 0.7,
  "stream": false
}
```

**Response (stream=false):**
```json
{
  "text": "Quantum computing is...",
  "model": "llama3.1",
  "duration_ms": 1234
}
```

**Response (stream=true):**
Server-Sent Events stream:
```
data: Quantum
data: computing
data: is
...
```

---

## Key Concepts

### Async HTTP Client
Using httpx.AsyncClient for non-blocking requests:

```python
async with httpx.AsyncClient(timeout=120.0) as client:
    response = await client.post(url, json=payload)
```

### Streaming Responses
FastAPI's StreamingResponse with Server-Sent Events:

```python
from fastapi.responses import StreamingResponse

async def generate_stream():
    async for chunk in ollama_client.generate_stream(prompt):
        yield f"data: {chunk}\n\n"

return StreamingResponse(generate_stream(), media_type="text/event-stream")
```

### Error Handling
Proper HTTP status codes for different error types:

- **503 Service Unavailable**: Ollama is not reachable
- **422 Unprocessable Entity**: Invalid request data (Pydantic validation)
- **500 Internal Server Error**: Unexpected errors

### Lifespan Management
Initialize the Ollama client once on startup:

```python
@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.ollama = OllamaClient(...)
    yield
```

---

## Testing the API

### Standard Generation (curl)

```bash
curl -X POST http://localhost:8000/api/v1/generate \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "What is FastAPI?",
    "temperature": 0.7,
    "stream": false
  }'
```

### Streaming Generation (curl)

```bash
curl -X POST http://localhost:8000/api/v1/generate \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "Write a short story about a robot",
    "temperature": 0.9,
    "stream": true
  }'
```

### Using Python

```python
import httpx

# Standard generation
response = httpx.post(
    "http://localhost:8000/api/v1/generate",
    json={
        "prompt": "Explain machine learning",
        "stream": False
    },
    timeout=120.0
)
print(response.json())

# Streaming generation
with httpx.stream(
    "POST",
    "http://localhost:8000/api/v1/generate",
    json={
        "prompt": "Tell me a joke",
        "stream": True
    },
    timeout=120.0
) as response:
    for line in response.iter_lines():
        if line.startswith("data: "):
            print(line[6:], end="", flush=True)
```

---

## OllamaClient Methods

### `async def generate(prompt, system, temperature, stream) -> str`
Generate text with Ollama (non-streaming).

### `async def generate_stream(prompt, system) -> AsyncGenerator[str, None]`
Generate text with streaming (yields chunks).

### `async def embed(text: str) -> List[float]`
Generate embeddings for text.

### `async def health_check() -> bool`
Check if Ollama is reachable.

---

## Common Issues

### Ollama not running
```bash
# Start Ollama
ollama serve

# Or check if it's already running
curl http://localhost:11434/api/version
```

### Timeout errors
Increase the timeout in ollama_client.py if generating long responses:
```python
httpx.AsyncClient(timeout=300.0)  # 5 minutes
```

### Streaming not working
Make sure your HTTP client supports Server-Sent Events (SSE).

---

## Next Steps

After completing this module, proceed to **Module 4: Document Ingestion** to learn how to load and chunk documents with LlamaIndex.

---

## Experimentation Ideas

- Add a `/api/v1/chat` endpoint that maintains conversation context
- Implement request caching to avoid re-generating identical prompts
- Add token counting to track usage
- Create a batch generation endpoint for multiple prompts
- Add support for different Ollama models via query parameters
- Implement rate limiting per IP address
