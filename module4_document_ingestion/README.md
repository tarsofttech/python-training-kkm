# Module 4: Document Ingestion

Learn how to load documents with LlamaIndex, experiment with different chunking strategies, and expose document ingestion via a FastAPI endpoint with file upload support.

---

## What You'll Learn

- Loading documents with LlamaIndex's SimpleDirectoryReader
- Chunking strategies: fixed-size vs sentence-window
- Adding metadata to document chunks
- File upload handling in FastAPI
- Comparing chunking methods for optimal retrieval

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

3. **Completed Module 3** (FastAPI + Ollama)

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

3. **Start the server**
   ```bash
   uvicorn main:app --reload
   ```

4. **Access the API**
   - Swagger UI: http://localhost:8000/docs
   - Upload endpoint: http://localhost:8000/api/v1/ingest

---

## Project Structure

```
module4_document_ingestion/
├── main.py              # FastAPI app with ingest router
├── schemas.py           # Pydantic models for ingestion
├── ingestor.py          # DocumentIngestor class with chunking methods
├── routers/
│   └── ingest.py        # File upload and ingestion endpoint
└── data/
    ├── hr_leave_policy.txt
    ├── hr_code_of_conduct.txt
    └── it_security_policy.txt
```

---

## API Endpoints

### POST /api/v1/ingest
Upload and ingest a document with configurable chunking.

**Request (multipart/form-data):**
- `file`: Document file to upload
- `chunk_size`: Size of chunks (128-1024, default: 512)
- `chunk_overlap`: Overlap between chunks (0-256, default: 50)

**Response:**
```json
{
  "status": "success",
  "chunks_created": 15,
  "index_size": 15,
  "document_name": "hr_leave_policy.txt"
}
```

---

## Chunking Strategies

### Fixed-Size Chunking (SentenceSplitter)
Splits documents into chunks of approximately equal size.

**Pros:**
- Predictable chunk sizes
- Good for consistent context windows
- Fast and simple

**Cons:**
- May split sentences mid-way
- Less semantic coherence

**Use when:**
- You need consistent chunk sizes
- Processing speed is important
- Documents have uniform structure

### Sentence-Window Chunking (SentenceWindowNodeParser)
Creates overlapping windows around sentences for better context.

**Pros:**
- Preserves sentence boundaries
- Better semantic coherence
- Includes surrounding context

**Cons:**
- Variable chunk sizes
- More chunks created
- Slightly slower

**Use when:**
- Semantic coherence is critical
- You need context around each sentence
- Document quality varies

---

## Running the Comparison Script

The `ingestor.py` file includes a `__main__` block that compares chunking methods:

```bash
python ingestor.py
```

**Output:**
```
Chunking Method Comparison
==========================
Method                    | Chunk Size | Node Count | Avg Length
--------------------------|------------|------------|------------
Fixed (512/50)           | 512        | 12         | 487
Sentence Window (3)      | N/A        | 18         | 324
```

---

## Key Concepts

### LlamaIndex Document
A Document represents a single file or text source:
```python
from llama_index.core import Document

doc = Document(text="...", metadata={"source": "file.txt"})
```

### TextNode
A TextNode is a chunk of text with metadata:
```python
from llama_index.core.schema import TextNode

node = TextNode(
    text="chunk content",
    metadata={"source": "file.txt", "page": 1}
)
```

### Metadata
Attach custom metadata to nodes for filtering:
```python
node.metadata["department"] = "HR"
node.metadata["document_type"] = "policy"
```

---

## Sample Data Files

This module includes 3 realistic policy documents:

1. **hr_leave_policy.txt** - Annual leave, sick leave, parental leave policies
2. **hr_code_of_conduct.txt** - Professional behavior, ethics, workplace conduct
3. **it_security_policy.txt** - Password policies, data protection, security guidelines

Each file is ~300 words with proper structure for testing RAG systems.

---

## Testing the API

### Using curl

```bash
# Upload a document
curl -X POST http://localhost:8000/api/v1/ingest \
  -F "file=@data/hr_leave_policy.txt" \
  -F "chunk_size=512" \
  -F "chunk_overlap=50"
```

### Using Python

```python
import requests

with open("data/hr_leave_policy.txt", "rb") as f:
    files = {"file": f}
    data = {"chunk_size": 512, "chunk_overlap": 50}
    
    response = requests.post(
        "http://localhost:8000/api/v1/ingest",
        files=files,
        data=data
    )
    print(response.json())
```

### Using Swagger UI

1. Go to http://localhost:8000/docs
2. Click on POST /api/v1/ingest
3. Click "Try it out"
4. Upload a file and set parameters
5. Click "Execute"

---

## Common Issues

### Import errors
Make sure all dependencies are installed:
```bash
pip install -e .
```

### File upload errors
Ensure the file is a valid text or PDF file.

### Chunk size validation
- chunk_size must be between 128 and 1024
- chunk_overlap must be less than chunk_size

---

## Next Steps

After completing this module, proceed to **Module 5: Full RAG Pipeline** to embed these chunks and store them in a FAISS vector database.

---

## Experimentation Ideas

- Try different chunk sizes and compare retrieval quality
- Add support for PDF files (already included in dependencies)
- Implement custom metadata extraction (e.g., extract dates, names)
- Create a chunking strategy that preserves code blocks
- Add a GET endpoint to list all ingested documents
- Implement chunk deduplication
