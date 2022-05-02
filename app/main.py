from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1.transaction import transaction_router
from app.api.v1.user import user_router
from app.api.v1.wallet import wallet_router

portfolio_service = FastAPI()
portfolio_service.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],

)

portfolio_service.include_router(transaction_router)
portfolio_service.include_router(user_router)
portfolio_service.include_router(wallet_router)
