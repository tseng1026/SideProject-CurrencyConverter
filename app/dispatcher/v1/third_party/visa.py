from datetime import date

import requests

from app.constants import settings
from app.dispatcher.v1.base import ExchangeRateDispatcher
from app.schemas import Currency, RealTimeExchangeRate
from app.utils import XPayToken, urljoin


class Visa(ExchangeRateDispatcher):
    PREFIX = settings.VISA_API_STR

    API_KEY = settings.VISA_API_KEY
    SHARED_SECRET = settings.VISA_SHARED_SECRET

    def get_realtime_rate(
        self,
        transaction_date: str,
        from_currency: Currency,
        to_currency: Currency,
        amount: float,
        interchange_rate: float,
    ) -> RealTimeExchangeRate:
        if transaction_date != date.today().isoformat():
            raise Exception("Historic data unsupported.")

        res = requests.post(
            urljoin(self.PREFIX, "forexrates/v2/foreignexchangerates"),
            params={"apiKey": self.API_KEY},
            json={
                "rateProductCode": "A",
                "sourceAmount": amount,
                "sourceCurrencyCode": from_currency.number,
                "destinationCurrencyCode": to_currency.number,
            },
            auth=XPayToken(self.SHARED_SECRET),
        )

        res_json = res.json()
        exchange_rate = RealTimeExchangeRate(
            date=date.today().isoformat(),
            from_currency=from_currency,
            from_amount=amount,
            to_currency=to_currency,
            to_amount=float(res_json["destinationAmount"]),
            rate=float(res_json["conversionRate"]),
            assessment_rate=1.0,
            interchange_rate=interchange_rate,
        )
        return exchange_rate


visa = Visa()
