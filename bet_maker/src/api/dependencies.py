from typing import Annotated
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from bet_maker.src.db.db import get_async_session
from bet_maker.src.services.bet import BetService
from bet_maker.src.repository.bet import BetRepository


def bet_service(session: Annotated[AsyncSession, Depends(get_async_session)]) -> BetService:
    repository = BetRepository(session)
    return BetService(repository)
