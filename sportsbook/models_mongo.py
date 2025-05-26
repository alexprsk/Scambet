from datetime import datetime, timezone
from uuid import UUID, uuid4
from typing import List, Optional
from pydantic import BaseModel
from beanie import Document
from enum import Enum


class BetStatus(str, Enum):
    settled="SETTLED"
    pending="PENDING"
    voided="VOIDED"

class PostRequest(Document):
    title: Optional[str]
    content: Optional[str]
    tags: Optional[List[str]]


class Post(Document):
    title: Optional[str]
    content: Optional[str]
    tags: Optional[List[str]]
    created_at: datetime = datetime.now(timezone.utc)

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
