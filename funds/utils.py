from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from schemas import CreateUserRequest, Token
from database import SessionLocal
from ..models import Users
from routers.auth import TOKEN_BLACKLIST
from sqlmodel import Session 
from sqlmodel import select
from typing import Annotated

from jose import jwt, JWTError
from passlib.hash import pbkdf2_sha256
from datetime import datetime, timedelta, timezone

SECRET_KEY = '939a99c39bf3dc73316bb5fd52c2195a596485c21cdb7cce1151c1a41dde32df'
ALGORITHM = 'HS256'

oauth2_bearer = OAuth2PasswordBearer(tokenUrl='auth/token')



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