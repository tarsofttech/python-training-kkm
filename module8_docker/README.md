# Module 8: Docker Deployment

Containerize the complete RAG application using Docker and Docker Compose. This module packages the FastAPI app and Ollama service together for easy deployment.

---

## What You'll Learn

- Creating a Dockerfile for FastAPI applications
- Multi-service orchestration with Docker Compose
- Container networking and service dependencies
- Volume management for persistent data
- Health checks for containers
- Running Ollama in a container

---

## Prerequisites

1. **Docker Desktop installed**
   - Download from [docker.com](https://www.docker.com/products/docker-desktop)
   - Ensure Docker daemon is running

2. **Completed Module 5 or 6** (RAG Pipeline or Chat Memory)

---

## Quick Start

### 1. Start Everything

```bash
# Build and start all services
docker compose up --build
```

This will:
- Build the FastAPI application image
- Pull the Ollama image
- Start both services
- Create necessary volumes and networks

### 2. Pull Required Models

In a new terminal, pull the LLM models into the Ollama container:

```bash
# Pull the LLM model
docker compose exec ollama ollama pull llama3.1

# Pull the embedding model
docker compose exec ollama ollama pull nomic-embed-text
```

### 3. Test the API

```bash
# Check health
curl http://localhost:8000/api/v1/status

# Access Swagger docs
open http://localhost:8000/docs
```

### 4. Stop Everything

```bash
# Stop and remove containers (keeps volumes)
docker compose down

# Stop and remove everything including volumes
docker compose down -v
```

---

## Project Structure

```
module8_docker/
├── Dockerfile              # FastAPI app container definition
├── docker-compose.yml      # Multi-service orchestration
├── .dockerignore          # Files to exclude from build
├── .env                   # Environment variables (pre-filled)
├── .env.example           # Environment template
├── pyproject.toml         # Python dependencies
├── main.py                # Complete FastAPI app
├── schemas.py             # Pydantic models
├── rag_engine.py          # RAG engine with FAISS
├── ollama_client.py       # Ollama HTTP client
├── ingestor.py            # Document ingestion
├── chat_manager.py        # Chat session management
├── routers/               # API route handlers
│   ├── ingest.py
│   ├── query.py
│   └── chat.py
└── data/                  # Sample documents
    ├── hr_leave_policy.txt
    ├── hr_code_of_conduct.txt
    └── it_security_policy.txt
```

---

## Docker Services

### Ollama Service
- **Image**: `ollama/ollama:latest`
- **Port**: 11434
- **Volume**: `ollama-models` (stores downloaded models)
- **Health Check**: Pings `/api/version` endpoint

### FastAPI App Service
- **Build**: From local Dockerfile
- **Port**: 8000
- **Volumes**:
  - `faiss-index`: Persistent FAISS vector store
  - `uploaded-docs`: Uploaded documents
- **Depends On**: Ollama service (waits for health check)
- **Health Check**: Pings `/api/v1/status` endpoint

---

## Environment Variables

The `.env` file is pre-configured for Docker:

```env
OLLAMA_HOST=http://ollama:11434    # Container network hostname
MODEL_NAME=llama3.1
EMBED_MODEL=nomic-embed-text
INDEX_PATH=/app/data/index         # Container path
UPLOAD_DIR=/app/data/uploads       # Container path
LOG_LEVEL=INFO
```

---

## Docker Commands

### Build and Run

```bash
# Build and start in detached mode
docker compose up -d --build

# View logs
docker compose logs -f

# View logs for specific service
docker compose logs -f fastapi-app
```

### Managing Services

```bash
# Stop services
docker compose stop

# Start stopped services
docker compose start

# Restart services
docker compose restart

# Remove containers
docker compose down
```

### Accessing Containers

```bash
# Execute command in Ollama container
docker compose exec ollama ollama list

# Execute command in FastAPI container
docker compose exec fastapi-app ls -la /app

# Open shell in FastAPI container
docker compose exec fastapi-app /bin/bash
```

### Volume Management

```bash
# List volumes
docker volume ls

# Inspect volume
docker volume inspect faiss-index

# Remove all volumes (WARNING: deletes data)
docker compose down -v
```

---

## Using the Dockerized Application

### 1. Ingest Documents

```bash
# Upload a document
curl -X POST http://localhost:8000/api/v1/ingest \
  -F "file=@data/hr_leave_policy.txt"
```

### 2. Query the RAG System

```bash
# Ask a question
curl -X POST http://localhost:8000/api/v1/query \
  -H "Content-Type: application/json" \
  -d '{
    "question": "How many vacation days do employees get?",
    "top_k": 3
  }'
```

### 3. Chat Sessions

```bash
# Start a conversation
curl -X POST http://localhost:8000/api/v1/chat \
  -H "Content-Type: application/json" \
  -d '{
    "session_id": "user123",
    "message": "What is the leave policy?"
  }'
```

---

## Dockerfile Explained

```dockerfile
FROM python:3.11-slim          # Base image
WORKDIR /app                   # Set working directory
RUN apt-get update && ...      # Install system dependencies (curl)
COPY pyproject.toml .          # Copy dependencies first (caching)
RUN pip install -e .           # Install Python packages
COPY . .                       # Copy application code
RUN useradd appuser            # Create non-root user
USER appuser                   # Switch to non-root
EXPOSE 8000                    # Document port
HEALTHCHECK ...                # Define health check
CMD ["uvicorn", ...]           # Start command
```

---

## Docker Compose Explained

```yaml
services:
  ollama:
    image: ollama/ollama       # Pre-built image
    ports: ["11434:11434"]     # Expose port
    volumes: [ollama-models]   # Persistent storage
    healthcheck: ...           # Health check definition
    
  fastapi-app:
    build: .                   # Build from Dockerfile
    depends_on:                # Wait for Ollama
      ollama:
        condition: service_healthy
    volumes:                   # Persistent data
      - faiss-index:/app/data/index
      - uploaded-docs:/app/data/uploads
    env_file: .env             # Load environment variables

volumes:                       # Named volumes
  ollama-models:
  faiss-index:
  uploaded-docs:

networks:                      # Custom network
  rag-network:
```

---

## Troubleshooting

### Ollama Not Reachable

```bash
# Check Ollama container logs
docker compose logs ollama

# Verify Ollama is healthy
docker compose ps

# Test Ollama directly
curl http://localhost:11434/api/version
```

### Models Not Found

```bash
# List models in Ollama container
docker compose exec ollama ollama list

# Pull models if missing
docker compose exec ollama ollama pull llama3.1
docker compose exec ollama ollama pull nomic-embed-text
```

### FastAPI App Errors

```bash
# Check app logs
docker compose logs fastapi-app

# Verify environment variables
docker compose exec fastapi-app env | grep OLLAMA

# Check health status
curl http://localhost:8000/api/v1/status
```

### Port Conflicts

```bash
# If port 8000 is in use, modify docker-compose.yml:
ports:
  - "8001:8000"  # Map host port 8001 to container port 8000
```

### Volume Permissions

```bash
# If permission errors occur, check volume ownership
docker compose exec fastapi-app ls -la /app/data

# Rebuild with proper permissions
docker compose down -v
docker compose up --build
```

---

## Production Considerations

### Security
- Use secrets management (not .env files)
- Enable HTTPS with reverse proxy (nginx/traefik)
- Restrict CORS origins
- Implement authentication

### Performance
- Use multi-stage builds to reduce image size
- Configure resource limits in docker-compose.yml
- Use production WSGI server (gunicorn)
- Enable caching layers

### Monitoring
- Add logging aggregation (ELK stack)
- Implement metrics collection (Prometheus)
- Set up alerts for health check failures
- Monitor resource usage

### Scaling
- Use Docker Swarm or Kubernetes for orchestration
- Implement load balancing
- Use external database for sessions (Redis)
- Separate read/write replicas

---

## Next Steps

Congratulations! You've completed all 8 modules of the FastAPI + Local LLM Training Lab.

You now know how to:
- ✅ Interact with Ollama via Python
- ✅ Build structured FastAPI applications
- ✅ Integrate LLMs with web APIs
- ✅ Ingest and chunk documents
- ✅ Build complete RAG pipelines
- ✅ Manage chat sessions
- ✅ Evaluate RAG quality
- ✅ Deploy with Docker

### Further Learning
- Explore other LLM models (Mistral, Llama 2)
- Implement advanced RAG techniques (HyDE, RAG-Fusion)
- Add authentication and authorization
- Build a web UI (React, Vue, Svelte)
- Deploy to cloud (AWS, GCP, Azure)
- Implement CI/CD pipelines

---

## Cleanup

To completely remove everything:

```bash
# Stop and remove containers, networks, volumes
docker compose down -v

# Remove images
docker rmi $(docker images -q module8-docker*)

# Remove unused Docker resources
docker system prune -a
```
