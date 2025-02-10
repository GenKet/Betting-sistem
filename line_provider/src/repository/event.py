from typing import Dict, List, Union
from line_provider.src.models.event import Event, EventStatus

class EventRepository:
    def __init__(self):
        self._events: Dict[Union[int, str], Event] = {}

    async def create(self, event: Event) -> Event:
        self._events[str(event.id)] = event
        return event

    async def list_all(self) -> List[Event]:
        return list(self._events.values())

    async def update_status(self, event_id: Union[int, str], status: EventStatus) -> Event:
        print(self._events)
        if str(event_id) in self._events:
            self._events[str(event_id)].status = status
            return self._events[event_id]
        raise ValueError("Event not found")

    async def get_unfinished_events(self) -> List[Event]:
        return [e for e in self._events.values() if e.status == EventStatus.UNFINISHED]
