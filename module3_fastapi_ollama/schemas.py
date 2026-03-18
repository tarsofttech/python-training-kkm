"""
Pydantic v2 Schemas for Module 3 - FastAPI + Ollama

This file extends the schemas from Module 2 with additional models
for LLM generation endpoints.
"""

from pydantic import BaseModel, Field
from typing import Optional


class GenerateRequest(BaseModel):
    """Request model for LLM generation endpoint."""
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
    """Response model for LLM generation endpoint (non-streaming)."""
    text: str = Field(..., description="Generated text from the LLM")
    model: str = Field(..., description="Model name used for generation")
    duration_ms: int = Field(..., description="Generation duration in milliseconds")


class HealthResponse(BaseModel):
    """Response model for health check endpoint."""
    status: str = Field(..., description="API status")
    ollama_reachable: bool = Field(..., description="Whether Ollama is reachable")
