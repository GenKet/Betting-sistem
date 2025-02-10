from datetime import datetime
from pydantic import BaseModel, Field
from typing import Union
from line_provider.src.models.event import EventStatus

class EventCreate(BaseModel):
    id: Union[int, str] = Field(..., description="Уникальный идентификатор")
    name: str = Field(..., description="Название события")
    odds: float = Field(..., gt=0, description="Коэффициент ставки")
    deadline: datetime = Field(..., description="Дедлайн для ставок")

class EventUpdate(BaseModel):
    status: EventStatus

class EventResponse(BaseModel):
    id: Union[int, str]
    name: str 
    odds: float
    deadline: datetime
    status: EventStatus

    class Config:
        orm_mode = True
