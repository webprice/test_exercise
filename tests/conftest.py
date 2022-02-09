import pytest
from main import app
from fastapi.testclient import TestClient

#client = TestClient(app)

@pytest.fixture(scope="function")
def client():
    with TestClient(app) as client:   # context manager will invoke startup event
        yield client
