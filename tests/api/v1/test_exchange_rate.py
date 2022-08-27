from http import HTTPStatus

import pytest

from app.constants import StatInterval, StatPeriod, settings
from app.schemas import Currency, HistoricExchangeRate, RealTimeExchangeRate
from app.utils import urljoin
from tests.fixtures.mock import MockedFunction, MockedFunctionType

CURRENCY_DISPATCHER = "app.dispatcher.v1.third_party.iso"
EXCHANGE_RATE_DISPATCHER = "app.dispatcher.v1.third_party.yahoo"


class TestExchangeRateAPI:
    MOCKED_CURRENCIES = [Currency(code=f"currency-code-{i}") for i in range(2)]
    MOCKED_REALTIME_EXCHANGE_RATE = RealTimeExchangeRate(
        from_currency=MOCKED_CURRENCIES[0],
        to_currency=MOCKED_CURRENCIES[1],
        date="1970-01-01",
        from_amount=1.0,
        to_amount=2.0,
        rate=2.0,
        assessment_rate=0.0,
        interchange_rate=0.0,
    )
    MOCKED_HISTORIC_EXCHANGE_RATE = HistoricExchangeRate(
        from_currency=MOCKED_CURRENCIES[0],
        to_currency=MOCKED_CURRENCIES[1],
        date_list=["1970-01-01"],
        rate_list=[2.0],
        interval="1d",
        period="1d",
    )

    @classmethod
    def setup_class(cls):
        cls.endpoint = urljoin(settings.API_PREFIX, "v1/exchange-rate")

    @pytest.mark.usefixtures("mocked_function_returns")
    @pytest.mark.parametrize(
        "mocked_function_list",
        [
            [
                MockedFunction(
                    mocked_type=MockedFunctionType.SIDE_EFFECT,
                    function_name=f"{CURRENCY_DISPATCHER}.get_currency",
                    return_value=MOCKED_CURRENCIES,
                ),
                MockedFunction(
                    mocked_type=MockedFunctionType.RETURN_VALUE,
                    function_name=f"{EXCHANGE_RATE_DISPATCHER}.get_realtime_rate",  # noqa: E501
                    return_value=MOCKED_REALTIME_EXCHANGE_RATE,
                ),
            ],
        ],
    )
    def test_get_realtime_rate(self, fastapi_client):
        query = {
            "from": "currency-code-0",
            "to": "currency-code-1",
            "amount": 1.0,
            "interchange_rate": 0.0,
        }
        response = fastapi_client.get(
            urljoin(self.endpoint, "real-time", "mid-market"),
            params=query,
        )

        assert response.status_code == HTTPStatus.OK
        assert response.json() == {
            "from_currency": {
                "code": "currency-code-0",
                "name": None,
                "number": None,
                "country": None,
                "flag": None,
                "symbol": None,
            },
            "to_currency": {
                "code": "currency-code-1",
                "name": None,
                "number": None,
                "country": None,
                "flag": None,
                "symbol": None,
            },
            "date": "1970-01-01",
            "from_amount": 1.0,
            "to_amount": 2.0,
            "rate": 2.0,
            "assessment_rate": 0.0,
            "interchange_rate": 0.0,
        }

    @pytest.mark.usefixtures("mocked_function_returns")
    @pytest.mark.parametrize(
        "mocked_function_list",
        [
            [
                MockedFunction(
                    mocked_type=MockedFunctionType.SIDE_EFFECT,
                    function_name=f"{CURRENCY_DISPATCHER}.get_currency",
                    return_value=MOCKED_CURRENCIES,
                ),
                MockedFunction(
                    mocked_type=MockedFunctionType.RETURN_VALUE,
                    function_name=f"{EXCHANGE_RATE_DISPATCHER}.get_historic_rate",  # noqa: E501
                    return_value=MOCKED_HISTORIC_EXCHANGE_RATE,
                ),
            ],
        ],
    )
    def test_get_historic_rate(self, fastapi_client):
        query = {
            "from": "currency-code-0",
            "to": "currency-code-1",
            "interval": "1d",
            "period": "1d",
        }
        response = fastapi_client.get(
            urljoin(self.endpoint, "historic"),
            params=query,
        )

        assert response.status_code == HTTPStatus.OK
        assert response.json() == {
            "from_currency": {
                "code": "currency-code-0",
                "name": None,
                "number": None,
                "country": None,
                "flag": None,
                "symbol": None,
            },
            "to_currency": {
                "code": "currency-code-1",
                "name": None,
                "number": None,
                "country": None,
                "flag": None,
                "symbol": None,
            },
            "date_list": ["1970-01-01"],
            "rate_list": [2.0],
            "interval": StatInterval.ONE_DAY.value,
            "period": StatPeriod.ONE_DAY,
        }
