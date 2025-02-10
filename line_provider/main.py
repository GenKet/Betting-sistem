import asyncio
from fastapi import FastAPI
from line_provider.src.schemas.event import EventCreate
from line_provider.src.api.event import router as router_event
from line_provider.src.core.scheduler import monitor_events
from line_provider.src.core.dependecies import repo
from line_provider.src.services.event import EventService
from line_provider.src.services.event_request_handler import event_request_handler
from line_provider.src.models.event import Event, EventStatus, EventName
from datetime import datetime, timedelta
import random

from contextlib import asynccontextmanager


service = EventService(repo)

@asynccontextmanager
async def lifespan(app: FastAPI):
    if not (await repo.list_all()):
        for i in range(1, 4):
            event_create = EventCreate(
                id=i,
                name=random.choice(EventName),
                odds=round(random.uniform(1.50, 3.00), 2),
                deadline=datetime.utcnow() + timedelta(seconds=random.randint(30, 90)),
            )
            event = Event(**event_create.model_dump(), status=EventStatus.UNFINISHED)
            await service.create_event(event)
        print("Created 3 random events.")
        asyncio.create_task(monitor_events(service))
        
        rabbitmq_task = asyncio.create_task(event_request_handler())
    
    yield
    
    rabbitmq_task.cancel()
    try:
        await rabbitmq_task
    except asyncio.CancelledError:
        print("[❌] Обработчик RabbitMQ остановлен.")
    print("Shutting down application...")

app = FastAPI(
    title="Line Provider Service", 
    lifespan=lifespan,
)

app.include_router(router_event, prefix="/api")

