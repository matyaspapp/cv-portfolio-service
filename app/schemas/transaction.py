from datetime import datetime, timezone
from pydantic import BaseModel


class Transaction(BaseModel):
    owner_id: str
    asset: str
    amount: float
    historical_price: float
    currency: str
    tags: list[str]
    date: datetime
    type: str
