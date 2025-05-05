from datetime import datetime, timezone
from uuid import UUID, uuid4
from sqlmodel import Field, SQLModel, Column, DateTime

class TestEvents(SQLModel, table=True):
    __tablename__ = "testevents"

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    event_id: str = Field(index=True)
    sport_key: str 
    sport_title: str 
    commence_time: datetime = Field(sa_column=Column(DateTime(timezone=True)))
    home_team: str
    away_team: str



class TestOddsSnapshot(SQLModel, table=True):
    __tablename__ = "testoddssnapshot"

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    event_id: UUID = Field(foreign_key="events.id")

    # Bookmaker info
    bookmaker_key: str
    bookmaker_title: str

    # Market info
    market_key: str
    market_last_update: datetime = Field(index=True)

    # Outcome info
    outcome_team: str
    position: str
    outcome_price: float
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))