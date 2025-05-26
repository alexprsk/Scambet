from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie
from sportsbook.models_mongo import Bet, PostRequest, Post

MONGO_URI= 'mongodb://localhost:27017'
MONGO_DB_NAME= 'PlayerBets'

async def init_db():
    client = AsyncIOMotorClient(MONGO_URI)
    await init_beanie(database=client.blog, document_models=[Bet,Post, PostRequest])
