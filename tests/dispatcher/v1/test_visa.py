from http import HTTPStatus

import pytest
import responses
from app.dispatcher.v1.third_party import visa
from app.schemas import Currency, RealTimeExchangeRate
from freezegun import freeze_time
from tests.fixtures.requests import MockedRequest

RESPONSE_DIR = "tests/dispatcher/v1/response"


class TestVisaAPI:
    MOCKED_CURRENCIES = [
        Currency(code=f"currency-code-{i}") for i in range(2)
    ]  # noqa: E501
    MOCKED_TRANSACTION_DATE = "1970-01-01"

    @freeze_time(MOCKED_TRANSACTION_DATE)
    @pytest.mark.usefixtures("mocked_request_responses")
    @pytest.mark.parametrize(
        "mocked_request_list",
        [
            [
                MockedRequest(
                    method=responses.POST,
                    api_url=visa.PREFIX
                    + "/forexrates/v2/foreignexchangerates",  # noqa: E501
                    content_file=f"{RESPONSE_DIR}/visa_get_realtime_rate.json",
                    status=HTTPStatus.OK,
                ),
            ],
        ],
    )
    def test_get_realtime_rate(self):
        response = visa.get_realtime_rate(
            transaction_date=self.MOCKED_TRANSACTION_DATE,
            from_currency=self.MOCKED_CURRENCIES[0],
            to_currency=self.MOCKED_CURRENCIES[1],
            amount=1.0,
            interchange_rate=0.0,
        )

        assert response == RealTimeExchangeRate(
            from_currency=self.MOCKED_CURRENCIES[0],
            to_currency=self.MOCKED_CURRENCIES[1],
            date=self.MOCKED_TRANSACTION_DATE,
            from_amount=1.0,
            to_amount=2.0,
            rate=2.0,
            assessment_rate=1.0,
            interchange_rate=0.0,
        )
