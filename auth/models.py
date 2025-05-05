from datetime import datetime, timezone
from fastapi import Depends
from sqlmodel import Field,SQLModel
from enum import Enum


class BetStatus(str, Enum):
    PENDING = "pending"
    WON = "won"
    LOST = "lost"
    CANCELED = "canceled"


class Test(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    type: str = Field(unique=True)



class Users(SQLModel, table=True):

    id: int = Field(default=None, primary_key=True)
    username: str = Field(index=True, unique=True)
    email: str = Field(index=True, unique=True)
    hashed_password: str
    first_name: str = Field(index=True)
    last_name: str = Field(index=True)
    phone_number: str | None = Field()
    age: int | None = Field(default=None, index=True)
    balance: float 
    is_active: bool | None = Field(default=True)
    role : str 
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc), sa_column_kwargs={"onupdate": datetime.now(timezone.utc)})




class Bets(SQLModel, table=True):
    
    id: int | None = Field(default=None, primary_key=True)
    user_id: int | None = Field(foreign_key="users.id", index=True)
    market: int | None
    bet_type: str | None
    odds: float | None
    status: BetStatus = Field(default=BetStatus.PENDING)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc), sa_column_kwargs={"onupdate": datetime.now(timezone.utc)})
   