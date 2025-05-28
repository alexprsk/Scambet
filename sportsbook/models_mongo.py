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

class Bet(Document):

    user_id: str
    event_id: Optional[str]
    selections: List
    status: BetStatus
    created_at: datetime = datetime.now(timezone.utc)

    class Settings:
        collection="Bets"
