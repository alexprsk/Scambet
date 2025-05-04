from auth.models import Users
from passlib.hash import pbkdf2_sha256
from datetime import datetime, timedelta, timezone
from jose import jwt



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