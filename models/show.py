from pydantic import BaseModel

class Show(BaseModel):
    name: str
    value: int