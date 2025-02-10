from typing import List

from fastapi import APIRouter, Depends

from bet_maker.src.services.event_messaging import EventMessagingService
from bet_maker.src.schemas.event import EventSchema


router_event = APIRouter(
    prefix="/events",
    tags=["Events"]
)

@router_event.get("", response_model=List[EventSchema])
async def get_all_events(event_messaging: EventMessagingService = Depends()):
    events = await event_messaging.request_events()
    return events