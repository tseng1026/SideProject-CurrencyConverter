from http import HTTPStatus

import pytest
import responses
from freezegun import freeze_time

from app.dispatcher.v1.third_party import visa
from app.schemas import Currency, RealTimeExchangeRate
from app.utils import filejoin, urljoin
from tests.fixtures.requests import MockedRequest

RESPONSE_DIR = "tests/dispatcher/v1/response"


class TestVisaAPI:
    MOCK_API_KEY = "mock-api-key"
    MOCK_SHARED_SECRET = "mock-shared-secret"
    visa.API_KEY = MOCK_API_KEY
    visa.SHARED_SECRET = MOCK_SHARED_SECRET

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
                    api_url=urljoin(
                        visa.PREFIX,
                        f"forexrates/v2/foreignexchangerates?apiKey={MOCK_API_KEY}",  # noqa: 501
                    ),
                    content_file=filejoin(
                        RESPONSE_DIR,
                        "visa_get_realtime_rate.json",
                    ),
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
