"""
Module 7: RAG Evaluation - Main Application

This application extends Module 5 with evaluation capabilities
for measuring RAG quality using faithfulness and relevancy metrics.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import os
from dotenv import load_dotenv

from rag_engine import RAGEngine
from routers import ingest, query
from routers.eval import router as eval_router
from schemas import StatusResponse

load_dotenv()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifespan context manager for startup and shutdown events.
    
    On startup:
    - Initialize the RAG engine
    - Attempt to load existing index
    - Create necessary directories
    
    On shutdown:
    - Clean up resources
    """
    print("🚀 Server starting up...")
    
    ollama_host = os.getenv("OLLAMA_HOST", "http://localhost:11434")
    model_name = os.getenv("MODEL_NAME", "llama3.1")
    embed_model = os.getenv("EMBED_MODEL", "nomic-embed-text")
    index_path = os.getenv("INDEX_PATH", "./data/index")
    
    app.state.rag_engine = RAGEngine(
        ollama_base_url=ollama_host,
        model=model_name,
        embed_model=embed_model,
        index_path=index_path
    )
    
    app.state.latest_report = None
    
    index_loaded = await app.state.rag_engine.load_index()
    
    if index_loaded:
        node_count = app.state.rag_engine.get_node_count()
        print(f"✅ Loaded existing index with {node_count} nodes")
    else:
        print("ℹ️  No existing index found. Ingest documents to build the index.")
    
    print(f"📖 Docs available at: http://localhost:8000/docs")
    
    yield
    
    print("👋 Server shutting down...")


app = FastAPI(
    title=os.getenv("API_TITLE", "RAG Training API"),
    version=os.getenv("API_VERSION", "0.1.0"),
    description="RAG Evaluation - Measuring and improving RAG quality",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(ingest.router)
app.include_router(query.router)
app.include_router(eval_router)


@app.get("/")
async def root():
    """Root endpoint with API information."""
    return {
        "message": "RAG Evaluation API",
        "version": app.version,
        "docs": "/docs",
        "endpoints": {
            "ingest": "/api/v1/ingest",
            "query": "/api/v1/query",
            "eval_run": "/api/v1/eval/run",
            "eval_report": "/api/v1/eval/report",
            "status": "/api/v1/status"
        }
    }


@app.get("/api/v1/status", response_model=StatusResponse)
async def get_status():
    """Get RAG system status."""
    rag_engine = app.state.rag_engine
    
    return StatusResponse(
        index_loaded=rag_engine.is_ready(),
        index_path=rag_engine.index_path,
        model=rag_engine.model_name,
        node_count=rag_engine.get_node_count() if rag_engine.is_ready() else 0
    )
