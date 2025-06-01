from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie
from sportsbook.models_mongo import Bet,  Event
import os


MONGO_URI = 'mongodb://mongodb:27017'
MONGO_DB_NAME= 'PlayerBets'

async def init_db():
    client = AsyncIOMotorClient(MONGO_URI)
    await init_beanie(database=client[MONGO_DB_NAME], document_models=[Event, Bet])
