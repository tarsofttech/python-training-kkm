from pydantic import BaseModel

class Addition(BaseModel):
    a: int
    b: int
