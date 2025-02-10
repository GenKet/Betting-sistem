from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException

from bet_maker.src.api.dependencies import bet_service
from bet_maker.src.schemas.bet import BetSchemaAdd, BetSchemaResponse
from bet_maker.src.services.bet import BetService


router = APIRouter(
    prefix="/bet",
    tags=["Bet"]
)

@router.get("/{bet_id}", response_model=BetSchemaResponse)
async def get_bet_by_id(
    bet_id: int,
    bet_service: Annotated[BetService, Depends(bet_service)],
):
    bet = await bet_service.get_by_id(bet_id)
    if not bet:
        raise HTTPException(status_code=404, detail="Bet not found")
    return bet


@router.post("")
async def add_one(
    bet: BetSchemaAdd,
    bet_service: Annotated[BetService, Depends(bet_service)],
):
    bet_id = await bet_service.add_one(bet)
    return {"bet_id": bet_id}

