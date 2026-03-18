"""
Basic API Router

This router contains simple endpoints for health checks and echo functionality.
These endpoints demonstrate the fundamentals of FastAPI routing and Pydantic validation.
"""

from fastapi import APIRouter
from datetime import datetime
from schemas import HealthResponse, EchoRequest, EchoResponse

router = APIRouter(tags=["basic"])


@router.get("/health", response_model=HealthResponse)
async def health_check():
    """
    Health check endpoint.
    
    Returns the current server status, version, and timestamp.
    This is useful for monitoring and ensuring the API is running.
    """
    return HealthResponse(
        status="healthy",
        version="0.1.0",
        timestamp=datetime.utcnow().isoformat()
    )


@router.post("/echo", response_model=EchoResponse)
async def echo_message(request: EchoRequest):
    """
    Echo endpoint that transforms the input message.
    
    Takes a message, converts it to uppercase, and counts the characters.
    This demonstrates Pydantic validation and response transformation.
    """
    return EchoResponse(
        original=request.message,
        uppercased=request.message.upper(),
        char_count=len(request.message)
    )
