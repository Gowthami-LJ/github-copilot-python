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


def test_check_identifies_wrong_cell_without_exposing_solution(
    client: FlaskClient,
) -> None:
    """Check should flag a wrong value without returning the solution."""
    client.get("/new?difficulty=easy")
    puzzle = [row[:] for row in CURRENT["puzzle"]]
    row, col = next(
        (row, col)
        for row in range(9)
        for col in range(9)
        if puzzle[row][col] == 0
    )
    solution_value = CURRENT["solution"][row][col]
    puzzle[row][col] = solution_value % 9 + 1

    response = client.post("/check", json={"board": puzzle})
    data = response.get_json()

    assert [row, col] in data["incorrect"]
    assert "solution" not in data


def test_hint_fills_an_empty_editable_cell_and_tracks_usage(
    client: FlaskClient,
) -> None:
    """A hint returns one solution value without exposing the full solution."""
    new_response = client.get("/new?difficulty=easy")
    puzzle = new_response.get_json()["puzzle"]
    board = [row[:] for row in puzzle]

    response = client.post("/hint", json={"board": board})
    data = response.get_json()

    assert response.status_code == 200
    assert board[data["row"]][data["col"]] == 0
    assert data["value"] == CURRENT["solution"][data["row"]][data["col"]]
    assert data["hints_used"] == 1
    assert set(data) == {"row", "col", "value", "hints_used"}


def test_hint_rejects_a_complete_board(client: FlaskClient) -> None:
    """Hints should fail clearly after the active board is complete."""
    client.get("/new?difficulty=easy")

    response = client.post("/hint", json={"board": CURRENT["solution"]})

    assert response.status_code == 400
    assert response.get_json() == {"error": "The board is already complete"}


def test_hint_requires_a_game(client: FlaskClient) -> None:
    """Hints should fail clearly when no game is active."""
    CURRENT["solution"] = None
    CURRENT["puzzle"] = None

    response = client.post("/hint", json={"board": []})

    assert response.status_code == 400
    assert response.get_json() == {"error": "No game in progress"}
