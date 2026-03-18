"""
Generate Router - LLM Text Generation Endpoints

This router provides endpoints for generating text using Ollama,
supporting both standard (complete response) and streaming modes.
"""

from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import StreamingResponse
from schemas import GenerateRequest, GenerateResponse
from ollama_client import OllamaConnectionError
import time

router = APIRouter(prefix="/api/v1", tags=["generate"])


@router.post("/generate")
async def generate_text(request_data: GenerateRequest, request: Request):
    """
    Generate text using Ollama.
    
    Supports both standard and streaming responses:
    - stream=false: Returns complete response as JSON
    - stream=true: Returns Server-Sent Events (SSE) stream
    
    Args:
        request_data: Generation parameters (prompt, system, temperature, stream)
        request: FastAPI request object (to access app.state.ollama)
    
    Returns:
        GenerateResponse (if stream=false) or StreamingResponse (if stream=true)
    
    Raises:
        HTTPException 503: If Ollama is not reachable
        HTTPException 500: For unexpected errors
    """
    ollama_client = request.app.state.ollama
    
    try:
        if request_data.stream:
            async def generate_stream():
                """
                Async generator that yields Server-Sent Events.
                Each chunk is formatted as: data: <text>\n\n
                """
                try:
                    async for chunk in ollama_client.generate_stream(
                        prompt=request_data.prompt,
                        system=request_data.system,
                        temperature=request_data.temperature
                    ):
                        yield f"data: {chunk}\n\n"
                    
                    yield "data: [DONE]\n\n"
                except OllamaConnectionError as e:
                    yield f"data: [ERROR] {str(e)}\n\n"
            
            return StreamingResponse(
                generate_stream(),
                media_type="text/event-stream",
                headers={
                    "Cache-Control": "no-cache",
                    "Connection": "keep-alive",
                }
            )
        else:
            start_time = time.time()
            
            text = await ollama_client.generate(
                prompt=request_data.prompt,
                system=request_data.system,
                temperature=request_data.temperature
            )
            
            duration_ms = int((time.time() - start_time) * 1000)
            
            return GenerateResponse(
                text=text,
                model=ollama_client.model,
                duration_ms=duration_ms
            )
    
    except OllamaConnectionError as e:
        raise HTTPException(
            status_code=503,
            detail=f"Ollama service unavailable: {str(e)}"
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Unexpected error: {str(e)}"
        )
