from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

from app.routers import item
from app.exceptions import ItemNotFoundError, DuplicateItemError

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
