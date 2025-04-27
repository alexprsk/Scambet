from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, Field
from sqlmodel import Session 
from database import SessionLocal
from sqlmodel import select
from typing import Annotated
from models import Test, Users
from passlib.hash import pbkdf2_sha256

router = APIRouter(
    prefix='/auth',
    tags=['auth'])

class CreateTest(BaseModel):
    type: str

class CreateUserRequest(BaseModel):
    username: str 
    email: str
    first_name: str
    last_name: str
    password: str
    phone_number: str = Field(min_length=7, max_length=15, pattern=r'^\+?\d{7,15}$')
    is_active : bool = Field(default=True)
    role: str = Field(default='user')

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]



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

        raise HTTPException(status_code=401, detail = "Email is already in use")
    
    db.add(create_user_model)
    db.commit()






@router.post("/test", status_code=status.HTTP_201_CREATED)
async def create_test(db: db_dependency, request: CreateTest):
    # Check if test type exists
    existing = db.exec(select(Test).where(Test.type == request.type)).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Test type already exists"
        )
    
    # Create new test
    test = Test(type=request.type)
    db.add(test)
    db.commit()
    db.refresh(test)
    
    return {
        "message": "Test created successfully",
        "data": {
            "id": test.id,
            "type": test.type
        }
    }