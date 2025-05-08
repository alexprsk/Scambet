from datetime import datetime, timezone
from fastapi import Depends
from sqlmodel import Field,SQLModel
from enum import Enum
from uuid import UUID, uuid4




# ---- Enums ----

class TransactionStatus(str, Enum):
    PENDING = "pending"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"

class TransactionType(str, Enum):
    DEPOSIT = "deposit"
    WITHDRAWAL = "withdrawal"
    BET_PLACEMENT = "bet_placement"
    BET_WIN = "bet_win"
    BET_REFUND = "bet_refund"
    CASINO_BET = "casino_bet"
    CASINO_WIN = "casino_win"



# ---- Tables ----
class Funds(SQLModel, table=True):
    transaction_id: UUID = Field(default_factory=uuid4, primary_key=True)
    player_id: int = Field(index=True, foreign_key="users.id")
    previous_balance: float 
    new_balance: float
    change_amount: float
    reason: TransactionType = Field(default=None)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    
