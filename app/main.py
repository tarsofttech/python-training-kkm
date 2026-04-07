from fastapi import FastAPI, Request, HTTPException, Depends
from fastapi.responses import JSONResponse, StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel
import httpx

from app.routers import item
from app.exceptions import ItemNotFoundError, DuplicateItemError
from app.auth import create_access_token, get_current_user
from app.schemas.chat import ChatRequest

app = FastAPI(
    title="Items API",
    version="1.0.0",
    description="FastAPI CRUD Training",
)


@app.exception_handler(ItemNotFoundError)
def item_not_found_handler(request: Request, exc: ItemNotFoundError) -> JSONResponse:
    return JSONResponse(
        status_code=404,
        content={"detail": f"Item with id {exc.item_id} not found"},
    )


@app.exception_handler(DuplicateItemError)
def duplicate_item_handler(request: Request, exc: DuplicateItemError) -> JSONResponse:
    return JSONResponse(
        status_code=409,
        content={"detail": f"Item with name '{exc.name}' already exists"},
    )


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(item.router, prefix="/items", tags=["Items"])


@app.get("/health")
def health_check() -> dict:
    return {"status": "ok"}


@app.post("/auth/token")
def login(form_data: OAuth2PasswordRequestForm = Depends()) -> dict:
    # Simple demo: accept any username/password (in real app, verify against DB)
    if not form_data.username or not form_data.password:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    access_token = create_access_token(data={"sub": form_data.username})
    return {"access_token": access_token, "token_type": "bearer"}


@app.get("/auth/me")
def read_users_me(current_user: str = Depends(get_current_user)) -> dict:
    return {"username": current_user}


@app.post("/chat")
async def chat_with_ollama(request: ChatRequest) -> dict:
    """Chat with Ollama LLM."""
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                "http://localhost:11434/api/chat",
                json={
                    "model": request.model,
                    "messages": [{"role": "user", "content": request.message}],
                    "stream": False
                },
                timeout=60.0
            )
            response.raise_for_status()
            data = response.json()
            return {
                "response": data.get("message", {}).get("content", ""),
                "model": request.model
            }
    except httpx.ConnectError:
        raise HTTPException(
            status_code=503,
            detail="Ollama not running. Start it with: ollama serve"
        )
    except httpx.TimeoutException:
        raise HTTPException(
            status_code=504,
            detail="Ollama request timed out"
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error communicating with Ollama: {str(e)}"
        )