from pydantic import BaseModel
from typing import Optional

class EventSchema(BaseModel):
    id: int
    name: Optional[str] = None
    odds: float
    deadline: str
    status: str