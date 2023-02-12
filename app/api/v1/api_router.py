from fastapi import APIRouter

from app.api.v1.endpoints import currency, exchange_rate

api_router = APIRouter()
api_router.include_router(currency.router, tags=["currency"])
api_router.include_router(exchange_rate.router, tags=["exchange-rate"])
