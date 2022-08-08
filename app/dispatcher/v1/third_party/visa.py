from datetime import date

import requests
from app.constants import settings
from app.dispatcher.v1.base import ExchangeRateDispatcher
from app.schemas import Currency, RealTimeExchangeRate


class Visa(ExchangeRateDispatcher):
    PREFIX = settings.VISA_API_STR

    SSL_CERT = settings.VISA_SSL_CERT
    SSL_KEY = settings.VISA_SSL_KEY
    AUTH_USERNAME = settings.VISA_AUTH_USERNAME
    AUTH_PASSWORD = settings.VISA_AUTH_PASSWORD

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
            self.PREFIX + "/forexrates/v2/foreignexchangerates",
            json={
                "rateProductCode": "A",
                "sourceAmount": amount,
                "sourceCurrencyCode": from_currency.number,
                "destinationCurrencyCode": to_currency.number,
            },
            cert=(self.SSL_CERT, self.SSL_KEY),
            auth=(self.AUTH_USERNAME, self.AUTH_PASSWORD),
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
