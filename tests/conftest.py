from typing import Generator

import pytest
from fastapi.testclient import TestClient
from main import app

pytest_plugins = ("tests.fixtures",)


@pytest.fixture
def fastapi_client() -> Generator:
    with TestClient(app) as test_client:
        yield test_client
