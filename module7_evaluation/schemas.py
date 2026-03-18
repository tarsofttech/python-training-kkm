"""
Pydantic v2 Schemas for Module 7 - RAG Evaluation

This file defines request and response models for evaluation endpoints.
"""

from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any


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


class EvalRunResponse(BaseModel):
    """Response model for evaluation run endpoint."""
    status: str = Field(..., description="Evaluation status")
    total_questions: int = Field(..., description="Total number of questions evaluated")
    avg_faithfulness: float = Field(..., description="Average faithfulness score")
    avg_relevancy: float = Field(..., description="Average relevancy score")
    pass_rate: float = Field(..., description="Percentage of passed evaluations")
    report_path: str = Field(..., description="Path to the saved report")


class EvalReportResponse(BaseModel):
    """Response model for evaluation report endpoint."""
    timestamp: str = Field(..., description="Report timestamp")
    total_questions: int = Field(..., description="Total questions evaluated")
    metrics: Dict[str, Any] = Field(..., description="Evaluation metrics")
    results: List[Dict[str, Any]] = Field(..., description="Individual question results")
