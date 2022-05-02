from pydantic import BaseModel


class Wallet(BaseModel):
    owner_id: str
    address: str
    chain: str
