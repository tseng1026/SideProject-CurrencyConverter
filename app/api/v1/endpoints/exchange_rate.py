from datetime import date
from typing import Any

from app.constants import StatInterval, StatPeriod
from app.dispatcher.v1.dispatcher import (
    get_currency_dispatcher,
    get_exchange_rate_dispatcher,
)
from app.schemas import HistoricExchangeRate, RealTimeExchangeRate
from fastapi import APIRouter, Path, Query

router = APIRouter()


@router.get(
    "/v1/exchange-rate/real-time/{institution}",
    response_model=RealTimeExchangeRate,
)
def get_realtime_rate(
    institution: str = Path(
        title="The institution of exchange rate to use, visa, mastercard or mid-market.",  # noqa: E501
    ),
    from_code: str = Query(
        alias="from",
        description="The currency to convert from in ISO-4217 format.",
    ),
    to_code: str = Query(
        alias="to",
        description="The currency to convert from in ISO-4217 format.",
    ),
    amount: float = Query(
        default=1.0,
        description="The amount of the currency to convert.",
    ),
    interchange_rate: float = Query(
        default=0.0,
        description="The interchange rate to card issuer during currency conversion.",  # noqa: E501
    ),
) -> Any:
    currency_dispatcher = get_currency_dispatcher()
    from_currency = currency_dispatcher.get_currency(from_code)
    to_currency = currency_dispatcher.get_currency(to_code)

    exchange_rate_dispatcher = get_exchange_rate_dispatcher(institution)
    return exchange_rate_dispatcher.get_realtime_rate(
        transaction_date=date.today().isoformat(),
        from_currency=from_currency,
        to_currency=to_currency,
        amount=amount,
        interchange_rate=interchange_rate,
    )


@router.get("/v1/exchange-rate/historic", response_model=HistoricExchangeRate)
def get_historic_rate(
    from_code: str = Query(
        alias="from",
        description="The currency to convert from in ISO-4217 format.",
    ),
    to_code: str = Query(
        alias="to",
        description="The currency to convert from in ISO-4217 format.",
    ),
    interval: StatInterval = Query(
        description="The interval between two data points, 1d, 1wk, 1mo.",
    ),
    period: StatPeriod = Query(
        description="The period for data to return, 1d, 1wk, 1mo.",
    ),
) -> Any:
    currency_dispatcher = get_currency_dispatcher()
    from_currency = currency_dispatcher.get_currency(from_code)
    to_currency = currency_dispatcher.get_currency(to_code)

    exchange_rate_dispatcher = get_exchange_rate_dispatcher()
    return exchange_rate_dispatcher.get_historic_rate(
        from_currency=from_currency,
        to_currency=to_currency,
        interval=interval,
        period=period,
    )
