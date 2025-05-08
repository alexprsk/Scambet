from datetime import datetime, timezone
from pydantic import BaseModel, Field
from uuid import UUID
from enum import Enum




class RoundStatus(str, Enum):

    OPEN = "open"
    CLOSED = "closed"

class RoundResult(str, Enum):

    WON = "won"
    LOST = "lost"

class Round(BaseModel):

    round_id: UUID
    player_id: int 
    status: RoundStatus 
    result: RoundResult | None
    bet_amount: float
    won_amount: float 
    created_at: datetime 
    updated_at: datetime 

class WithdrawRequest(BaseModel):

    bet_amount: float = Field(min=0.1, max=20)

