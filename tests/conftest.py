import pytest

from ales.app import create_app


@pytest.fixture
def client():
    test_app = create_app()
    with test_app.test_client() as client:
        yield client
