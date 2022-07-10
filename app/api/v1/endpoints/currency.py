from typing import Any, List

from fastapi import APIRouter

import schemas

router = APIRouter()


@router.get("/currencies", response_model=List[schemas.Currency])
def get_currencies(
    language: str,
) -> Any:
    en_us = [
        schemas.Currency(curr="SGD", country="Singapore"),
        schemas.Currency(curr="USD", country="United States"),
    ]
    zh_tw = [
        schemas.Currency(curr="SGD", country="新加坡"),
        schemas.Currency(curr="USD", country="美國"),
    ]

    currencies = None
    if language == "en_us":
        currencies = en_us
    else:
        currencies = zh_tw
    return currencies
