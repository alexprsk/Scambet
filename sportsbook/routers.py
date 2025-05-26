from fastapi import APIRouter, Depends, HTTPException, status, Request, Query, Body
from database import SessionLocal
from sqlmodel import Session, select, update, insert, values, desc
from typing import Optional, Annotated
from dotenv import load_dotenv

import httpx, os
import random

from sportsbook.models import Events, OddsSnapshot
from sportsbook.models_mongo import Bet, PostRequest, Post

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
    

    

@router.get('/odds/prelive_latest', status_code=status.HTTP_200_OK)
async def get_prelive_odds(db:db_dependency):

    try:
        response = db.exec(select(TestOddsSnapshot).order_by(TestOddsSnapshot.created_at.desc())).all()

        if response is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Response was empty")
        return response
    
    except httpx.RequestError as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Unexpected error: {str(e)}")
    

@router.post('/place_bet', status_code=status.HTTP_201_CREATED)
async def place_bet(request: Request):

    try:
        data = await request.json()
        print(data)

        if not data:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail= "response was empty" )
        
    except Exception as e:
        return {f"An error occurred {e}"}
    return data


@router.post('/test/place_bet', status_code=status.HTTP_201_CREATED, response_model=Post)
async def place_bet(post_request: PostRequest):

    post = Post(**post_request.model_dump())
    print("Incoming request data:", post)
    await post.create()
    return post


@router.get('/test/place_bet', status_code=status.HTTP_201_CREATED, response_model=Bet)
async def place_bet():

    posts = await Bet.find_all().to_list()
    return posts

@router.get('/test/{bet_id}', status_code=status.HTTP_201_CREATED, response_model=Bet)
async def place_bet(bet_id: str):

    post = await Bet.get(bet_id)
    if not post or post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Bet not Found")
    return post