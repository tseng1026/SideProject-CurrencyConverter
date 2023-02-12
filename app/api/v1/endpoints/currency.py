from typing import Any, List

from fastapi import APIRouter

from app.dispatcher.v1.dispatcher import get_currency_dispatcher
from app.schemas import Currency

router = APIRouter()


@router.get("/v1/currency/list", response_model=List[Currency])
def get_currencies() -> Any:
    currency_dispatcher = get_currency_dispatcher()
    return currency_dispatcher.get_currencies()
