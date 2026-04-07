from datetime import datetime

from pydantic import BaseModel, Field, field_validator, ConfigDict, field_serializer


class ItemCreate(BaseModel):
    name: str = Field(min_length=2, max_length=100)
    description: str | None = None
    price: int = Field(gt=0)

    @field_validator("name")
    @classmethod
    def validate_name(cls, v: str) -> str:
        v = v.strip()
        if any(char.isdigit() for char in v):
            raise ValueError("Name cannot contain digits")
        return v


class ItemUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=2, max_length=100)
    description: str | None = None
    price: int | None = Field(default=None, gt=0)
    is_active: bool | None = None


class ItemResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    description: str | None
    price: int
    is_active: bool
    created_at: str | None
    updated_at: str | None

    @field_serializer("created_at")
    def serialize_created_at(self, v: datetime | None) -> str | None:
        if v is None:
            return None
        return v.isoformat()

    @field_serializer("updated_at")
    def serialize_updated_at(self, v: datetime | None) -> str | None:
        if v is None:
            return None
        return v.isoformat()
