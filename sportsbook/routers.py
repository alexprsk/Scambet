from fastapi import APIRouter, Depends, HTTPException, status, Request, Query, Body
from apscheduler.schedulers.background import BackgroundScheduler  
from apscheduler.triggers.interval import IntervalTrigger 
from database import SessionLocal
from datetime import datetime, timezone
from sqlmodel import Session, select, update, insert, values, desc
from typing import Optional, Annotated, List
from dotenv import load_dotenv

import httpx, os,asyncio
import random
import time

from scheduler.scheduler import scheduler, asyncscheduler

from sportsbook.models import Events, OddsSnapshot
from sportsbook.models_mongo import Bet, PostRequest, Post, Event, Bookmaker
from sportsbook.utils import insert_events_from_api

from sportsbook.schemas import Bet
from tests.models import TestOddsSnapshot
from utilities.random_odds import random_odds_generator

router = APIRouter(
    prefix= "/sportsbook",
     tags=['sportsbook']
)

load_dotenv()

odds_api_key=os.getenv("ODDS_API_KEY")



#-----------------------------------------#
#--------------- FUNCTIONS ---------------#
#-----------------------------------------#

inserted = []
    
async def my_async_task():
    print(f"Async Task is running at {datetime.now()}")
    global inserted
    print(f"globalinserted: {inserted}")
    inserted = []
    print(f"inserted: {inserted}")
    start_time = time.perf_counter()
    async with httpx.AsyncClient() as client:

            url = f"https://api.the-odds-api.com/v4/sports/upcoming/odds/?apiKey={odds_api_key}&regions=us,eu&markets=h2h&bookmakers=pinnacle"
            try:
                response = await client.get(url)
                response.raise_for_status()
                data = response.json()

                inserted.append(data)
                print(f"Appendedinserted: {inserted}")

                await insert_events_from_api(data)
            except httpx.HTTPStatusError as e:
                print(f"HTTP error for {response}: {e.response.text}")
            except httpx.RequestError as e:
                print(f"Request error for {response}: {str(e)}")
            except Exception as e:
                print(f"Unexpected error for {response}: {str(e)}")

    end_time = time.perf_counter()

    print({"inserted_count": len(inserted),"duration_seconds": round(end_time - start_time, 2)})
    return {

        "events": inserted
    }

    # ... additional task code goes here ...

#scheduler.add_job(my_daily_task, IntervalTrigger(seconds=3))
asyncscheduler.add_job(my_async_task, IntervalTrigger(minutes=3), next_run_time=datetime.now())


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
   

#-----------------------------------------#
#--------------- ENDPOINTS ---------------#
#-----------------------------------------#


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
async def get_events_by_sport(sport: str = Query(description="soccer_england_league2")):


    url = f"https://api.the-odds-api.com/v4/sports/{sport}/events/?apiKey={odds_api_key}"

    api_key_check(odds_api_key, url)

    try:
        async with httpx.AsyncClient() as client:

            request = await client.get(url)

        return request.json()
    
    except httpx.RequestError as e:
        raise Exception(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Unexpected error: {str(e)}")
    






@router.get('/odds', status_code=status.HTTP_200_OK)
async def get_upcoming_events_with_odds():
    start_time = time.perf_counter()
    
        
    end_time = time.perf_counter()

    return {

        "events": inserted
    }




@router.post('/place_bet', status_code=status.HTTP_201_CREATED, response_model=Post)
async def place_bet(request: PostRequest):


    post = Post(userId=request.userId,
                stake=request.stake,
                selections=request.selections)

    print("Incoming request data:", post)
    print("Saving post...")
    await post.insert()
    print("Post saved.")
    return post



@router.get('/open_bets', status_code=status.HTTP_200_OK, response_model=List[Post])
async def place_bet():

    posts = await Post.find_all().to_list()
    return posts



@router.get('/test/{bet_id}', status_code=status.HTTP_201_CREATED, response_model=Bet)
async def place_bet(bet_id: str):

    post = await Bet.get(bet_id)
    if not post or post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Bet not Found")
    return post


