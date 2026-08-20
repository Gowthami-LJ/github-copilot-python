from typing import TypeAlias

Board: TypeAlias = list[list[int]]

SIZE = 9


def is_safe(board: Board, row: int, col: int, num: int) -> bool:
    """Return whether placing ``num`` is safe at the given board position.

    Args:
        board: The Sudoku board to inspect.
        row: Zero-based row index for the candidate position.
        col: Zero-based column index for the candidate position.
        num: Candidate value to place.

    Returns:
        True when the candidate does not conflict with its row, column, or box.
    """
    for index in range(SIZE):
        if board[row][index] == num or board[index][col] == num:
            return False

    start_row = row - row % 3
    start_col = col - col % 3
    for box_row in range(3):
        for box_col in range(3):
            if board[start_row + box_row][start_col + box_col] == num:
                return False
    return True
