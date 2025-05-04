from fastapi import APIRouter, Depends, HTTPException, status, Request, Query
from database import SessionLocal, Session
from typing import Optional, Annotated
from dotenv import load_dotenv
import httpx, os

from sportsbook.models import Events, BookMakers, Markets, Outcomes


router = APIRouter(
    prefix= "/sportsbook",
     tags=['sportsbook']
)

load_dotenv()

odds_api_key=os.getenv("ODDS_API_KEY")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]

def api_key_check(odds_api_key, url):
        
        if not odds_api_key:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="API key not configured"
            )
        

def insert_games_in_db(response, db):

    for game_data in response:

        event = Events(

            event_id = game_data["id"],
            sport_key = game_data["sport_key"],
            sport_title = game_data["sport_title"],
            commence_time = game_data["commence_time"],
            home_team = game_data["home_team"],
            away_team = game_data["away_team"]

        )

        db.add(event)
        db.commit()

        for bookmaker_data in game_data["bookmakers"]:

            bookmaker = BookMakers(key = bookmaker_data["key"],
            title = bookmaker_data["title"],
            last_update = bookmaker_data["last_update"],
            event_id = game_data["id"]
            )

        db.add(bookmaker)
        db.commit()






@router.get('/sports', status_code=status.HTTP_200_OK)
async def get_all_sports():


    url = f"https://api.the-odds-api.com/v4/sports/?apiKey={odds_api_key}"

    api_key_check(odds_api_key, url)

    try:
        async with httpx.AsyncClient() as client:
            request= await client.get(url)

            if request.status_code != 200:
                raise HTTPException(status_code=request.status_code, detail= request.text)
            

        return request.json()
    
    except httpx.RequestError as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Unexpected error: {str(e)}")
    



@router.get('/events', status_code=status.HTTP_200_OK)
async def get_events_by_sport(sport: str):


    url = f"https://api.the-odds-api.com/v4/sports/{sport}/events/?apiKey={odds_api_key}"

    api_key_check(odds_api_key, url)

    try:
        async with httpx.AsyncClient() as client:

            request = await client.get(url)

        return request.json()
    
    except httpx.RequestError as e:
        raise Exception(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Unexpected error: {str(e)}")
    



@router.get('/odds', status_code=status.HTTP_200_OK)
async def get_odds_by_sport(db: db_dependency,
    sport: str = Query(default="soccer_england_league2"),
    regions: str = Query(default="eu", description="eu,us"), 
    markets: str = Query(default="h2h", description="h2h, spreads, totals")
    ):


    url = f"https://api.the-odds-api.com/v4/sports/{sport}/odds/?apiKey={odds_api_key}&regions={regions}&markets={markets}"

    api_key_check(odds_api_key, url)

    try:
        async with httpx.AsyncClient() as client:

            request = await client.get(url)
            insert_games_in_db(request.json(), db)
        
        return request.json()
    
    except httpx.RequestError as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Unexpected error: {str(e)}")