from flask.testing import FlaskClient


def test_home_route_returns_ok(client: FlaskClient) -> None:
    """The home route should start successfully and return HTTP 200."""
    response = client.get("/")

    assert response.status_code == 200


def test_hard_game_returns_expected_clue_count(client: FlaskClient) -> None:
    """The hard difficulty should return a puzzle with 25 filled cells."""
    response = client.get("/new?difficulty=hard")
    puzzle = response.get_json()["puzzle"]

    assert response.status_code == 200
    assert sum(cell != 0 for row in puzzle for cell in row) == 25
