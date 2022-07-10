from typing import Any

from fastapi import APIRouter, Path, Query

import schemas

router = APIRouter()


@router.get("/{institution}/conversion-rate", response_model=schemas.ExchangeRate)
def get_conversion_rate(
    institution: str = Path(title="The institution of exchange rate to use"),
    from_curr: str = Query(alias="from", description="The currency to convert from in ISO-4217 format."),
    to_curr: str = Query(alias="to", description="The currency to convert from in ISO-4217 format."),
    amount: float = Query(default=1.0, description="The amount of the currency to convert."),
    bank_fee: float = Query(default=0.0, description="The extra bank fee during currency conversion."),
) -> Any:
    # TODO: get from correct dispatcher
    result = schemas.ExchangeRate(
        date="2022-07-01",
        from_curr=from_curr,
        from_amount=amount,
        to_curr=to_curr,
        to_amount=100.0,
        rate=18.0,
        bank_fee=bank_fee,
    )
    return result


@router.get("/{institution}/historic-rate", response_model=schemas.ExchangeRate)
def get_historic_rate(
    institution: str = Path(title="The institution of exchange rate to use"),
    date: str = Query(default="2022-01-01", description="The specific date of currenct conversion."),
    from_curr: str = Query(alias="from", description="The currency to convert from in ISO-4217 format."),
    to_curr: str = Query(alias="to", description="The currency to convert from in ISO-4217 format."),
    amount: float = Query(default=1.0, description="The amount of the currency to convert."),
    bank_fee: float = Query(default=0.0, description="The extra bank fee during currency conversion."),
) -> Any:
    # TODO: get from correct dispatcher
    result = schemas.ExchangeRate(
        date=date,
        from_curr=from_curr,
        from_amount=amount,
        to_curr=to_curr,
        to_amount=100.0,
        rate=3.0,
        bank_fee=bank_fee,
    )
    return result