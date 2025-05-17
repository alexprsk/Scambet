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
from funds.models import Funds, TransactionStatus, TransactionType
from funds.routers import  get_funds
from casino.schemas import WithdrawRequest
from casino.models import Round, RoundStatus

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


@router.get("/history", status_code=status.HTTP_200_OK)
async def casino_history(
    db: db_dependency,
    request: Request):
    """
    Get casino history for the authenticated user
    """
    token = request.cookies.get("access_token")
    print(f"User token is : {token}")
    if not token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized request")
        
    user = get_current_user(token)  # Validate token
    history = db.exec(select(Round).where(Round.player_id == user['user_id']).order_by(Round.created_at.desc())).all()
    
    return history





@router.post("/games/provider_1/flipcoin/play", status_code=status.HTTP_200_OK, response_model=Round)
async def WithdrawRequest(db: db_dependency, request: WithdrawRequest, user_request: Request):

    try:

        
        token = user_request.cookies.get("access_token")
        print(f"User token is : {token}")
        
        if not token:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized request")
            
        user = get_current_user(token)  # Validate token

        
        user_id = user["user_id"]
        current_balance = get_funds(db, user_id)
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")


    try:
        bet_amount = request.bet_amount
        if current_balance < bet_amount:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Insufficient Funds")

        current_balance = get_funds(db, user_id)
        new_balance = current_balance - bet_amount
        change_amount = bet_amount
        reason=TransactionType.CASINO_BET


        new_funds = Funds(
            player_id=user_id,
            previous_balance=current_balance,
            new_balance=new_balance,
            change_amount=bet_amount,
            reason=reason
        )

        db.add(new_funds)
        db.flush()

        if flipcoin():
            

            won_amount = bet_amount * 2
            result="won"
            reason=TransactionType.CASINO_WIN
            change_amount = won_amount
            new_balance = current_balance + won_amount

            round = Round(
                player_id = user_id,
                bet_amount = bet_amount,
                won_amount = won_amount,
                status = RoundStatus.CLOSED,
                result = result
            )

            db.add(round)
            db.flush()

            new_funds = Funds(
                player_id=user_id,
                previous_balance=current_balance,
                new_balance=new_balance,
                change_amount=change_amount,
                reason=reason
            )

            db.add(new_funds)

            
            #After this it would be better to actually send a balance update message instead of updating it here

            db.commit()
            db.refresh(round)
            
            return round.model_dump()
        
        else:
            won_amount = 0


            round = Round(
                player_id = user_id,
                bet_amount = bet_amount,
                won_amount = won_amount,
                status = RoundStatus.CLOSED,
                result = "loss"
            )

            db.add(round)
            db.flush()


            db.commit()
            db.refresh(round)
            return round.model_dump()

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")
            
        