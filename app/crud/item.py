from sqlalchemy.orm import Session
from sqlalchemy import func

from app.models.item import Item
from app.schemas.item import ItemCreate, ItemUpdate


def get_item(db: Session, item_id: int) -> Item | None:
    return db.query(Item).filter(Item.id == item_id).first()


def get_items(
    db: Session, skip: int = 0, limit: int = 10, q: str | None = None
) -> tuple[list[Item], int]:
    query = db.query(Item)
    if q:
        query = query.filter(Item.name.ilike(f"%{q}%"))
    total = query.count()
    items = query.offset(skip).limit(limit).all()
    return (items, total)


def create_item(db: Session, data: ItemCreate) -> Item:
    db_item = Item(
        name=data.name,
        description=data.description,
        price=data.price,
    )
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


def update_item(db: Session, item_id: int, data: ItemUpdate) -> Item | None:
    db_item = get_item(db, item_id)
    if not db_item:
        return None

    update_data = data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_item, field, value)

    db.commit()
    db.refresh(db_item)
    return db_item


def delete_item(db: Session, item_id: int) -> bool:
    db_item = get_item(db, item_id)
    if not db_item:
        return False
    db.delete(db_item)
    db.commit()
    return True
