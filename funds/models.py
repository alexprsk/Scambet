from datetime import datetime, timezone
from fastapi import Depends
from sqlmodel import Field,SQLModel
from enum import Enum
from uuid import UUID, uuid4




# ---- Enums ----
class TransactionReason(str, Enum):
    DEPOSIT = "deposit"
    WITHDRAWAL = "withdrawal"
    BET = "bet"
    MANUAL_ADJUSTMENT = "manual_adjustment"

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



# ---- Tables ----
class Funds(SQLModel, table=True):
    movement_id: int = Field(default=None, primary_key=True)
    player_id: int = Field(index=True, foreign_key="users.id")
    previous_balance: float 
    new_balance: float
    change_amount: float
    #transaction_id: UUID = Field(foreign_key="transactions.transaction_id") 
    reason: TransactionReason = Field(default=None)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    
'''class Transactions(SQLModel, table=True):
    transaction_id: UUID = Field(
        default_factory=uuid4,
        primary_key=True,
        index=True
    )
    player_id: int = Field(foreign_key="users.id", index=True)
    type: TransactionType
    amount: float
    status: TransactionStatus  
    reference_id: str | None = None
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))'''