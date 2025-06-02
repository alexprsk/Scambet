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


from database import SessionLocal
from auth.models import Users
from funds.models import Funds
from auth.schemas import CreateUserRequest, Token
from funds.schemas import DepositRequest, WithdrawRequest


router = APIRouter(
    prefix='/auth',
    tags=['auth'])



#################### REDIS BLACKLIST ####################

TOKEN_BLACKLIST = []  # In-memory storage (not for production!)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()



db_dependency = Annotated[Session, Depends(get_db)]


SECRET_KEY = '939a99c39bf3dc73316bb5fd52c2195a596485c21cdb7cce1151c1a41dde32df'
ALGORITHM = 'HS256'

oauth2_bearer = OAuth2PasswordBearer(tokenUrl='auth/token')



#################### FUNCTIONS ####################


def get_current_user(token = Annotated[str, Depends(oauth2_bearer)]):

    try:

        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        print(payload)
        username = payload.get('sub')
        user_id = payload.get('id')
        user_role = payload.get('role')

        if token in TOKEN_BLACKLIST:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate user")
        
        if username is None or user_id is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate user")
    
        return {'username':username, 'user_id': user_id, 'user_role': user_role}

    
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate user")


user_dependency = Annotated[str, Depends(get_current_user)]



def authenticate_user(username:str, password: str, db):

    user = db.query(Users).filter(Users.username == username).first()

    if not user:

        return False
    
    if not pbkdf2_sha256.verify(password, user.hashed_password):

        return False
    
    return user



def create_access_token(username:str, user_id:int, role:str, expires_delta: timedelta):

    payload = {'sub': username, 'id': user_id, 'role': role}

    expires = datetime.now(timezone.utc) + expires_delta

    payload.update({ 'exp': expires })

    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)




#################### RETURN ALL USERS ####################


@router.get("/", status_code= status.HTTP_200_OK)
async def get_all_users(db: db_dependency):
    users = db.exec(select(Users)).all()

    return users


#################### SIGN UP ####################


@router.post('/sign-up', status_code=status.HTTP_201_CREATED)
async def sign_up(db: db_dependency, request: CreateUserRequest):

    create_user_model = Users(
        username = request.username,
        email = request.email,
        first_name = request.first_name,
        last_name = request.last_name,
        hashed_password = pbkdf2_sha256.hash(request.password),
        phone_number = request.phone_number,
        balance = 0,
        role = 'user',
        is_active = True
    )
    
    if db.exec(select(Users).where(Users.username == request.username)).first():

        raise HTTPException(status_code=409, detail = "Username is already in use")
    
    if db.exec(select(Users).where(Users.email == request.email)).first():

        raise HTTPException(status_code=409, detail = "Email is already in use")
    
    if db.exec(select(Users).where(Users.phone_number == request.phone_number)).first():
        
        raise HTTPException(status_code=409, detail="Phone number is already in use")

    db.add(create_user_model)
    db.commit()



#################### TOKEN ####################


@router.post("/token", response_model = Token)
async def login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db:db_dependency):
    user = authenticate_user(form_data.username, form_data.password, db)

    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Could not Validate user.')

 
    token = create_access_token(user.username, user.id, user.role, timedelta(hours=4))
    print(token)
    return {'access_token': token, 'user_id': user.id, 'token_type': 'bearer', "expires_in": 14400}



#################### LOGOUT ####################


@router.post("/logout", status_code=status.HTTP_200_OK)
async def logout(request: Request):

    token = request.cookies.get("access_token")

    TOKEN_BLACKLIST.append(token)


    




