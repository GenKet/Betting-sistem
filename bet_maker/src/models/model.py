import enum
from decimal import Decimal
from sqlalchemy import Numeric, Enum
from sqlalchemy.orm import Mapped, mapped_column
from bet_maker.src.db.db import Base

class BetStatus(enum.Enum):
    PENDING = "pending"
    WON = "won"
    LOST = "lost"

class Bet(Base):
    __tablename__ = "bet"

    id: Mapped[int] = mapped_column(primary_key=True)
    event_id: Mapped[int] = mapped_column()
    amount: Mapped[Decimal] = mapped_column(Numeric(10, 2))
    status: Mapped[BetStatus] = mapped_column(Enum(BetStatus), default=BetStatus.PENDING)


    
