from fastapi import APIRouter, Depends, HTTPException, status, Request, Query
from database import SessionLocal
from typing import Optional
from dotenv import load_dotenv
import httpx, os




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



def api_key_check(odds_api_key, url):
        
        if not odds_api_key:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="API key not configured"
            )
        


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
async def get_odds_by_sport(
    sport: str = Query(default="soccer_england_league2"),
    regions: str = Query(default="eu", description="eu,us"), 
    markets: str = Query(default="h2h", description="h2h, spreads, totals")
    ):


    url = f"https://api.the-odds-api.com/v4/sports/{sport}/odds/?apiKey={odds_api_key}&regions={regions}&markets={markets}"

    api_key_check(odds_api_key, url)

    try:
        async with httpx.AsyncClient() as client:

            request = await client.get(url)
        
        return request.json()
    
    except httpx.RequestError as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Unexpected error: {str(e)}")