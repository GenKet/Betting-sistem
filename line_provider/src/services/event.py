from typing import List, Union
from line_provider.src.models.event import Event, EventStatus
from line_provider.src.repository.event import EventRepository

class EventService:
    def __init__(self, repo: EventRepository):
        self.repo = repo

    async def create_event(self, event: Event) -> Event:
        return await self.repo.create(event)

    async def list_events(self) -> List[Event]:
        return await self.repo.list_all()

    async def update_event_status(self, event_id: Union[int, str], status: EventStatus) -> Event:
        event = await self.repo.update_status(event_id, status)

        return event

    async def get_unfinished_events(self) -> List[Event]:
        return await self.repo.get_unfinished_events()
    