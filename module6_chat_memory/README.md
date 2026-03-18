# Module 6: Chat Memory and Sessions

Add multi-turn conversation support to the RAG system with session-based memory management and metadata filtering. This module extends Module 5 with conversational capabilities.

---

## What You'll Learn

- Implementing session-based chat memory
- Using LlamaIndex's CondensePlusContextChatEngine
- Managing multiple concurrent chat sessions
- Retrieving conversation history
- Filtering documents by metadata (e.g., department)
- Session lifecycle management (create, get, delete)

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

3. **Completed Module 5** (Full RAG Pipeline)

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

3. **Build the index**
   ```bash
   # Ingest documents first (see Module 5)
   ```

4. **Start the server**
   ```bash
   uvicorn main:app --reload
   ```

5. **Access the API**
   - Swagger UI: http://localhost:8000/docs
   - Chat endpoint: http://localhost:8000/api/v1/chat
   - Sessions: http://localhost:8000/api/v1/sessions

---

## Project Structure

```
module6_chat_memory/
├── main.py              # FastAPI app with chat manager
├── schemas.py           # Chat-specific Pydantic models
├── rag_engine.py        # Extended RAG engine with filtering
├── chat_manager.py      # Session-based chat management
├── routers/
│   ├── ingest.py        # Document ingestion
│   ├── query.py         # Single-turn queries
│   └── chat.py          # Multi-turn chat endpoints
└── data/
    ├── hr_leave_policy.txt
    ├── hr_code_of_conduct.txt
    └── it_security_policy.txt
```

---

## API Endpoints

### POST /api/v1/chat
Send a message in a chat session.

**Request:**
```json
{
  "session_id": "user123",
  "message": "How many vacation days do I get?"
}
```

**Response:**
```json
{
  "session_id": "user123",
  "response": "You are entitled to 14 days of annual leave per year...",
  "sources": ["hr_leave_policy.txt (score: 0.89)"]
}
```

### GET /api/v1/sessions
List all active chat sessions.

**Response:**
```json
{
  "sessions": ["user123", "user456"],
  "count": 2
}
```

### GET /api/v1/sessions/{session_id}/history
Get conversation history for a session.

**Response:**
```json
{
  "session_id": "user123",
  "messages": [
    {"role": "user", "content": "How many vacation days?"},
    {"role": "assistant", "content": "You are entitled to 14 days..."}
  ],
  "message_count": 2
}
```

### DELETE /api/v1/sessions/{session_id}
Delete a chat session.

**Response:**
```json
{
  "status": "deleted",
  "session_id": "user123"
}
```

---

## How Chat Memory Works

### Session Management
Each user gets a unique session ID that tracks their conversation:
```
Session ID → Chat Engine → Conversation History
```

### CondensePlusContextChatEngine
LlamaIndex's chat engine that:
1. Condenses conversation history into a standalone question
2. Retrieves relevant context from the index
3. Generates a response considering both history and context

### Conversation Flow
```
User Message → Condense with History → Retrieve Context → Generate Response → Store in History
```

---

## Key Concepts

### Session Persistence
Sessions are stored in-memory (dict). In production, use Redis or a database.

### Context Window
The chat engine maintains conversation history to provide context-aware responses.

### Metadata Filtering
Filter retrieval by document metadata:
```python
filters = MetadataFilters(
    filters=[
        MetadataFilter(key="department", value="HR")
    ]
)
```

---

## Testing Chat Sessions

### Start a conversation

```bash
# First message
curl -X POST http://localhost:8000/api/v1/chat \
  -H "Content-Type: application/json" \
  -d '{
    "session_id": "alice",
    "message": "How many vacation days do I get?"
  }'

# Follow-up (uses conversation context)
curl -X POST http://localhost:8000/api/v1/chat \
  -H "Content-Type: application/json" \
  -d '{
    "session_id": "alice",
    "message": "Can I carry them forward to next year?"
  }'

# Another follow-up
curl -X POST http://localhost:8000/api/v1/chat \
  -H "Content-Type: application/json" \
  -d '{
    "session_id": "alice",
    "message": "What about sick leave?"
  }'
```

### View conversation history

```bash
curl http://localhost:8000/api/v1/sessions/alice/history
```

### List all sessions

```bash
curl http://localhost:8000/api/v1/sessions
```

### Delete a session

```bash
curl -X DELETE http://localhost:8000/api/v1/sessions/alice
```

---

## Metadata Filtering Example

Documents are tagged with department metadata during ingestion:
- `hr_leave_policy.txt` → `department: HR`
- `hr_code_of_conduct.txt` → `department: HR`
- `it_security_policy.txt` → `department: IT`

Query with filtering:
```python
# Only search HR documents
result = await rag_engine.query_with_filter(
    question="What is the leave policy?",
    filter_key="department",
    filter_value="HR",
    top_k=3
)
```

---

## ChatSessionManager Methods

### `create_session(session_id: str, index) -> None`
Create a new chat session with a chat engine.

### `get_or_create(session_id: str, index) -> ChatEngine`
Get existing session or create if doesn't exist.

### `chat(session_id: str, message: str, index) -> dict`
Send a message and get a response.

### `get_history(session_id: str) -> List[dict]`
Get all messages in a session.

### `delete_session(session_id: str) -> bool`
Delete a session and its history.

### `list_sessions() -> List[str]`
Get all active session IDs.

---

## Common Issues

### Session not found
Sessions are created automatically on first message.

### Context not maintained
Ensure you're using the same session_id for follow-up messages.

### Memory usage
Sessions are stored in-memory. Implement cleanup for old sessions in production.

---

## Next Steps

After completing this module, proceed to **Module 7: RAG Evaluation** to learn how to measure and improve RAG quality.

---

## Experimentation Ideas

- Implement session timeout (auto-delete after inactivity)
- Add session persistence with Redis
- Implement conversation summarization for long chats
- Add user authentication and session ownership
- Create a streaming chat endpoint
- Implement conversation branching (save/restore points)
- Add sentiment analysis to chat messages
