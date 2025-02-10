from fastapi import APIRouter, HTTPException
from typing import Union
from line_provider.src.schemas.event import EventCreate, EventUpdate, EventResponse
from line_provider.src.core.dependecies import repo
from line_provider.src.models.event import Event, EventStatus
from line_provider.src.repository.event import EventRepository
from line_provider.src.services.event import EventService

router = APIRouter()
service = EventService(repo)

@router.post("/events/", response_model=EventResponse)
async def create_event(event_create: EventCreate):
    event = Event(**event_create.model_dump(), status=EventStatus.UNFINISHED)
    return await service.create_event(event)

@router.get("/events/", response_model=list[EventResponse])
async def list_events():
    return await service.list_events()

@router.patch("/events/{event_id}/status/", response_model=EventResponse)
async def update_event_status(event_id: Union[int, str], update: EventUpdate):
    try:
        return await service.update_event_status(event_id, update.status)
    except ValueError:
        raise HTTPException(status_code=404, detail="Event not found")
