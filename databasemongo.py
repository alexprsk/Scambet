from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie
from sportsbook.models_mongo import Bets,  Event
import os
from dotenv import load_dotenv

load_dotenv("prod.env")

MONGO_URI = os.getenv("MONGO_URI")
   

MONGO_DB_NAME= 'PlayerBets'

async def init_db():
    client = AsyncIOMotorClient(MONGO_URI)
    await init_beanie(database=client[MONGO_DB_NAME], document_models=[Event, Bets])