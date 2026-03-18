"""
Module 2: FastAPI Foundations - Main Application

This is the main FastAPI application file that sets up:
- The FastAPI app with metadata
- CORS middleware for cross-origin requests
- Lifespan events for startup/shutdown
- Router inclusion for organizing endpoints
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import os
from dotenv import load_dotenv

from routers import basic

load_dotenv()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifespan context manager for startup and shutdown events.
    
    This runs when the server starts and stops, allowing you to:
    - Initialize database connections
    - Load models or data
    - Set up background tasks
    - Clean up resources on shutdown
    """
    print("🚀 Server starting up...")
    print(f"📚 API Title: {app.title}")
    print(f"📌 Version: {app.version}")
    print(f"📖 Docs available at: http://localhost:8000/docs")
    
    yield
    
    print("👋 Server shutting down...")


app = FastAPI(
    title=os.getenv("API_TITLE", "RAG Training API"),
    version=os.getenv("API_VERSION", "0.1.0"),
    description="A training API for building RAG applications with FastAPI and local LLMs",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(basic.router)


@app.get("/")
async def root():
    """
    Root endpoint that provides basic API information.
    """
    return {
        "message": "Welcome to the RAG Training API",
        "version": app.version,
        "docs": "/docs",
        "redoc": "/redoc"
    }
