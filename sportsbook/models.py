from datetime import datetime, timezone
from fastapi import Depends
from enum import Enum
from uuid import UUID, uuid4

from sqlmodel import Field, SQLModel





class Events(SQLModel, table=True):

    event_id: str = Field(primary_key=True, unique=True, index=True)
    sport_key: str 
    sport_title: str 
    commence_time: datetime = Field(index=True)
    home_team: str
    away_team: str

class BookMakers(SQLModel, table=True):

    id: int = Field(default=None, primary_key=True, index=True)
    key: str
    title: str
    last_update: datetime = Field(index=True)
    event_id: str = Field(foreign_key="events.event_id")



class Markets(SQLModel, table=True):

    id: UUID = Field(default=uuid4,index=True, primary_key=True)
    key: str
    bookmaker_id: int = Field(foreign_key="bookmakers.id")
    last_update: datetime = Field(index=True)

class Outcomes(SQLModel, table=True):

    id: UUID = Field(default=uuid4, primary_key=True)
    event_id : str = Field(foreign_key="events.event_id")
    name: str
    price: float






