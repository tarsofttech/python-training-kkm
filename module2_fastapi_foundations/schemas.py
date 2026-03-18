"""
Pydantic v2 Schemas for the RAG Training API

This file defines all the request and response models used across the API.
Pydantic provides automatic validation, serialization, and documentation.
"""

from pydantic import BaseModel, Field, field_validator
from typing import List, Optional, Literal
from datetime import datetime


class HealthResponse(BaseModel):
    """Response model for the health check endpoint."""
    status: str = Field(..., description="Server status (e.g., 'healthy')")
    version: str = Field(..., description="API version")
    timestamp: str = Field(..., description="Current server timestamp in ISO format")


class EchoRequest(BaseModel):
    """Request model for the echo endpoint."""
    message: str = Field(
        ..., 
        min_length=1, 
        max_length=500,
        description="Message to echo back (1-500 characters)"
    )


class EchoResponse(BaseModel):
    """Response model for the echo endpoint."""
    original: str = Field(..., description="Original message")
    uppercased: str = Field(..., description="Message converted to uppercase")
    char_count: int = Field(..., description="Number of characters in the message")


class QueryRequest(BaseModel):
    """Request model for RAG query endpoint (used in Module 5+)."""
    question: str = Field(
        ...,
        min_length=5,
        max_length=500,
        description="Question to ask the RAG system"
    )
    top_k: int = Field(
        default=3,
        ge=1,
        le=10,
        description="Number of relevant chunks to retrieve"
    )
    filters: Optional[dict] = Field(
        default=None,
        description="Optional metadata filters for retrieval"
    )


class QueryResponse(BaseModel):
    """Response model for RAG query endpoint."""
    answer: str = Field(..., description="Generated answer from the RAG system")
    sources: List[str] = Field(
        default_factory=list,
        description="List of source documents used to generate the answer"
    )
    confidence: float = Field(
        ...,
        ge=0.0,
        le=1.0,
        description="Confidence score of the answer (0.0 to 1.0)"
    )


class IngestRequest(BaseModel):
    """Request model for document ingestion endpoint (used in Module 4+)."""
    document_name: str = Field(
        ...,
        min_length=1,
        description="Name of the document to ingest"
    )
    chunk_size: int = Field(
        default=512,
        ge=128,
        le=1024,
        description="Size of text chunks in tokens"
    )
    chunk_overlap: int = Field(
        default=50,
        ge=0,
        le=256,
        description="Number of overlapping tokens between chunks"
    )
    
    @field_validator('chunk_overlap')
    @classmethod
    def validate_overlap(cls, v, info):
        """Ensure chunk_overlap is less than chunk_size."""
        if 'chunk_size' in info.data and v >= info.data['chunk_size']:
            raise ValueError('chunk_overlap must be less than chunk_size')
        return v


class IngestResponse(BaseModel):
    """Response model for document ingestion endpoint."""
    status: str = Field(..., description="Ingestion status (e.g., 'success', 'failed')")
    chunks_created: int = Field(..., description="Number of chunks created from the document")
    index_size: int = Field(..., description="Total number of chunks in the index")
    document_name: str = Field(..., description="Name of the ingested document")


class ChatMessage(BaseModel):
    """Individual message in a chat conversation."""
    role: Literal["user", "assistant"] = Field(
        ...,
        description="Role of the message sender"
    )
    content: str = Field(
        ...,
        min_length=1,
        description="Content of the message"
    )


class ChatRequest(BaseModel):
    """Request model for chat endpoint (used in Module 6+)."""
    session_id: str = Field(
        ...,
        min_length=1,
        description="Unique session identifier for conversation tracking"
    )
    message: str = Field(
        ...,
        min_length=1,
        max_length=1000,
        description="User's message"
    )
    history: Optional[List[ChatMessage]] = Field(
        default=None,
        description="Optional conversation history (if not using server-side sessions)"
    )


class ChatResponse(BaseModel):
    """Response model for chat endpoint."""
    session_id: str = Field(..., description="Session identifier")
    response: str = Field(..., description="Assistant's response")
    sources: List[str] = Field(
        default_factory=list,
        description="Source documents used to generate the response"
    )


class GenerateRequest(BaseModel):
    """Request model for LLM generation endpoint (used in Module 3+)."""
    prompt: str = Field(
        ...,
        min_length=1,
        max_length=2000,
        description="Prompt to send to the LLM"
    )
    system: Optional[str] = Field(
        default=None,
        max_length=1000,
        description="Optional system prompt to set LLM behavior"
    )
    temperature: float = Field(
        default=0.7,
        ge=0.0,
        le=2.0,
        description="Temperature for response randomness (0.0 = deterministic, 2.0 = very random)"
    )
    stream: bool = Field(
        default=False,
        description="Whether to stream the response"
    )


class GenerateResponse(BaseModel):
    """Response model for LLM generation endpoint."""
    text: str = Field(..., description="Generated text from the LLM")
    model: str = Field(..., description="Model name used for generation")
    duration_ms: int = Field(..., description="Generation duration in milliseconds")
