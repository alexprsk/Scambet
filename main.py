from fastapi import FastAPI
from routers import auth
from sqlmodel import SQLModel
from database import engine
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Create all database tables on startup
    SQLModel.metadata.create_all(engine)
    print("Database tables created")
    yield
    # Clean up on shutdown if needed
    print("Shutting down")

app = FastAPI(lifespan=lifespan)

@app.get("/")
async def home_page():
    return {"Message": "Welcome to ScamBet"}

app.include_router(auth.router)

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)