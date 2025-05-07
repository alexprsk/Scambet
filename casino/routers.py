from fastapi import APIRouter, Depends, HTTPException, status, Request, Query
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordBearer
from database import SessionLocal
from sqlmodel import Session, select, update, insert, values, desc
from typing import Optional, Annotated
from casinogames.flipcoin import flipcoin

import httpx, os
import random

from auth.routers import oauth2_bearer, get_current_user
from funds.routers import  get_funds
from casino.schemas import WithdrawRequest

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


@router.post("/games/provider_1/flipcoin/withdraw_request", status_code=status.HTTP_200_OK)
async def WithdrawRequest(db: db_dependency, token: Annotated[str, Depends(oauth2_bearer)], bet_amount: float):

    try:

        if token is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized request")

        user = get_current_user(token)


        
        if user["user_id"] is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized request")

        
        user_id = user["user_id"]
        current_balance = get_funds(db, user_id)
    
    except Exception as e:
        return (f"An error occurred: {e}")


    try:
        if current_balance < bet_amount:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Insufficient Funds")
        

        if flipcoin():
            return JSONResponse(content={"result": f"You won {bet_amount *2}"}, status_code=200)
        else:
            return JSONResponse(content={"result": "You lost"}, status_code=200)

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")
            
        
        




    

    









