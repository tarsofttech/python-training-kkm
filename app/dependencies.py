from dataclasses import dataclass

from fastapi import Query, Header, HTTPException

from app.config import settings


@dataclass
class Pagination:
    skip: int = Query(default=0, ge=0)
    limit: int = Query(default=10, ge=1, le=100)


def require_api_key(x_api_key: str = Header(...)) -> str:
    if x_api_key != settings.API_KEY:
        raise HTTPException(status_code=401, detail="Invalid API key")
    return x_api_key
