"""
Ingest Router - Document Upload and Ingestion Endpoints

This router provides endpoints for uploading and ingesting documents
with configurable chunking strategies.
"""

from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from schemas import IngestResponse
from ingestor import DocumentIngestor
from llama_index.core import Document
import os
import tempfile
import shutil

router = APIRouter(prefix="/api/v1", tags=["ingest"])


@router.post("/ingest", response_model=IngestResponse)
async def ingest_document(
    file: UploadFile = File(..., description="Document file to upload"),
    chunk_size: int = Form(512, ge=128, le=1024, description="Chunk size in tokens"),
    chunk_overlap: int = Form(50, ge=0, le=256, description="Chunk overlap in tokens")
):
    """
    Upload and ingest a document with configurable chunking.
    
    This endpoint:
    1. Accepts a file upload (text or PDF)
    2. Saves it to a temporary directory
    3. Loads and chunks the document
    4. Returns ingestion statistics
    
    Args:
        file: The uploaded file
        chunk_size: Size of chunks (128-1024 tokens)
        chunk_overlap: Overlap between chunks (0-256 tokens)
    
    Returns:
        IngestResponse: Ingestion status and statistics
    
    Raises:
        HTTPException 400: If chunk_overlap >= chunk_size
        HTTPException 422: If file type is not supported
        HTTPException 500: For unexpected errors
    """
    if chunk_overlap >= chunk_size:
        raise HTTPException(
            status_code=400,
            detail="chunk_overlap must be less than chunk_size"
        )
    
    allowed_extensions = {'.txt', '.pdf', '.md', '.doc', '.docx'}
    file_ext = os.path.splitext(file.filename)[1].lower()
    
    if file_ext not in allowed_extensions:
        raise HTTPException(
            status_code=422,
            detail=f"Unsupported file type: {file_ext}. Allowed: {allowed_extensions}"
        )
    
    temp_dir = None
    
    try:
        temp_dir = tempfile.mkdtemp()
        
        file_path = os.path.join(temp_dir, file.filename)
        
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        print(f"📁 Saved uploaded file to: {file_path}")
        
        ingestor = DocumentIngestor()
        
        documents = ingestor.load_documents(temp_dir)
        
        if not documents:
            raise HTTPException(
                status_code=422,
                detail="No content could be extracted from the file"
            )
        
        nodes = ingestor.chunk_fixed(
            documents=documents,
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap
        )
        
        return IngestResponse(
            status="success",
            chunks_created=len(nodes),
            index_size=len(nodes),
            document_name=file.filename
        )
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error processing document: {str(e)}"
        )
    finally:
        if temp_dir and os.path.exists(temp_dir):
            shutil.rmtree(temp_dir)
            print(f"🗑️  Cleaned up temporary directory: {temp_dir}")
