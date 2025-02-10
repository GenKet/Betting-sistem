from fastapi import FastAPI
from bet_maker.src.db.db import Base, engine
from bet_maker.src.api.router import all as all_routers
from bet_maker.src.models.model import Bet

from contextlib import asynccontextmanager


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Creating database tables if they don't exist...")
    async with engine.begin() as conn:
        print("Таблицы, которые должны быть созданы:", Base.metadata.tables.keys())
        await conn.run_sync(Base.metadata.create_all)
        
    yield
    
    print("Shutting down application...")

app = FastAPI(lifespan=lifespan)

for router in all_routers:
    app.include_router(router)