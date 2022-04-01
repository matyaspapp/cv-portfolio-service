from fastapi import FastAPI

from app.api.v1.transaction import transaction_router
from app.api.v1.user import user_router

portfolio_service = FastAPI()

portfolio_service.include_router(transaction_router)
portfolio_service.include_router(user_router)
