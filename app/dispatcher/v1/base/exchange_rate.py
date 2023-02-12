from abc import ABC, abstractclassmethod

from app.constants import StatInterval, StatPeriod
from app.schemas import Currency, HistoricExchangeRate, RealTimeExchangeRate


class ExchangeRateDispatcher(ABC):
    @abstractclassmethod
    def get_realtime_rate(
        self,
        transaction_date: str,
        from_currency: Currency,
        to_currency: Currency,
        amount: float,
        interchange_rate: float,
    ) -> RealTimeExchangeRate:
        raise Exception("Undefined get_realtime_rate method")

    def get_historic_rate(
        self,
        from_currency: Currency,
        to_currency: Currency,
        interval: StatInterval,
        period: StatPeriod,
    ) -> HistoricExchangeRate:
        pass
