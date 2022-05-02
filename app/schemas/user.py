from pydantic import BaseModel


class User(BaseModel):
    username: str
    hashed_password: str


class UserResponse(BaseModel):
    id: str
    username: str
