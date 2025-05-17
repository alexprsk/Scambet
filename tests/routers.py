from fastapi import APIRouter, Depends, HTTPException, status, Request, Query
from database import SessionLocal
from sqlmodel import Session, select, update, insert, values, desc
from typing import Optional, Annotated
from dotenv import load_dotenv
import httpx, os
import random

from tests.models import TestEvents, TestOddsSnapshot
from utilities.random_odds import random_odds_generator, event_odds

router = APIRouter(
    prefix= "/tests",
     tags=['tests']
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

        event = TestEvents(

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


                        odds_snapshot = TestOddsSnapshot(
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
                        db.flush()

        db.commit()

    return event, odds_snapshot



#-----------------------------------------#
#--------------- ENDPOINTS ---------------#
#-----------------------------------------#


    

@router.get('/test/latest_odds', status_code=status.HTTP_200_OK)
async def get_latest_test_odds(db: db_dependency):


    try:
        response = random_odds_generator(event_odds)
        
        insert_games_in_db(response, db)
        
        return response

    except Exception as e:
        return (f"An error occured while trying to write to db:{e}")

