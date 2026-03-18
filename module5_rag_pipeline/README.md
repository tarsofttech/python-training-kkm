# Module 5: Full RAG Pipeline

Build a complete end-to-end RAG (Retrieval-Augmented Generation) system with FAISS vector store, Ollama embeddings, and LlamaIndex query engine. This module combines everything from previous modules into a working RAG application.

---

## What You'll Learn

- Building a FAISS vector store for semantic search
- Embedding documents with Ollama's nomic-embed-text
- Creating a RAG query engine with LlamaIndex
- Persisting and loading vector indices
- Retrieving relevant context for LLM queries
- Source attribution in RAG responses

---

## Prerequisites

1. **Ollama installed and running**
   ```bash
   ollama serve
   ```

2. **Required models pulled**
   ```bash
   ollama pull llama3.1
   ollama pull nomic-embed-text
   ```

3. **Completed Modules 3 & 4** (FastAPI + Ollama, Document Ingestion)

---

## Setup

1. **Install dependencies**
   ```bash
   pip install -e .
   ```

2. **Create .env file**
   ```bash
   cp .env.example .env
   ```

3. **Build the index (first time)**
   ```bash
   # The index will be built automatically when you ingest documents
   # Or you can run the ingestor script directly
   python -c "from rag_engine import RAGEngine; import asyncio; asyncio.run(RAGEngine().build_from_directory('./data'))"
   ```

4. **Start the server**
   ```bash
   uvicorn main:app --reload
   ```

5. **Access the API**
   - Swagger UI: http://localhost:8000/docs
   - Query endpoint: http://localhost:8000/api/v1/query
   - Status: http://localhost:8000/api/v1/status

---

## Project Structure

```
module5_rag_pipeline/
├── main.py              # FastAPI app with RAG engine
├── schemas.py           # Request/response models
├── ollama_client.py     # Ollama client (from Module 3)
├── ingestor.py          # Document ingestor (from Module 4)
├── rag_engine.py        # RAG engine with FAISS
├── routers/
│   ├── ingest.py        # Document ingestion endpoint
│   └── query.py         # RAG query endpoints
└── data/
    ├── hr_leave_policy.txt
    ├── hr_code_of_conduct.txt
    ├── it_security_policy.txt
    └── index/           # FAISS index storage (created automatically)
```

---

## API Endpoints

### POST /api/v1/ingest
Upload and index a document.

**Request (multipart/form-data):**
- `file`: Document file
- `chunk_size`: Chunk size (default: 512)
- `chunk_overlap`: Overlap (default: 50)

**Response:**
```json
{
  "status": "success",
  "chunks_created": 15,
  "index_size": 45,
  "document_name": "hr_leave_policy.txt"
}
```

### POST /api/v1/query
Query the RAG system with a question.

**Request:**
```json
{
  "question": "How many vacation days do employees get?",
  "top_k": 3,
  "filters": null
}
```

**Response:**
```json
{
  "answer": "Employees are entitled to 14 days of annual leave per calendar year...",
  "sources": [
    "hr_leave_policy.txt (score: 0.89)",
    "hr_leave_policy.txt (score: 0.82)"
  ],
  "confidence": 0.85
}
```

### GET /api/v1/debug/query
Same as query but includes the augmented prompt sent to the LLM.

**Response:**
```json
{
  "answer": "...",
  "sources": [...],
  "confidence": 0.85,
  "augmented_prompt": "Context:\n[Retrieved chunks]\n\nQuestion: How many vacation days?\nAnswer:"
}
```

### GET /api/v1/status
Check RAG system status.

**Response:**
```json
{
  "index_loaded": true,
  "index_path": "./data/index",
  "model": "llama3.1",
  "node_count": 45
}
```

---

## How RAG Works

### 1. Document Ingestion
```
Document → Chunking → Embedding → FAISS Index
```

1. Load document with SimpleDirectoryReader
2. Split into chunks with SentenceSplitter
3. Generate embeddings with nomic-embed-text
4. Store in FAISS vector index
5. Persist index to disk

### 2. Query Process
```
Question → Embedding → Similarity Search → Context Retrieval → LLM Generation
```

1. Embed the user's question
2. Search FAISS index for similar chunks
3. Retrieve top-k most relevant chunks
4. Augment question with retrieved context
5. Send to LLM for answer generation
6. Return answer with source attribution

---

## Key Concepts

### Vector Embeddings
Numerical representations of text that capture semantic meaning. Similar texts have similar embeddings.

### FAISS (Facebook AI Similarity Search)
High-performance library for similarity search. Stores embeddings and finds nearest neighbors efficiently.

### Retrieval-Augmented Generation (RAG)
Combines retrieval (finding relevant context) with generation (LLM response) to provide accurate, grounded answers.

### Source Attribution
Tracking which documents/chunks were used to generate an answer, enabling verification and transparency.

---

## Testing the RAG Pipeline

### Step 1: Ingest Documents

```bash
# Ingest the HR leave policy
curl -X POST http://localhost:8000/api/v1/ingest \
  -F "file=@data/hr_leave_policy.txt"

# Ingest the code of conduct
curl -X POST http://localhost:8000/api/v1/ingest \
  -F "file=@data/hr_code_of_conduct.txt"

# Ingest the IT security policy
curl -X POST http://localhost:8000/api/v1/ingest \
  -F "file=@data/it_security_policy.txt"
```

### Step 2: Query the System

```bash
# Ask about vacation days
curl -X POST http://localhost:8000/api/v1/query \
  -H "Content-Type: application/json" \
  -d '{
    "question": "How many vacation days do employees get?",
    "top_k": 3
  }'

# Ask about password requirements
curl -X POST http://localhost:8000/api/v1/query \
  -H "Content-Type: application/json" \
  -d '{
    "question": "What are the password requirements?",
    "top_k": 3
  }'
```

### Step 3: Debug Mode

```bash
# See the augmented prompt
curl -X GET "http://localhost:8000/api/v1/debug/query?question=What%20is%20the%20dress%20code&top_k=3"
```

---

## RAG Engine Methods

### `async def build_index(nodes: List[TextNode]) -> None`
Build FAISS index from text nodes and persist to disk.

### `async def load_index() -> bool`
Load existing index from disk. Returns True if successful.

### `async def query(question: str, top_k: int = 3) -> dict`
Query the RAG system and return answer with sources.

### `def is_ready() -> bool`
Check if the index is loaded and ready for queries.

---

## Performance Tuning

### Chunk Size
- **Smaller (256)**: More granular, better precision, more chunks to search
- **Larger (1024)**: More context per chunk, fewer chunks, faster search

### Top-K
- **Lower (1-3)**: Faster, more focused, may miss context
- **Higher (5-10)**: More comprehensive, slower, may include noise

### Embedding Model
- **nomic-embed-text**: Fast, good quality, 768 dimensions
- Try other models for different trade-offs

---

## Common Issues

### Index not found
Build the index first by ingesting documents.

### Out of memory
Reduce chunk size or use fewer documents. FAISS loads the entire index into memory.

### Slow queries
- Reduce top_k
- Use smaller chunk sizes
- Ensure Ollama is running locally (not remote)

### Poor answer quality
- Increase top_k to retrieve more context
- Adjust chunk size and overlap
- Improve document quality
- Use more specific questions

---

## Next Steps

After completing this module, proceed to **Module 6: Chat Memory** to add multi-turn conversation support with session management.

---

## Experimentation Ideas

- Compare different chunk sizes (256, 512, 1024)
- Try different top_k values (1, 3, 5, 10)
- Implement hybrid search (keyword + semantic)
- Add re-ranking of retrieved chunks
- Implement query expansion or reformulation
- Add caching for frequent queries
- Create a web UI for the RAG system
