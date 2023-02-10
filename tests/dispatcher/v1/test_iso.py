import pytest
from app.dispatcher.v1.third_party import iso
from app.schemas import Currency
from app.utils import filejoin
from tests.fixtures.mock import MockedFunction, MockedFunctionType

ISO_API = "app.dispatcher.v1.third_party.iso"
RESPONSE_DIR = "tests/dispatcher/v1/response"


class TestIsoApi:
    MOCKED_CURRENCY_CODE = "currency-code-0"

    @pytest.mark.usefixtures("mocked_function_returns")
    @pytest.mark.parametrize(
        "mocked_function_list",
        [
            [
                MockedFunction(
                    mocked_type=MockedFunctionType.RETURN_VALUE,
                    function_name=f"{ISO_API}.get_currencies_from_static_files",  # noqa: E501
                    return_value=False,
                ),
                MockedFunction(
                    mocked_type=MockedFunctionType.RETURN_VALUE,
                    function_name="urllib.request.urlopen",
                    return_value=open(
                        filejoin(RESPONSE_DIR, "get_currencies.xml"),
                        "r",
                    ),
                ),
            ],
        ],
    )
    def test_get_currencies_from_url(self):
        response = iso.get_currencies()

        assert response == [
            Currency(
                code=f"currency-code-{i}".upper(),
                name=f"currency name {i}".capitalize(),
                number=i,
                country=f"country name {i}".capitalize(),
                flag=None,
                symbol=None,
            )
            for i in range(2)
        ]

    @pytest.mark.usefixtures("mocked_function_returns")
    @pytest.mark.parametrize(
        "mocked_function_list",
        [
            [
                MockedFunction(
                    mocked_type=MockedFunctionType.RETURN_VALUE,
                    function_name="os.path.exists",
                    return_value=True,
                ),
                # TODO(scarlett): Improve readability
                MockedFunction(
                    mocked_type=MockedFunctionType.RETURN_VALUE,
                    function_name="builtins.open",
                    return_value=open(
                        filejoin(RESPONSE_DIR, "get_currencies.xml"),
                        "r",
                    ),
                ),
            ],
        ],
    )
    def test_get_currencies_from_static_files(self):
        response = iso.get_currencies()

        assert response == [
            Currency(
                code=f"currency-code-{i}".upper(),
                name=f"currency name {i}".capitalize(),
                number=i,
                country=f"country name {i}".capitalize(),
                flag=None,
                symbol=None,
            )
            for i in range(2)
        ]

    @pytest.mark.usefixtures("mocked_function_returns")
    @pytest.mark.parametrize(
        "mocked_function_list",
        [
            [
                MockedFunction(
                    mocked_type=MockedFunctionType.RETURN_VALUE,
                    function_name=f"{ISO_API}.get_currency_from_static_files",  # noqa: E501
                    return_value=False,
                ),
                MockedFunction(
                    mocked_type=MockedFunctionType.RETURN_VALUE,
                    function_name="urllib.request.urlopen",
                    return_value=open(
                        filejoin(RESPONSE_DIR, "get_currencies.xml"),
                        "r",
                    ),
                ),
            ],
        ],
    )
    def test_get_currency_from_url(self):
        response = iso.get_currency(self.MOCKED_CURRENCY_CODE)

        assert response == Currency(
            code="currency-code-0".upper(),
            name="currency name 0".capitalize(),
            number=0,
            country="country name 0".capitalize(),
            flag=None,
            symbol=None,
        )

    @pytest.mark.usefixtures("mocked_function_returns")
    @pytest.mark.parametrize(
        "mocked_function_list",
        [
            [
                MockedFunction(
                    mocked_type=MockedFunctionType.RETURN_VALUE,
                    function_name="os.path.exists",
                    return_value=True,
                ),
                # TODO(scarlett): Improve readability
                MockedFunction(
                    mocked_type=MockedFunctionType.RETURN_VALUE,
                    function_name="builtins.open",
                    return_value=open(
                        filejoin(RESPONSE_DIR, "get_currencies.xml"),
                        "r",
                    ),
                ),
            ],
        ],
    )
    def test_get_currency_from_static_files(self):
        response = iso.get_currency(self.MOCKED_CURRENCY_CODE)

        assert response == Currency(
            code="currency-code-0".upper(),
            name="currency name 0".capitalize(),
            number=0,
            country="country name 0".capitalize(),
            flag=None,
            symbol=None,
        )
