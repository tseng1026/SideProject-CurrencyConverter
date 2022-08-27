from http import HTTPStatus

import pytest
import responses
from freezegun import freeze_time

from app.constants import StatInterval, StatPeriod
from app.dispatcher.v1.third_party import yahoo
from app.schemas import Currency, HistoricExchangeRate, RealTimeExchangeRate
from app.utils import filejoin, urljoin
from tests.fixtures.requests import MockedRequest

YAHOO_API = "app.dispatcher.v1.third_party.yahoo"
RESPONSE_DIR = "tests/dispatcher/v1/response"


class TestMastercardAPI:
    MOCKED_CURRENCIES = [
        Currency(code=f"currency-code-{i}") for i in range(2)
    ]  # noqa: E501
    MOCKED_TRANSACTION_DATE = "1970-01-01"

    @freeze_time("1970-01-01")
    @pytest.mark.usefixtures("mocked_request_responses")
    @pytest.mark.parametrize(
        "mocked_request_list",
        [
            [
                MockedRequest(
                    method=responses.GET,
                    api_url=urljoin(
                        yahoo.PREFIX,
                        f"{MOCKED_CURRENCIES[0].code}{MOCKED_CURRENCIES[1].code}=X",  # noqa: 501
                    ),
                    content_file=filejoin(
                        RESPONSE_DIR,
                        "yahoo_get_realtime_rate.txt",
                    ),
                    status=HTTPStatus.OK,
                ),
            ],
        ],
    )
    def test_get_realtime_rate(self):
        response = yahoo.get_realtime_rate(
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
            assessment_rate=0.0,
            interchange_rate=0.0,
        )

    @freeze_time("1970-01-07")
    @pytest.mark.usefixtures("mocked_request_responses")
    @pytest.mark.parametrize(
        "mocked_request_list",
        [
            [
                MockedRequest(
                    method=responses.GET,
                    api_url=urljoin(
                        yahoo.PREFIX,
                        f"{MOCKED_CURRENCIES[0].code}{MOCKED_CURRENCIES[1].code}=X",  # noqa: 501
                    ),
                    content_file=filejoin(
                        RESPONSE_DIR,
                        "yahoo_get_historic_rate.txt",
                    ),
                    status=HTTPStatus.OK,
                ),
            ],
        ],
    )
    def test_get_historic_rate(self):
        response = yahoo.get_historic_rate(
            from_currency=self.MOCKED_CURRENCIES[0],
            to_currency=self.MOCKED_CURRENCIES[1],
            interval=StatInterval.ONE_DAY,
            period=StatPeriod.ONE_WEEK,
        )

        assert response == HistoricExchangeRate(
            from_currency=self.MOCKED_CURRENCIES[0],
            to_currency=self.MOCKED_CURRENCIES[1],
            date_list=[f"1970-01-0{i}" for i in range(1, 8)],
            rate_list=[i for i in range(2, 9)],
            interval=StatInterval.ONE_DAY,
            period=StatPeriod.ONE_WEEK,
        )
