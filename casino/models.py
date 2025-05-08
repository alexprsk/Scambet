from datetime import datetime, timezone
from uuid import UUID, uuid4
from sqlmodel import Field, SQLModel, Column, DateTime
from enum import Enum

class RoundStatus(str, Enum):

    OPEN = "open"
    CLOSED = "closed"

class RoundResult(str, Enum):

    WON = "won"
    LOST = "loss"




class Round(SQLModel, table=True):


    round_id: UUID = Field(default_factory=uuid4, primary_key=True)
    player_id: int = Field(index=True)
    bet_amount: float
    won_amount: float
    status: RoundStatus = Field(default=None)
    result: RoundResult = Field(default=None,nullable=True)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc), sa_column_kwargs={"onupdate": lambda: datetime.now(timezone.utc)})