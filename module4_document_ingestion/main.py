"""
Module 4: Document Ingestion - Main Application

This application demonstrates document loading and chunking with LlamaIndex.
It provides an endpoint for uploading documents and configuring chunking strategies.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import os
from dotenv import load_dotenv

from routers import ingest

load_dotenv()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifespan context manager for startup and shutdown events.
    
    On startup:
    - Create upload directory if it doesn't exist
    - Log configuration
    
    On shutdown:
    - Clean up resources
    """
    print("🚀 Server starting up...")
    
    upload_dir = os.getenv("UPLOAD_DIR", "./data/uploads")
    os.makedirs(upload_dir, exist_ok=True)
    
    print(f"📁 Upload directory: {upload_dir}")
    print(f"📖 Docs available at: http://localhost:8000/docs")
    
    yield
    
    print("👋 Server shutting down...")


app = FastAPI(
    title=os.getenv("API_TITLE", "RAG Training API"),
    version=os.getenv("API_VERSION", "0.1.0"),
    description="Document Ingestion with LlamaIndex - Load and chunk documents",
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


@app.get("/")
async def root():
    """Root endpoint with API information."""
    return {
        "message": "Document Ingestion API",
        "version": app.version,
        "docs": "/docs",
        "endpoints": {
            "ingest": "/api/v1/ingest"
        }
    }
