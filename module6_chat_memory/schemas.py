"""
Pydantic v2 Schemas for Module 6 - Chat Memory

This file defines request and response models for chat endpoints.
"""

from pydantic import BaseModel, Field
from typing import List, Optional, Literal


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
    """Request model for chat endpoint."""
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


class ChatResponse(BaseModel):
    """Response model for chat endpoint."""
    session_id: str = Field(..., description="Session identifier")
    response: str = Field(..., description="Assistant's response")
    sources: List[str] = Field(
        default_factory=list,
        description="Source documents used to generate the response"
    )


class SessionListResponse(BaseModel):
    """Response model for listing sessions."""
    sessions: List[str] = Field(..., description="List of active session IDs")
    count: int = Field(..., description="Number of active sessions")


class SessionHistoryResponse(BaseModel):
    """Response model for session history."""
    session_id: str = Field(..., description="Session identifier")
    messages: List[ChatMessage] = Field(..., description="Conversation history")
    message_count: int = Field(..., description="Number of messages in history")


class SessionDeleteResponse(BaseModel):
    """Response model for session deletion."""
    status: str = Field(..., description="Deletion status")
    session_id: str = Field(..., description="Deleted session identifier")


class QueryRequest(BaseModel):
    """Request model for RAG query endpoint."""
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


class DebugQueryResponse(QueryResponse):
    """Extended response model for debug query endpoint."""
    augmented_prompt: str = Field(
        ...,
        description="The full prompt sent to the LLM including retrieved context"
    )


class IngestResponse(BaseModel):
    """Response model for document ingestion endpoint."""
    status: str = Field(..., description="Ingestion status")
    chunks_created: int = Field(..., description="Number of chunks created")
    index_size: int = Field(..., description="Total number of chunks in index")
    document_name: str = Field(..., description="Name of ingested document")


class StatusResponse(BaseModel):
    """Response model for RAG system status endpoint."""
    index_loaded: bool = Field(..., description="Whether the index is loaded")
    index_path: str = Field(..., description="Path to the index storage")
    model: str = Field(..., description="LLM model name")
    node_count: int = Field(default=0, description="Number of nodes in the index")
