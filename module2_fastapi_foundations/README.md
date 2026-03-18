# Module 2: FastAPI Foundations

Learn how to build a structured FastAPI application with Pydantic v2 schemas, routing, CORS middleware, and automatic API documentation with Swagger.

---

## What You'll Learn

- Creating a FastAPI application with proper structure
- Defining Pydantic v2 models with validation
- Organizing routes using APIRouter
- Configuring CORS middleware for development
- Using FastAPI's automatic Swagger documentation
- Implementing lifespan events for startup/shutdown

---

## Prerequisites

- Basic Python knowledge
- Understanding of REST APIs
- Completed Module 1 (optional but recommended)

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
   - ReDoc: http://localhost:8000/redoc
   - OpenAPI JSON: http://localhost:8000/openapi.json

---

## Project Structure

```
module2_fastapi_foundations/
├── main.py              # FastAPI app with CORS and lifespan
├── schemas.py           # Pydantic v2 models with validation
├── routers/
│   └── basic.py         # Basic endpoints (health, echo)
└── data/                # Empty (no data needed)
```

---

## API Endpoints

### GET /health
Health check endpoint that returns server status.

**Response:**
```json
{
  "status": "healthy",
  "version": "0.1.0",
  "timestamp": "2024-03-12T10:30:00"
}
```

### POST /echo
Echo endpoint that transforms and analyzes input text.

**Request:**
```json
{
  "message": "Hello World"
}
```

**Response:**
```json
{
  "original": "Hello World",
  "uppercased": "HELLO WORLD",
  "char_count": 11
}
```

---

## Key Concepts

### Pydantic v2 Models
Pydantic provides automatic data validation and serialization:

```python
from pydantic import BaseModel, Field

class EchoRequest(BaseModel):
    message: str = Field(..., min_length=1, max_length=500)
```

### Field Validation
- `min_length`, `max_length`: String length constraints
- `ge`, `le`: Numeric constraints (greater/less than or equal)
- `Field(...)`: Required field
- `Field(default=...)`: Optional field with default

### APIRouter
Organize endpoints into logical groups:

```python
router = APIRouter(prefix="/api", tags=["basic"])
```

### CORS Middleware
Allow cross-origin requests for development:

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify exact origins
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### Lifespan Events
Run code on startup and shutdown:

```python
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    print("Server starting...")
    yield
    # Shutdown
    print("Server shutting down...")
```

---

## Testing the API

### Using curl

```bash
# Health check
curl http://localhost:8000/health

# Echo endpoint
curl -X POST http://localhost:8000/echo \
  -H "Content-Type: application/json" \
  -d '{"message": "Hello FastAPI"}'
```

### Using Python requests

```python
import requests

# Health check
response = requests.get("http://localhost:8000/health")
print(response.json())

# Echo
response = requests.post(
    "http://localhost:8000/echo",
    json={"message": "Hello FastAPI"}
)
print(response.json())
```

### Using Swagger UI

1. Go to http://localhost:8000/docs
2. Click on an endpoint
3. Click "Try it out"
4. Fill in the request body
5. Click "Execute"

---

## Pydantic Models Reference

This module defines 10 Pydantic models that will be used in later modules:

1. **HealthResponse** - Server health status
2. **EchoRequest/Response** - Text transformation
3. **QueryRequest/Response** - RAG query (Module 5)
4. **IngestRequest/Response** - Document ingestion (Module 4)
5. **ChatMessage** - Individual chat message
6. **ChatRequest/Response** - Chat conversation (Module 6)

---

## Common Issues

### Port already in use
```bash
# Use a different port
uvicorn main:app --reload --port 8001
```

### Module not found
```bash
# Make sure you're in the module directory
cd module2_fastapi_foundations
pip install -e .
```

### Validation errors
Check the Swagger UI for the exact schema requirements. All validation rules are documented there.

---

## Next Steps

After completing this module, proceed to **Module 3: FastAPI + Ollama Integration** to connect your API to a local LLM.

---

## Experimentation Ideas

- Add a new endpoint that reverses text
- Create a POST endpoint that accepts a list of messages
- Add custom validation (e.g., email format, URL format)
- Implement request/response logging middleware
- Add rate limiting using SlowAPI
- Create a new router for a different resource type
