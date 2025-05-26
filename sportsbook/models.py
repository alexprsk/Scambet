from datetime import datetime, timezone
from uuid import UUID, uuid4
from sqlmodel import Field, SQLModel, Column, DateTime
from typing import List, Optional
from pydantic import BaseModel
from beanie import Document
from enum import Enum

class Events(SQLModel, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    event_id: str = Field(index=True)
    sport_key: str 
    sport_title: str 
    commence_time: datetime = Field(sa_column=Column(DateTime(timezone=True)))
    home_team: str
    away_team: str


class OddsSnapshot(SQLModel, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    event_id: str = Field(index=True)

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


