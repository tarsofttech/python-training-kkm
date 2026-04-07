from fastapi import APIRouter, Depends, HTTPException, Query, Response

from sqlalchemy.orm import Session

from app.database import get_db
from app.crud import item as crud_item
from app.schemas.item import ItemCreate, ItemUpdate, ItemResponse
from app.dependencies import Pagination
from app.exceptions import ItemNotFoundError

router = APIRouter()


@router.post("/", status_code=201, response_model=ItemResponse)
def create_item(data: ItemCreate, db: Session = Depends(get_db)) -> ItemResponse:
    db_item = crud_item.create_item(db, data)
    return db_item


@router.get("/")
def list_items(
    pagination: Pagination = Depends(),
    q: str | None = Query(default=None),
    db: Session = Depends(get_db),
) -> dict:
    items, total = crud_item.get_items(db, skip=pagination.skip, limit=pagination.limit, q=q)
    return {"total": total, "items": [ItemResponse.model_validate(item) for item in items]}


@router.get("/{item_id}", response_model=ItemResponse)
def read_item(item_id: int, db: Session = Depends(get_db)) -> ItemResponse:
    db_item = crud_item.get_item(db, item_id)
    if not db_item:
        raise ItemNotFoundError(item_id)
    return db_item


@router.put("/{item_id}", response_model=ItemResponse)
def update_item(
    item_id: int, data: ItemUpdate, db: Session = Depends(get_db)
) -> ItemResponse:
    db_item = crud_item.update_item(db, item_id, data)
    if not db_item:
        raise ItemNotFoundError(item_id)
    return db_item


@router.delete("/{item_id}", status_code=204)
def delete_item(item_id: int, db: Session = Depends(get_db)) -> Response:
    success = crud_item.delete_item(db, item_id)
    if not success:
        raise ItemNotFoundError(item_id)
    return Response(status_code=204)
