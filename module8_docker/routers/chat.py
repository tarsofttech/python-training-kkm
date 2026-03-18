"""
Chat Router - Multi-turn Conversation Endpoints

This router provides endpoints for managing chat sessions and
conducting multi-turn conversations with the RAG system.
"""

from fastapi import APIRouter, HTTPException, Request
from schemas import (
    ChatRequest, ChatResponse, SessionListResponse,
    SessionHistoryResponse, SessionDeleteResponse
)

router = APIRouter(prefix="/api/v1", tags=["chat"])


@router.post("/chat", response_model=ChatResponse)
async def chat(request_data: ChatRequest, request: Request):
    """
    Send a message in a chat session.
    
    This endpoint maintains conversation history and provides
    context-aware responses using the CondensePlusContextChatEngine.
    
    Args:
        request_data: Chat request with session_id and message
        request: FastAPI request object
    
    Returns:
        ChatResponse: Assistant's response with sources
    
    Raises:
        HTTPException 503: If RAG engine is not ready
        HTTPException 500: For unexpected errors
    """
    rag_engine = request.app.state.rag_engine
    chat_manager = request.app.state.chat_manager
    
    if not rag_engine.is_ready():
        raise HTTPException(
            status_code=503,
            detail="RAG system not ready. Please ingest documents first."
        )
    
    try:
        result = await chat_manager.chat(
            session_id=request_data.session_id,
            message=request_data.message,
            index=rag_engine.index
        )
        
        return ChatResponse(**result)
    
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error processing chat message: {str(e)}"
        )


@router.get("/sessions", response_model=SessionListResponse)
async def list_sessions(request: Request):
    """
    List all active chat sessions.
    
    Returns:
        SessionListResponse: List of session IDs and count
    """
    chat_manager = request.app.state.chat_manager
    
    sessions = chat_manager.list_sessions()
    
    return SessionListResponse(
        sessions=sessions,
        count=len(sessions)
    )


@router.get("/sessions/{session_id}/history", response_model=SessionHistoryResponse)
async def get_session_history(session_id: str, request: Request):
    """
    Get conversation history for a specific session.
    
    Args:
        session_id: Unique session identifier
        request: FastAPI request object
    
    Returns:
        SessionHistoryResponse: Conversation history
    
    Raises:
        HTTPException 404: If session not found
    """
    chat_manager = request.app.state.chat_manager
    
    if session_id not in chat_manager.sessions:
        raise HTTPException(
            status_code=404,
            detail=f"Session not found: {session_id}"
        )
    
    messages = chat_manager.get_history(session_id)
    
    return SessionHistoryResponse(
        session_id=session_id,
        messages=messages,
        message_count=len(messages)
    )


@router.delete("/sessions/{session_id}", response_model=SessionDeleteResponse)
async def delete_session(session_id: str, request: Request):
    """
    Delete a chat session and its history.
    
    Args:
        session_id: Unique session identifier
        request: FastAPI request object
    
    Returns:
        SessionDeleteResponse: Deletion status
    
    Raises:
        HTTPException 404: If session not found
    """
    chat_manager = request.app.state.chat_manager
    
    deleted = chat_manager.delete_session(session_id)
    
    if not deleted:
        raise HTTPException(
            status_code=404,
            detail=f"Session not found: {session_id}"
        )
    
    return SessionDeleteResponse(
        status="deleted",
        session_id=session_id
    )
