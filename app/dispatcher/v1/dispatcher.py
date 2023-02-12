from app.constants import Institution
from app.dispatcher.v1.base import CurrencyDispatcher, ExchangeRateDispatcher
from app.dispatcher.v1.third_party import iso, mastercard, visa, yahoo


def get_currency_dispatcher() -> CurrencyDispatcher:
    return iso


def get_exchange_rate_dispatcher(
    institution: str = Institution.MIDMARKET.value,
) -> ExchangeRateDispatcher:
    if institution == Institution.MIDMARKET.value:
        return yahoo
    elif institution == Institution.VISA.value:
        return visa
    elif institution == Institution.MASTERCARD.value:
        return mastercard
    else:
        raise Exception("Unsupported currency exchange institution")
