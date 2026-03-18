"""
Query Router - RAG Query Endpoints

This router provides endpoints for querying the RAG system,
including a debug mode that shows the augmented prompt.
"""

from fastapi import APIRouter, HTTPException, Request
from schemas import QueryRequest, QueryResponse, DebugQueryResponse

router = APIRouter(prefix="/api/v1", tags=["query"])


@router.post("/query", response_model=QueryResponse)
async def query_rag(request_data: QueryRequest, request: Request):
    """
    Query the RAG system with a question.
    
    This endpoint:
    1. Takes a user question
    2. Retrieves relevant chunks from the FAISS index
    3. Augments the question with retrieved context
    4. Generates an answer using the LLM
    5. Returns the answer with source attribution
    
    Args:
        request_data: Query parameters (question, top_k, filters)
        request: FastAPI request object (to access app.state.rag_engine)
    
    Returns:
        QueryResponse: Answer, sources, and confidence score
    
    Raises:
        HTTPException 503: If RAG engine is not ready
        HTTPException 500: For unexpected errors
    """
    rag_engine = request.app.state.rag_engine
    
    if not rag_engine.is_ready():
        raise HTTPException(
            status_code=503,
            detail="RAG system not ready. Please ingest documents first."
        )
    
    try:
        result = await rag_engine.query(
            question=request_data.question,
            top_k=request_data.top_k,
            return_augmented_prompt=False
        )
        
        return QueryResponse(
            answer=result["answer"],
            sources=result["sources"],
            confidence=result["confidence"]
        )
    
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error processing query: {str(e)}"
        )


@router.get("/debug/query", response_model=DebugQueryResponse)
async def debug_query_rag(
    question: str,
    top_k: int = 3,
    request: Request = None
):
    """
    Query the RAG system in debug mode.
    
    This endpoint is identical to the regular query endpoint,
    but also returns the augmented prompt that was sent to the LLM.
    This is useful for understanding how the RAG system works
    and debugging retrieval issues.
    
    Args:
        question: The user's question
        top_k: Number of chunks to retrieve (1-10)
        request: FastAPI request object
    
    Returns:
        DebugQueryResponse: Answer, sources, confidence, and augmented prompt
    
    Raises:
        HTTPException 503: If RAG engine is not ready
        HTTPException 500: For unexpected errors
    """
    rag_engine = request.app.state.rag_engine
    
    if not rag_engine.is_ready():
        raise HTTPException(
            status_code=503,
            detail="RAG system not ready. Please ingest documents first."
        )
    
    try:
        result = await rag_engine.query(
            question=question,
            top_k=top_k,
            return_augmented_prompt=True
        )
        
        return DebugQueryResponse(
            answer=result["answer"],
            sources=result["sources"],
            confidence=result["confidence"],
            augmented_prompt=result["augmented_prompt"]
        )
    
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error processing query: {str(e)}"
        )
