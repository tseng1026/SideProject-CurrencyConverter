from typing import List

import pandas as pd
import requests
from app.constants import StatColumns, StatInterval, StatPeriod, settings
from app.dispatcher.v1.base import ExchangeRateDispatcher
from app.schemas import Currency, HistoricExchangeRate, RealTimeExchangeRate
from app.utils import urljoin
from user_agent import generate_user_agent


class Yahoo(ExchangeRateDispatcher):
    PREFIX = settings.YAHOO_CRAWLER_STR
    USER_AGENT = generate_user_agent()

    def get_realtime_rate(
        self,
        transaction_date: str,
        from_currency: Currency,
        to_currency: Currency,
        amount: float,
        interchange_rate: float = 0,
    ) -> RealTimeExchangeRate:
        return self.get_realtime_rate_from_url(
            transaction_date=transaction_date,
            from_currency=from_currency,
            to_currency=to_currency,
            amount=amount,
            interchange_rate=interchange_rate,
        )

    def get_realtime_rate_from_url(
        self,
        transaction_date: str,
        from_currency: Currency,
        to_currency: Currency,
        amount: float,
        interchange_rate: float = 0,
    ) -> RealTimeExchangeRate:
        res = requests.get(
            urljoin(self.PREFIX, f"{from_currency.code}{to_currency.code}=X"),
            headers={
                "User-Agent": self.USER_AGENT,
            },
            params={
                "interval": "1d",
                "event": "history",
                "includeAdjustedClose": True,
            },
        )
        text_str = self.parse_text(res.text)

        stat = pd.DataFrame(data=text_str[1:], columns=text_str[0])
        rate = stat[StatColumns.ADJ_CLOSE][0]

        exchange_rate = RealTimeExchangeRate(
            date=transaction_date,
            from_currency=from_currency,
            from_amount=amount,
            to_currency=to_currency,
            to_amount=amount * float(rate),
            rate=float(rate),
            assessment_rate=0.0,
            interchange_rate=interchange_rate,
        )
        return exchange_rate

    def get_historic_rate(
        self,
        from_currency: Currency,
        to_currency: Currency,
        interval: StatInterval,
        period: StatPeriod,
    ) -> HistoricExchangeRate:
        return self.get_historic_rate_from_url(
            from_currency=from_currency,
            to_currency=to_currency,
            interval=interval,
            period=period,
        )

    def get_historic_rate_from_url(
        self,
        from_currency: Currency,
        to_currency: Currency,
        interval: str,
        period: StatPeriod,
    ) -> HistoricExchangeRate:
        res = requests.get(
            urljoin(self.PREFIX, f"{from_currency.code}{to_currency.code}=X"),
            headers={
                "User-Agent": self.USER_AGENT,
            },
            params={
                "interval": interval.value,
                "range": StatPeriod.from_str(period).value,
                "event": "history",
                "includeAdjustedClose": True,
            },
        )
        text_str = self.parse_text(res.text)

        stats = pd.DataFrame(data=text_str[1:], columns=text_str[0])
        date_list = stats[StatColumns.DATE].to_list()
        rate_list = stats[StatColumns.ADJ_CLOSE].astype(float).to_list()

        exchange_rate = HistoricExchangeRate(
            date_list=date_list,
            rate_list=rate_list,
            from_currency=from_currency,
            to_currency=to_currency,
            interval=interval,
            period=period,
        )
        return exchange_rate

    def parse_text(self, text: str) -> List[List[str]]:
        text = text.split("\n")
        for idx, line in enumerate(text):
            if not line:
                text[idx] = None
                continue
            text[idx] = line.split(",")

        return [line for line in text if line]


yahoo = Yahoo()
