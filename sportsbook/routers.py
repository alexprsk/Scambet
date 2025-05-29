from fastapi import APIRouter, Depends, HTTPException, status, Request, Query, Body
from database import SessionLocal
from sqlmodel import Session, select, update, insert, values, desc
from typing import Optional, Annotated, List
from dotenv import load_dotenv

import httpx, os
import random
import time

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
        db.flush()

        for bookmaker_data in game_data["bookmakers"]:

            if bookmaker_data["key"] in ["pinnacle", "sport888"]:

                for market_data in bookmaker_data["markets"]:

                    for outcomes_data in market_data["outcomes"]:
                        
                        outcome_team = outcomes_data["name"]
                        position = ""

                        if outcome_team == event.home_team:
                            
                            outcome_team = event.home_team
                            position = "Home"

                        elif outcome_team == event.away_team:

                            outcome_team = event.away_team
                            position = "Away"
                        
                        elif outcome_team == "Draw":
                            
                            outcome_team = "Draw"
                            position = "Draw"


                        odds_snapshot = OddsSnapshot(
                        event_id=event.id,
                        bookmaker_key=bookmaker_data["key"],
                        bookmaker_title=bookmaker_data["title"],
                        market_key=market_data["key"],
                        market_last_update=market_data["last_update"],
                        outcome_team=outcome_team,
                        position = position,
                        outcome_price=outcomes_data["price"]
                    )
                        db.add(odds_snapshot)

        db.commit()


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
async def get_odds_by_sport():
    start_time = time.perf_counter()
    
    

    inserted = []

    async with httpx.AsyncClient() as client:

            url = f"https://api.the-odds-api.com/v4/sports/upcoming/odds/?apiKey={odds_api_key}&regions=us,eu&markets=h2h&bookmakers=pinnacle"
            try:
                response = await client.get(url)
                response.raise_for_status()
                data = response.json()

                inserted.append(data)

                await insert_events_from_api(data)
            except httpx.HTTPStatusError as e:
                print(f"HTTP error for {response}: {e.response.text}")
            except httpx.RequestError as e:
                print(f"Request error for {response}: {str(e)}")
            except Exception as e:
                print(f"Unexpected error for {response}: {str(e)}")

    end_time = time.perf_counter()

    return {
        "inserted_count": len(inserted),
        "duration_seconds": round(end_time - start_time, 2),
        "events": inserted
    }

    

@router.get('/odds/prelive_latest', status_code=status.HTTP_200_OK)
async def get_prelive_odds(db:db_dependency):

    try:
        response = db.exec(select(TestOddsSnapshot).order_by(TestOddsSnapshot.created_at.desc())).all()

        if response is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Response was empty")
        return response
    
    except httpx.RequestError as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Unexpected error: {str(e)}")
    


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



@router.get('/place_bet', status_code=status.HTTP_200_OK, response_model=List[Post])
async def place_bet():

    posts = await Post.find_all().to_list()
    return posts



@router.get('/test/{bet_id}', status_code=status.HTTP_201_CREATED, response_model=Bet)
async def place_bet(bet_id: str):

    post = await Bet.get(bet_id)
    if not post or post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Bet not Found")
    return post



@router.post("/events/", response_model=Event, status_code=status.HTTP_201_CREATED)
async def create_event(event: Event = Body(...)):

    # Check if event with this ID already exists
    existing_event = await Event.find_one(Event.event_id == event.event_id)
    if existing_event:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Event with ID {event.event_id} already exists"
        )
    
    # Insert the new event
    await event.create()
    return event
