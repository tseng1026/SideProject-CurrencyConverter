from datetime import date

import requests
from app.constants import settings
from app.dispatcher.v1.base import ExchangeRateDispatcher
from app.schemas import Currency, RealTimeExchangeRate
from oauth1.authenticationutils import load_signing_key
from oauth1.oauth_ext import OAuth1RSA


class MasterCard(ExchangeRateDispatcher):
    PREFIX = settings.MASTERCARD_API_STR

    OPENSSL_KEY = settings.MASTERCARD_OPENSSL_KEY
    OPENSSL_PASSWORD = settings.MASTERCARD_OPENSSL_PASSWORD
    SIGNING_KEY = load_signing_key(OPENSSL_KEY, OPENSSL_PASSWORD)
    CONSUMER_KEY = settings.MASTERCARD_CONSUMER_KEY

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

        res = requests.get(
            self.PREFIX + "/settlement/currencyrate/conversion-rate",
            auth=OAuth1RSA(self.CONSUMER_KEY, self.SIGNING_KEY),
            params={
                "fxDate": transaction_date,
                "transAmt": amount,
                "transCurr": from_currency.code,
                "crdhldBillCurr": to_currency.code,
                "bankFee": interchange_rate,
            },
        )

        res_json = res.json()
        exchange_rate = RealTimeExchangeRate(
            date=transaction_date,
            from_currency=from_currency,
            from_amount=amount,
            to_currency=to_currency,
            to_amount=float(res_json["data"]["crdhldBillAmt"]),
            rate=float(res_json["data"]["conversionRate"]),
            assessment_rate=1.0,
            interchange_rate=interchange_rate,
        )
        return exchange_rate


mastercard = MasterCard()
