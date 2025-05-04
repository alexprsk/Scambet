from datetime import datetime
from uuid import UUID, uuid4
from sqlmodel import Field, SQLModel, Column, DateTime

class Events(SQLModel, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    event_id: str = Field(index=True)
    sport_key: str 
    sport_title: str 
    commence_time: datetime = Field(sa_column=Column(DateTime(timezone=True)))
    home_team: str
    away_team: str

class BookMakers(SQLModel, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True) 
    key: str
    title: str
    last_update: datetime = Field(index=True)
    event_id: UUID = Field(foreign_key="events.id")  

class Markets(SQLModel, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    key: str
    bookmaker_id: UUID = Field(foreign_key="bookmakers.id")  
    last_update: datetime = Field(index=True)


class Outcomes(SQLModel, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    event_id: UUID = Field(foreign_key="events.id")
    market_id: UUID = Field(foreign_key="markets.id")
    name: str
    price: float

