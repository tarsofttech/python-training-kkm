from fastapi import FastAPI, Request, HTTPException, Depends
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordRequestForm

from app.routers import item
from app.exceptions import ItemNotFoundError, DuplicateItemError
from app.auth import create_access_token, get_current_user

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
