from typing import List, Optional

from pydantic import BaseModel

from app.constants import StatInterval, StatPeriod
from app.schemas import Currency


class BaseExchangeRate(BaseModel):
    from_currency: Currency
    to_currency: Currency


class RealTimeExchangeRate(BaseExchangeRate):
    date: str
    from_amount: Optional[float]
    to_amount: Optional[float]

    rate: float = 1.0
    assessment_rate: Optional[float]
    interchange_rate: Optional[float]


class HistoricExchangeRate(BaseExchangeRate):
    interval: StatInterval
    period: StatPeriod
    date_list: List[str]
    rate_list: List[float] = [1.0]
