from pydantic import BaseModel, Field



class DepositRequest(BaseModel):

    amount: float


class WithdrawRequest(BaseModel):
    
    amount: float

