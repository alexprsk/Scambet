from pydantic import BaseModel, Field
from uuid import UUID, uuid4
from datetime import datetime, timezone


class DepositRequest(BaseModel):

    amount: float


class WithdrawRequest(BaseModel):
    
    amount: float

