from fastapi import APIRouter, Depends, HTTPException, status, Request, Query
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordBearer
from database import SessionLocal
from sqlmodel import Session, select, update, insert, values, desc
from typing import Optional, Annotated
from casinogames.flipcoin import flipcoin

from uuid import UUID, uuid4
import httpx, os
import random

from auth.routers import oauth2_bearer, get_current_user
from auth.models import Users
from funds.routers import  get_funds
from casino.schemas import WithdrawRequest
from casino.models import Round

router = APIRouter(
    prefix='/casino',
    tags=['casino'])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]

oauth2_bearer = OAuth2PasswordBearer(tokenUrl='auth/token')





@router.post("/games/provider_1/flipcoin/play", status_code=status.HTTP_200_OK)
async def WithdrawRequest(db: db_dependency, token: Annotated[str, Depends(oauth2_bearer)], bet_amount: float):

    try:

        user = get_current_user(token)

        
        if user["user_id"] is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized request")

        
        user_id = user["user_id"]
        current_balance = get_funds(db, user_id)
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")


    try:
        if current_balance < bet_amount:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Insufficient Funds")
        

        if flipcoin():
            
            won_amount = bet_amount * 2
            new_balance = current_balance + won_amount

            round = Round(
                player_id = user_id,
                bet_amount = bet_amount,
                won_amount = won_amount,
                status = "closed",
                result = "won"
            )

            db.add(round)
            
            #After this it would be better to actually send a balance update message instead of updating it here
            db.exec(update(Users).where(Users.id == user_id).values(balance = new_balance))
            db.commit()

            return round
        else:
            new_balance = current_balance - bet_amount
            won_amount = 0

            round = Round(
                player_id = user_id,
                bet_amount = bet_amount,
                won_amount = won_amount,
                status = "closed",
                result = "loss"
            )

            db.add(round)
            db.flush()
            
            db.exec(update(Users).where(Users.id == user_id).values(balance=new_balance))
            db.commit()
            
            return round

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")
            
        
        




    

    









