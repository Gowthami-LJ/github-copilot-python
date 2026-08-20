from sudoku.solver import Board, SIZE


def is_valid_board(board: Board) -> bool:
    """Return whether a completed board satisfies Sudoku rules."""
    expected_values = set(range(1, SIZE + 1))

    if len(board) != SIZE or any(len(row) != SIZE for row in board):
        return False

    for row in board:
        if set(row) != expected_values:
            return False

    for col in range(SIZE):
        if {board[row][col] for row in range(SIZE)} != expected_values:
            return False

    for start_row in range(0, SIZE, 3):
        for start_col in range(0, SIZE, 3):
            box = {
                board[row][col]
                for row in range(start_row, start_row + 3)
                for col in range(start_col, start_col + 3)
            }
            if box != expected_values:
                return False

    return True


def find_conflicts(board: Board, solution: Board) -> list[list[int]]:
    """Return coordinates where a board differs from the expected solution."""
    conflicts = []
    for row in range(SIZE):
        for col in range(SIZE):
            if board[row][col] != solution[row][col]:
                conflicts.append([row, col])
    return conflicts
