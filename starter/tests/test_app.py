from flask.testing import FlaskClient

from app import CURRENT


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


def test_new_game_returns_prefilled_cells_without_solution(
    client: FlaskClient,
) -> None:
    """New games identify locked cells without returning the solution."""
    response = client.get("/new?difficulty=easy")
    data = response.get_json()
    puzzle = data["puzzle"]
    prefilled = {tuple(cell) for cell in data["prefilled"]}

    assert prefilled == {
        (row, col)
        for row in range(9)
        for col in range(9)
        if puzzle[row][col] != 0
    }
    assert "solution" not in data


def test_check_reports_completion_for_matching_full_board(
    client: FlaskClient,
) -> None:
    """A complete board matching the active solution is reported complete."""
    client.get("/new?difficulty=easy")
    response = client.post("/check", json={"board": CURRENT["solution"]})

    assert response.get_json() == {"incorrect": [], "complete": True}
