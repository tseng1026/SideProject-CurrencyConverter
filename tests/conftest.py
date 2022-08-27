from typing import Generator

import pytest
from app.main import app
from fastapi.testclient import TestClient

pytest_plugins = ("tests.fixtures",)


@pytest.fixture
def fastapi_client() -> Generator:
    with TestClient(app) as test_client:
        yield test_client
