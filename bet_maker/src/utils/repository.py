from abc import ABC, abstractmethod

from sqlalchemy import select, insert, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError

from bet_maker.src.models.model import Bet, BetStatus


class AbstractRepository(ABC):
    @abstractmethod
    async def add_one(self, data: dict):
        raise NotImplementedError
    
    @abstractmethod
    async def get_all(self):
        raise NotImplementedError    
    
    @abstractmethod
    async def get_by_id(self, item_id: int):
        raise NotImplementedError
    
    @abstractmethod
    async def update_status(self, bet_id: int, new_status: BetStatus):
        raise NotImplementedError
    

class SQLAlchemyRepository(AbstractRepository):
    model = None

    def __init__(self, session:AsyncSession):
        self.session = session

    async def add_one(self, data: dict, **kwargs):
        try:
            stmt = insert(Bet).values(**data).returning(Bet.id)
            result = await self.session.execute(stmt)
            await self.session.commit()
            return result.scalar()
        except SQLAlchemyError as e:
            await self.session.rollback()
            raise Exception(f"Database error: {str(e)}")

    async def get_all(self):
        result = await self.session.execute(select(self.model))
        await self.session.commit()
        return result.scalars().all()
    
    async def get_by_id(self, item_id: int):
        """Возвращает запись по ID"""
        stmt = select(self.model).where(self.model.id == item_id)
        result = await self.session.execute(stmt)
        item = result.scalar_one_or_none()
        return item
    
    async def update_status(self, bet_id: int, new_status: BetStatus):
        """Обновляет статус ставки"""
        try:
            stmt = update(Bet).where(Bet.id == bet_id).values(status=new_status)
            await self.session.execute(stmt)
            await self.session.commit()
        except SQLAlchemyError as e:
            await self.session.rollback()
            raise Exception(f"Failed to update bet status: {str(e)}")