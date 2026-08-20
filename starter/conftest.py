from collections.abc import Iterator

import pytest
from flask.testing import FlaskClient

from app import app


@pytest.fixture
def client() -> Iterator[FlaskClient]:
    """Provide a Flask test client for application tests."""
    app.config.update(TESTING=True)

    with app.test_client() as test_client:
        yield test_client
