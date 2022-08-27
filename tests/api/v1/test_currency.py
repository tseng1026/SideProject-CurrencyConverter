from http import HTTPStatus

import pytest
from app.constants import settings
from app.schemas import Currency
from tests.fixtures.mock import MockedFunction, MockedFunctionType

CURRENCY_DISPATCHER = "app.dispatcher.v1.third_party.iso"


class TestCurrencyAPI:
    MOCKED_CURRENCIES = [
        Currency(code=f"currency-code-{i}") for i in range(10)
    ]  # noqa: E501

    @classmethod
    def setup_class(cls):
        cls.endpoint = f"{settings.API_PREFIX}/v1/currency"

    @pytest.mark.usefixtures("mocked_function_returns")
    @pytest.mark.parametrize(
        "mocked_function_list",
        [
            [
                MockedFunction(
                    mocked_type=MockedFunctionType.RETURN_VALUE,
                    function_name=f"{CURRENCY_DISPATCHER}.get_currencies",
                    return_value=MOCKED_CURRENCIES,
                ),
            ],
        ],
    )
    def test_get_currencies(self, fastapi_client):
        response = fastapi_client.get(f"{self.endpoint}/list")

        assert response.status_code == HTTPStatus.OK
        assert response.json() == [
            {
                "code": f"currency-code-{i}",
                "name": None,
                "number": None,
                "country": None,
                "flag": None,
                "symbol": None,
            }
            for i in range(10)
        ]
