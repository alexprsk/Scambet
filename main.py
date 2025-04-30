from fastapi import FastAPI, Request
import uvicorn
from routers import auth
from funds import routers, models, schema
from sqlmodel import SQLModel
from database import engine
from contextlib import asynccontextmanager
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse

import time



@asynccontextmanager
async def lifespan(app: FastAPI):
    # Create all database tables on startup
    SQLModel.metadata.create_all(engine)
    print("Database tables created")
    yield
    # Clean up on shutdown if needed
    print("Shutting down")

app = FastAPI(lifespan=lifespan)


templates = Jinja2Templates(directory="templates")

app.mount("/static", StaticFiles(directory="./static"), name="static")




@app.get("/")
async def home_page(request: Request):
        
        return templates.TemplateResponse(
        request=request, name="home.html")


app.include_router(auth.router)
app.include_router(routers.router)



if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)