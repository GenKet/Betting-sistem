from bet_maker.src.models.model import BetStatus
from bet_maker.src.schemas.bet import BetSchemaAdd, BetSchemaResponse
from bet_maker.src.repository.bet import BetRepository
from bet_maker.src.utils.repository import AbstractRepository

from fastapi import HTTPException



class BetService:
    def __init__(self, repository: AbstractRepository):
        self.repository = repository
        
    async def add_one(self, bet: BetSchemaAdd) -> int:
        bet_dict = bet.model_dump()
        bet_id = await self.repository.add_one(bet_dict)
        return bet_id
        
    async def get_all(self):
        bets = await self.repository.get_all()
        return bets
    
    async def get_by_id(self, bet_id: int) -> BetSchemaResponse:
        bet = await self.repository.get_by_id(bet_id)



        if not bet:
            raise HTTPException(status_code=404, detail="Bet not found")
        return BetSchemaResponse(**bet.__dict__)
    
    async def update_bet_status(self, bet_id: int, new_status: BetStatus):
        bet = await self.repository.get_by_id(bet_id)
        if not bet:
            raise HTTPException(status_code=404, detail="Bet not found")
        await self.repository.update_status(bet_id, new_status)
    
