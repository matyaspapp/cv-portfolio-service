from datetime import datetime
from pydantic import BaseModel


class Transaction(BaseModel):
    owner_id: str
    asset: str
    amount: float
    historical_price: float
    currency: str
    tags: list[str]
    date: str
    type: str
