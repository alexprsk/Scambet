
from pydantic import BaseModel, Field

#################### PYDANTIC ####################

#################### AUTHENTICATION ####################

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


class Token(BaseModel):
    access_token: str
    token_type: str
    user_id: int