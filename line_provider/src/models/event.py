from enum import Enum
from datetime import datetime
from pydantic import BaseModel, Field
from typing import Union

class EventStatus(str, Enum):
    UNFINISHED = "unfinished"
    TEAM_1_WIN = "team_1_win"
    TEAM_2_WIN = "team_2_win"


EventName = [
    "Ливерпуль-Эвертон",
    "Арсенал-Реал-Мадрид",
    "Челси-Барселона",
    "Манчестер-Сити-Манчестер-Юнайтед", 
    "Бавария-Боруссия",
    "Лестер-ПСЖ",
]

class Event(BaseModel):
    id: Union[int, str] = Field(..., description="Id события")
    name: str = Field(..., description="Название события")
    odds: float = Field(..., gt=0, description="Коэффициент ставки")
    deadline: datetime = Field(..., description="Дедлайн ставок")
    status: EventStatus = Field(EventStatus.UNFINISHED, description="Текущий статус")
