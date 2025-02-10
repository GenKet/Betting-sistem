import asyncio
import random
from datetime import datetime
from line_provider.src.models.event import EventStatus
from line_provider.src.services.event import EventService


CHECK_INTERVAL = 10

async def monitor_events(service: EventService):
    while True:
        unfinished_events = await service.get_unfinished_events()
        now = datetime.utcnow()
        for event in unfinished_events:
            if now >= event.deadline:
                new_status = random.choice([EventStatus.TEAM_1_WIN, EventStatus.TEAM_2_WIN])
                try:
                    await service.update_event_status(event.id, new_status)
                    print(f"Event {event.id} deadline passed. Updated status to {new_status}.")
                except Exception as e:
                    print(f"Error updating event {event.id}: {e}")
        await asyncio.sleep(CHECK_INTERVAL)
