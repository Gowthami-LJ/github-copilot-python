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


def count_solutions(board: Board, limit: int = 2) -> int:
    """Count valid Sudoku solutions, stopping once ``limit`` is reached.

    Args:
        board: A Sudoku board that may contain empty cells represented by zero.
        limit: Maximum number of solutions to count before returning.

    Returns:
        The number of solutions found, capped at ``limit``.
    """
    if limit <= 0:
        return 0

    for row in range(SIZE):
        for col in range(SIZE):
            value = board[row][col]
            if value == 0:
                continue
            if not 1 <= value <= SIZE:
                return 0
            board[row][col] = 0
            is_consistent = is_safe(board, row, col, value)
            board[row][col] = value
            if not is_consistent:
                return 0

    def search() -> int:
        first_empty: tuple[int, int] | None = None
        for row in range(SIZE):
            for col in range(SIZE):
                if board[row][col] == 0:
                    first_empty = (row, col)
                    break
            if first_empty is not None:
                break

        if first_empty is None:
            return 1

        row, col = first_empty
        solutions = 0
        for candidate in range(1, SIZE + 1):
            if is_safe(board, row, col, candidate):
                board[row][col] = candidate
                solutions += search()
                board[row][col] = 0
                if solutions >= limit:
                    return limit
        return solutions

    return search()
