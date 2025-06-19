from fastapi import APIRouter, Depends, HTTPException, status, Request, Query, Body
from fastapi.security import OAuth2PasswordBearer
from fastapi.concurrency import run_in_threadpool


from apscheduler.schedulers.background import BackgroundScheduler  
from apscheduler.triggers.interval import IntervalTrigger 
from database import SessionLocal
from datetime import datetime, timezone
from jose import jwt, JWTError
from sqlmodel import Session
from uuid import uuid4
from typing import Annotated, List
from dotenv import load_dotenv

import httpx, os,asyncio
import random
import time

from scheduler.scheduler import scheduler, asyncscheduler

from sqlmodel import Session, select, update, insert, values


from auth.models import Users
from auth.routers import TOKEN_BLACKLIST
from funds.models import Funds
from funds.routers import get_funds
from sportsbook.models_mongo import Bet, PostRequest, Post, Bets
from sportsbook.utils import insert_events_from_api
from sportsbook.scripts.prelive_endpoints import get_all_events

from sportsbook.schemas import Bet

router = APIRouter(
    prefix= "/sportsbook",
     tags=['sportsbook']
)

load_dotenv("prod.env")

odds_api_key=os.getenv("ODDS_API_KEY")
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")

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
oauth2_bearer = OAuth2PasswordBearer(tokenUrl='auth/token')

def get_user(db: db_dependency, username: str):

    user = db.exec(select(Users).where(Users.username == username)).first()

    if user:
        return user

def get_current_user(db:db_dependency, token : Annotated[str, Depends(oauth2_bearer)]):

    try:

        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        print(payload)
        username = payload.get('sub')
        user_id = payload.get('id')
        

        if token in TOKEN_BLACKLIST:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate user")
        
        if username is None or user_id is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate user")
        user = get_user(db, username)
        return user

    
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate user")
    

user_dependency = Annotated[Users, Depends(get_current_user)]

inserted = []
cached_events = {}
    
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



async def scheduled_get_all_events():
    global cached_events
    cached_events = await get_all_events()
    print(cached_events)
    print(f"Events updated at {datetime.now()}: {list(cached_events.keys())}")



asyncscheduler.add_job(my_async_task, IntervalTrigger(minutes=10), next_run_time=datetime.now())
asyncscheduler.add_job(scheduled_get_all_events, IntervalTrigger(minutes=5), next_run_time=datetime.now())




oauth2_bearer = OAuth2PasswordBearer(tokenUrl='auth/token')


def get_user(db: db_dependency, username: str):

    user = db.exec(select(Users).where(Users.username == username)).first()

    if user:
        return user

def get_current_user(db:db_dependency, token : Annotated[str, Depends(oauth2_bearer)]):

    try:

        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        print(payload)
        username = payload.get('sub')
        user_id = payload.get('id')
        

        if token in TOKEN_BLACKLIST:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate user")
        
        if username is None or user_id is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate user")
        user = get_user(db, username)
        return user

    
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate user")
    



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
    



@router.get('/events/by_sport', status_code=status.HTTP_200_OK)
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

@router.get('/events', status_code=status.HTTP_200_OK)
async def get_all_events_from_api():
    start_time = time.perf_counter()
    
        
    end_time = time.perf_counter()

    return {

        "events": cached_events
    }


@router.post('/place_bet', status_code=status.HTTP_201_CREATED, response_model=Bets)
async def place_bet(request: PostRequest, db: db_dependency, current_user: user_dependency  
):

    user_id = current_user.id

    balance = await run_in_threadpool(get_funds, db, user_id)

    if request.stake > balance:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Insufficient funds")

    new_balance = balance - request.stake

    db.exec(update(Users).where(Users.id == user_id).values(balance=new_balance))

    new_funds = Funds(
        player_id=user_id,
        previous_balance=balance,
        new_balance=new_balance,
        change_amount=-request.stake,  
        transaction_id=uuid4(),
        reason='withdrawal'
    )
    db.add(new_funds)
    db.commit()

    post = Bets(
        userId=str(user_id),
        stake=request.stake,
        status=request.status,
        selections=request.selections
    )

    await post.insert()
    return post




@router.get('/get_all_open_bets', status_code=status.HTTP_200_OK, response_model=List[Bets])
async def open_bets():

    posts = await Bets.find_all().to_list()
    return posts


@router.get('/open_bets', status_code=status.HTTP_200_OK)
async def user_open_bets(db: db_dependency, current_user: user_dependency):
    try:
        if current_user is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid user credentials"
            )

        user_id = str(current_user.id)  # Ensure string format matches how you store it
        bets = await Bets.find(Bets.userId == user_id).to_list()
        return bets

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )



@router.get('/test/{bet_id}', status_code=status.HTTP_201_CREATED, response_model=Bets)
async def place_bet(bet_id: str):

    post = await Bets.get(bet_id)
    if not post or post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Bet not Found")
    return post


