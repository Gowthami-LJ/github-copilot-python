from flask.testing import FlaskClient


def test_home_route_returns_ok(client: FlaskClient) -> None:
    """The home route should start successfully and return HTTP 200."""
    response = client.get("/")

    assert response.status_code == 200
