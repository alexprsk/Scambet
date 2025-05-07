from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from sqlmodel import SQLModel
import os

from database import engine
from auth.routers import router as auth_router
from casino.routers import router as casino_router
from funds.routers import router as funds_router
from sportsbook.routers import router as sportsbook_router
from tests.routers import router as tests_router



templates = Jinja2Templates(directory="templates")


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Initialize DB and other resources on startup."""
    SQLModel.metadata.create_all(engine)
    print("Database tables created")
    yield
    print("Shutting down")


app = FastAPI(lifespan=lifespan)



app.mount("/static", StaticFiles(directory="static"), name="static")
app.include_router(auth_router)
app.include_router(casino_router)
app.include_router(funds_router)
app.include_router(sportsbook_router)
app.include_router(tests_router)


@app.get("/", response_class=HTMLResponse)
async def home_page(request: Request):
    """Render the home page."""
    return templates.TemplateResponse("home.html", {"request": request})


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)