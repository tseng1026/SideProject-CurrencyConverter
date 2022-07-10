from typing import Optional, List

from pydantic import BaseModel


class ExchangeRate(BaseModel):
    date: Optional[str] = None

    from_curr: str = ""
    from_amount: Optional[float] = None

    to_curr: str = ""
    to_amount: Optional[float] = None

    rate: float = 1.0
    bank_fee: Optional[float] = None
