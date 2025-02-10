from pydantic import BaseModel
from decimal import Decimal
from enum import Enum


class BetStatus(str, Enum):
    PENDING = "pending"  
    WON = "won"  
    LOST = "lost"


class BetSchemaBase(BaseModel):
    pass


class BetSchemaAdd(BetSchemaBase):
    event_id: int
    amount: Decimal
    
class BetSchemaResponse(BetSchemaBase):
    id: int
    event_id: int
    amount: Decimal
    status: BetStatus