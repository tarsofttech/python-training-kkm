"""
Pydantic v2 Schemas for Module 5 - RAG Pipeline

This file defines request and response models for the RAG pipeline endpoints.
"""

from pydantic import BaseModel, Field, field_validator
from typing import List, Optional


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


class IngestRequest(BaseModel):
    """Request model for document ingestion endpoint."""
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


class StatusResponse(BaseModel):
    """Response model for RAG system status endpoint."""
    index_loaded: bool = Field(..., description="Whether the index is loaded")
    index_path: str = Field(..., description="Path to the index storage")
    model: str = Field(..., description="LLM model name")
    node_count: int = Field(default=0, description="Number of nodes in the index")
