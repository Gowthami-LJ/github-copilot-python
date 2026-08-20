from sudoku.generator import generate_puzzle
from sudoku.solver import count_solutions
from sudoku.validator import find_conflicts, is_valid_board


VALID_BOARD = [
    [5, 3, 4, 6, 7, 8, 9, 1, 2],
    [6, 7, 2, 1, 9, 5, 3, 4, 8],
    [1, 9, 8, 3, 4, 2, 5, 6, 7],
    [8, 5, 9, 7, 6, 1, 4, 2, 3],
    [4, 2, 6, 8, 5, 3, 7, 9, 1],
    [7, 1, 3, 9, 2, 4, 8, 5, 6],
    [9, 6, 1, 5, 3, 7, 2, 8, 4],
    [2, 8, 7, 4, 1, 9, 6, 3, 5],
    [3, 4, 5, 2, 8, 6, 1, 7, 9],
]


def test_generated_puzzle_has_a_valid_solution() -> None:
    """Generated solutions should satisfy the complete Sudoku rules."""
    _, solution = generate_puzzle()

    assert is_valid_board(solution)


def test_generated_puzzle_has_exactly_one_solution() -> None:
    """Generated puzzles should have exactly one valid solution."""
    puzzle, _ = generate_puzzle()

    assert count_solutions(puzzle) == 1


def test_find_conflicts_returns_changed_cell_coordinates() -> None:
    """Validation should identify every cell that differs from the solution."""
    board = [row[:] for row in VALID_BOARD]
    board[0][0] = 0
    board[8][8] = 1

    assert find_conflicts(board, VALID_BOARD) == [[0, 0], [8, 8]]
