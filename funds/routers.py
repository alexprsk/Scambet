import os
from datetime import datetime, timedelta, timezone
from typing import Annotated
from uuid import UUID, uuid4


from dotenv import load_dotenv
from fastapi import APIRouter, Depends, HTTPException, Request, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import jwt, JWTError
from passlib.hash import pbkdf2_sha256
from sqlmodel import Session, select, update, insert, values


from auth.models import Users
from database import SessionLocal
from funds.models import Funds
from funds.schemas import DepositRequest, WithdrawRequest



router = APIRouter(
    prefix='/funds',
    tags=['funds'])


#################### REDIS BLACKLIST ####################

TOKEN_BLACKLIST = []  # In-memory storage (not for production!)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


SECRET_KEY = '939a99c39bf3dc73316bb5fd52c2195a596485c21cdb7cce1151c1a41dde32df'
ALGORITHM = 'HS256'

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
    

user_dependency = Annotated[dict, Depends(get_current_user)]



def get_funds(db: db_dependency, user_id: int) -> float:

    user = db.exec(select(Users).where(Users.id == user_id)).first()

    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    return user.balance



@router.get('/', status_code=status.HTTP_200_OK)
async def get_user_funds(db: db_dependency,  request: Request):
    
    token = request.cookies.get("access_token")

    
    if not token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate user")
    
    user = get_current_user(token)

    
    
    user_data = db.exec(select(Users).where(Users.id == user['user_id'])).first()
    
    if not user_data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    return {'user_balance': user_data.balance}




@router.post('/deposit', status_code=status.HTTP_200_OK)
async def deposit(db:db_dependency, deposit_request: DepositRequest, current_user: user_dependency):



    try:

        

        if current_user is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid user credentials"
            )
        
        if deposit_request.amount <= 0:
                    raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Deposit amount must be positive"
            )
            
        user_id = current_user.id
        current_balance = get_funds(db, user_id)
        print(current_balance)


        new_balance = current_balance + deposit_request.amount
        change_amount = deposit_request.amount


        # Start Transaction on Funds Table


        #Update User Balace
        db.exec(update(Users).where(Users.id == user_id).values(balance = new_balance))

        #Create New Funds Record

        new_funds = Funds(
            player_id=user_id,
            previous_balance=current_balance,
            new_balance=new_balance,
            change_amount=change_amount,
            transaction_id=uuid4(),
            reason='deposit'
        )
        db.add(new_funds)
        db.commit()
        
        return {
            "message": "Deposit successful",
            "new_balance": new_balance,
            "transaction_id": str(new_funds.transaction_id)
        }




    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Deposit failed: {str(e)}"
        )        



@router.post('/withdraw', status_code=status.HTTP_200_OK)
async def withdraw(db:db_dependency, withdrawal: WithdrawRequest, current_user: user_dependency):



    try:
        if current_user is None:
                    raise HTTPException(
                        status_code=status.HTTP_401_UNAUTHORIZED,
                        detail="Invalid user credentials"
                    )
        
        
        user_id = current_user.id
        current_balance = get_funds(db, user_id)


        if withdrawal.amount <= 0:
            raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="Deposit amount must be positive"
    )
    
    


        if withdrawal.amount > current_balance:
             raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Insufficient balance to perform this operation")



        new_balance = current_balance - withdrawal.amount
        change_amount = (-withdrawal.amount)


        # Start Transaction on Funds Table


        #Update User Balace
        db.exec(update(Users).where(Users.id == user_id).values(balance = new_balance))

        #Create New Funds Record

        new_funds = Funds(
            player_id=user_id,
            previous_balance=current_balance,
            new_balance=new_balance,
            change_amount=change_amount,
            transaction_id=uuid4(),
            reason='withdrawal'
        )
        db.add(new_funds)
        db.commit()
        
        return {
            "message": "Withdrawal successful",
            "new_balance": new_balance,
            "transaction_id": str(new_funds.transaction_id)
        }




    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )








########### TEST ENDPOINTS ##########

@router.put('/edit_amount/{user_id}', status_code=status.HTTP_200_OK)
async def edit_amount(db:db_dependency, user_id : int, new_balance: float, current_user: user_dependency):
    
    
    update_balance = db.exec(update(Users).where(Users.id == current_user.id).values(balance = new_balance))

    if update_balance.rowcount == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    
    db.commit()




@router.get('/history/{user_id}', status_code=status.HTTP_200_OK)
async def get_user_all_funds(db: db_dependency, user_id: int):

    return db.exec(select(Funds).where(Users.id == user_id)).all()