"""
Pydantic v2 Schemas for Module 4 - Document Ingestion

This file defines request and response models for document ingestion endpoints.
"""

from pydantic import BaseModel, Field, field_validator


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
