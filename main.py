from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie
from sportsbook.models_mongo import Bet, PostRequest, Post, Event
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from apscheduler.schedulers.background import BackgroundScheduler
from sqlmodel import SQLModel
import os

from scheduler.scheduler import scheduler, asyncscheduler

from database import engine
from databasemongo import MONGO_URI, MONGO_DB_NAME
from auth.routers import router as auth_router
from casino.routers import router as casino_router
from funds.routers import router as funds_router
from sportsbook.routers import router as sportsbook_router


templates = Jinja2Templates(directory="templates")


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Initialize DB and other resources on startup."""
    SQLModel.metadata.create_all(engine)
    print("Database tables created")
    mongo_client = AsyncIOMotorClient(MONGO_URI)
    await init_beanie(
        database=mongo_client[MONGO_DB_NAME], 
        document_models=[Bet, PostRequest, Post, Event]  # Add all your Beanie models here
    )
    print("MongoDB initialized")
    scheduler.start()
    print("scheduler started")
    asyncscheduler.start()
    print("Async scheduler started")
    
    yield
    
    # Cleanup on shutdown
    print("Shutting down")
    scheduler.shutdown()
    mongo_client.close()


app = FastAPI(lifespan=lifespan)

origins = [
    "http://localhost:5173",
    # add any additional origins if necessary
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,  # if you are handling cookies or auth headers
    allow_methods=["*"],     # or specify specific methods, e.g., ["GET", "POST"]
    allow_headers=["*"],     # or specify specific headers
)

app.mount("/static", StaticFiles(directory="static"), name="static")
app.include_router(auth_router)
app.include_router(casino_router)
app.include_router(funds_router)
app.include_router(sportsbook_router)



@app.get("/", response_class=HTMLResponse)
async def home_page(request: Request):
    """Render the home page."""
    return templates.TemplateResponse("home.html", {"request": request})


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)