from http import HTTPStatus
from typing import Any

import pytest
import responses
from pydantic import BaseModel


class MockedRequest(BaseModel):
    method: Any
    api_url: str
    content_file: str
    status: HTTPStatus


@pytest.fixture
def mocked_request_responses(mocked_request_list):
    for mocked_request in mocked_request_list:
        with responses.RequestsMock() as rsps:
            with open(mocked_request.content_file, "r") as f:
                content = f.read()
            rsps.add(
                mocked_request.method,
                mocked_request.api_url,
                body=content,
                status=mocked_request.status,
            )
            yield rsps
