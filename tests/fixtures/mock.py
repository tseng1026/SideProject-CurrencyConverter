import json
from enum import Enum
from typing import Any

import pytest
from pydantic import BaseModel


class MockedFunctionType(int, Enum):
    RETURN_VALUE = 0
    STATIC_FILE = 1
    SIDE_EFFECT = 2
    EXCEPTION = 3


class MockedFunction(BaseModel):
    mocked_type: MockedFunctionType = MockedFunctionType.RETURN_VALUE
    function_name: str
    return_value: Any = None  # or static file path


@pytest.fixture
def mocked_function_returns(mocker, mocked_function_list):
    for mocked_function in mocked_function_list:
        mocked_type = mocked_function.mocked_type

        if mocked_type == MockedFunctionType.RETURN_VALUE:
            mocker.patch(
                target=mocked_function.function_name,
                return_value=mocked_function.return_value,
                create=True,
            )
        elif mocked_type == MockedFunctionType.STATIC_FILE:
            with open(mocked_function.return_value) as f:
                json_data = json.load(f)
            mocker.patch(
                target=mocked_function.function_name,
                return_value=json_data,
                create=True,
            )
        elif mocked_type == MockedFunctionType.SIDE_EFFECT:
            mocker.patch(
                target=mocked_function.function_name,
                side_effect=mocked_function.return_value,
                create=True,
            )
        else:
            mocker.patch(
                target=mocked_function.function_name,
                side_effect=mocked_function.return_value,
                create=True,
            )
