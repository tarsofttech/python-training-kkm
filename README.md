# FastAPI CRUD Training Project

A production-ready FastAPI CRUD application with SQLAlchemy, MySQL, Alembic migrations, JWT authentication, and comprehensive validation.

## Prerequisites

- Python 3.11+
- MySQL database
- `pip` or `uv` package manager

## Setup Steps

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd fastapi_crud
   ```

2. **Create and activate virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies using uv**
   ```bash
   uv pip install -r requirements.txt
   ```

4. **Copy environment file and edit**
   ```bash
   cp .env.example .env
   ```
   Edit `.env` with your actual database credentials and secrets:
   ```
   DATABASE_URL=mysql+pymysql://user:password@localhost/fastapi_db
   API_KEY=your-secret-api-key
   SECRET_KEY=your-jwt-secret-key
   DEBUG=False
   ```

5. **Run migrations**
   ```bash
   alembic revision --autogenerate -m "init"
   alembic upgrade head
   ```

6. **Run the server**
   ```bash
   uvicorn app.main:app --reload
   ```

7. **Test at**
   - Interactive docs: http://localhost:8000/docs
   - Health check: http://localhost:8000/health

## Authentication

All CRUD endpoints require JWT authentication.

### 1. Get Access Token
```bash
curl -X POST "http://localhost:8000/auth/token" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=testuser&password=testpass"
```

Response:
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

### 2. Use Token in Requests
Add the Authorization header to all CRUD requests:
```bash
curl "http://localhost:8000/items/" \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
```

### 3. Verify Current User
```bash
curl -H "Authorization: Bearer your-token" http://localhost:8000/auth/me
```

## CRUD Endpoints

### 1. Create Item (POST /items/)
```bash
# First get token
TOKEN=$(curl -s -X POST "http://localhost:8000/auth/token" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=testuser&password=testpass" | jq -r '.access_token')

# Create item with token
curl -X POST "http://localhost:8000/items/" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Laptop",
    "description": "High-performance laptop",
    "price": 1200
  }'
```

### 2. List Items (GET /items/)
```bash
# Get token first
TOKEN=$(curl -s -X POST "http://localhost:8000/auth/token" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=testuser&password=testpass" | jq -r '.access_token')

# List items
curl "http://localhost:8000/items/?skip=0&limit=10" \
  -H "Authorization: Bearer $TOKEN"
```

Search items:
```bash
curl "http://localhost:8000/items/?q=laptop&skip=0&limit=10" \
  -H "Authorization: Bearer $TOKEN"
```

### 3. Get Single Item (GET /items/{item_id})
```bash
# Get token first
TOKEN=$(curl -s -X POST "http://localhost:8000/auth/token" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=testuser&password=testpass" | jq -r '.access_token')

curl "http://localhost:8000/items/1" \
  -H "Authorization: Bearer $TOKEN"
```

### 4. Update Item (PUT /items/{item_id})
```bash
# Get token first
TOKEN=$(curl -s -X POST "http://localhost:8000/auth/token" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=testuser&password=testpass" | jq -r '.access_token')

curl -X PUT "http://localhost:8000/items/1" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Gaming Laptop",
    "price": 1500
  }'
```

### 5. Delete Item (DELETE /items/{item_id})
```bash
# Get token first
TOKEN=$(curl -s -X POST "http://localhost:8000/auth/token" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=testuser&password=testpass" | jq -r '.access_token')

curl -X DELETE "http://localhost:8000/items/1" \
  -H "Authorization: Bearer $TOKEN"
```

## Features

- **CRUD Operations**: Full Create, Read, Update, Delete for items
- **Pagination**: Configurable skip/limit with dataclass dependency
- **Search**: Case-insensitive name search with `?q=` parameter
- **Validation**: Pydantic v2 schemas with custom validators
- **Error Handling**: Custom exceptions with proper HTTP status codes
- **Database**: SQLAlchemy ORM with MySQL
- **Migrations**: Alembic for database schema management
- **Security**: JWT authentication helpers and API key validation
- **CORS**: Configured for development
- **OpenAPI**: Auto-generated docs at `/docs`

## Project Structure

```
fastapi_crud/
├── app/
│   ├── main.py           # FastAPI app factory
│   ├── config.py         # Pydantic settings
│   ├── database.py       # SQLAlchemy setup
│   ├── dependencies.py   # Common dependencies
│   ├── exceptions.py     # Custom exceptions
│   ├── auth.py           # JWT utilities
│   ├── models/           # SQLAlchemy models
│   ├── schemas/          # Pydantic schemas
│   ├── crud/             # Database operations
│   └── routers/          # API endpoints
├── alembic/              # Migration scripts
├── alembic.ini           # Alembic config
├── .env.example          # Environment template
├── requirements.txt      # Dependencies
└── README.md             # This file
```
