"""
Module 3: FastAPI + Ollama Integration - Main Application

This application demonstrates how to integrate FastAPI with Ollama for LLM text generation.
It includes health checks, error handling, and both standard and streaming responses.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import os
from dotenv import load_dotenv

from ollama_client import OllamaClient
from routers import generate
from schemas import HealthResponse

load_dotenv()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifespan context manager for startup and shutdown events.
    
    On startup:
    - Initialize the Ollama client
    - Store it in app.state for access in route handlers
    - Check Ollama connectivity
    
    On shutdown:
    - Clean up resources (if needed)
    """
    print("🚀 Server starting up...")
    
    ollama_host = os.getenv("OLLAMA_HOST", "http://localhost:11434")
    model_name = os.getenv("MODEL_NAME", "llama3.1")
    embed_model = os.getenv("EMBED_MODEL", "nomic-embed-text")
    
    app.state.ollama = OllamaClient(
        base_url=ollama_host,
        model=model_name,
        embed_model=embed_model
    )
    
    print(f"📡 Ollama URL: {ollama_host}")
    print(f"🤖 Model: {model_name}")
    print(f"🧮 Embed Model: {embed_model}")
    
    is_healthy = await app.state.ollama.health_check()
    if is_healthy:
        print("✅ Ollama is reachable")
    else:
        print("⚠️  Warning: Ollama is not reachable. Make sure it's running!")
        print("   Run: ollama serve")
    
    print(f"📖 Docs available at: http://localhost:8000/docs")
    
    yield
    
    print("👋 Server shutting down...")


app = FastAPI(
    title=os.getenv("API_TITLE", "RAG Training API"),
    version=os.getenv("API_VERSION", "0.1.0"),
    description="FastAPI + Ollama Integration - Local LLM text generation",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(generate.router)


@app.get("/")
async def root():
    """Root endpoint with API information."""
    return {
        "message": "FastAPI + Ollama Integration API",
        "version": app.version,
        "docs": "/docs",
        "endpoints": {
            "health": "/api/v1/health",
            "generate": "/api/v1/generate"
        }
    }


@app.get("/api/v1/health", response_model=HealthResponse)
async def health_check():
    """
    Health check endpoint.
    
    Checks both the API status and Ollama connectivity.
    Returns 200 even if Ollama is down (but indicates it in the response).
    """
    ollama_healthy = await app.state.ollama.health_check()
    
    return HealthResponse(
        status="healthy",
        ollama_reachable=ollama_healthy
    )
