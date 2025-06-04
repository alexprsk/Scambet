from datetime import datetime, timezone
from uuid import UUID, uuid4
from typing import List, Optional
from pydantic import BaseModel, Field
from beanie import Document, PydanticObjectId
from enum import Enum


class BetStatus(str, Enum):
    settled="SETTLED"
    pending="PENDING"
    voided="VOIDED"

class PostRequest(Document):
    userId: str
    stake: float
    selections: Optional[List[dict]]
    status: BetStatus
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc)
    )


class Post(Document):
    id: Optional[PydanticObjectId] = Field(alias="_id", default=None)
    userId: str
    stake: float
    selections: List[dict]
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc)
    )

    class Settings:
        collection_name='posts'

class Bets(Document):
    id: Optional[PydanticObjectId] = Field(alias="_id", default=None)
    userId: str
    stake: float
    status: BetStatus
    selections: List[dict]
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc)
    )

    class Settings:
        collection_name='bets'

class Bet(Document):

    user_id: str
    event_id: Optional[str]
    selections: List
    status: BetStatus
    created_at: datetime = datetime.now(timezone.utc)

    class Settings:
        collection_name="bets"






class Bookmaker(BaseModel):
    # You can expand this with more detailed bookmaker fields later
    key: str
    title: str
    last_update: Optional[datetime] = None
    markets: List[dict] = []

class Event(Document):
    event_id: str
    sport_key: str
    sport_title: str
    commence_time: datetime
    home_team: str
    away_team: str
    bookmakers: List[Bookmaker] = []
    
    class Settings:
        collection_name = "events"  # This will be the collection name in MongoDB

    class Config:
        schema_extra = {
            "example": {
                "event_id": "test123",
                "sport_key": "basketball_nba",
                "sport_title": "NBA Basketball",
                "commence_time": "2023-05-30T23:00:00Z",
                "home_team": "Lakers",
                "away_team": "Warriors",
                "bookmakers": []
            }
        }
        