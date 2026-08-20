import copy
import random

from sudoku.solver import Board, count_solutions, is_safe

SIZE = 9
EMPTY = 0
DIFFICULTY_CLUES = {
    "easy": 45,
    "medium": 35,
    "hard": 25,
}


def deep_copy(board: Board) -> Board:
    """Return a deep copy of a Sudoku board."""
    return copy.deepcopy(board)


def create_empty_board() -> Board:
    """Create a blank nine-by-nine Sudoku board."""
    return [[EMPTY for _ in range(SIZE)] for _ in range(SIZE)]


def fill_board(board: Board) -> bool:
    """Fill a board with a valid randomized Sudoku solution."""
    for row in range(SIZE):
        for col in range(SIZE):
            if board[row][col] == EMPTY:
                possible = list(range(1, SIZE + 1))
                random.shuffle(possible)
                for candidate in possible:
                    if is_safe(board, row, col, candidate):
                        board[row][col] = candidate
                        if fill_board(board):
                            return True
                        board[row][col] = EMPTY
                return False
    return True


def remove_cells(board: Board, clues: int) -> None:
    """Remove cells while preserving a unique solution where possible.

    Args:
        board: A completed Sudoku board to modify in place.
        clues: Target number of filled cells to retain.
    """
    filled_positions = [
        (row, col)
        for row in range(SIZE)
        for col in range(SIZE)
        if board[row][col] != EMPTY
    ]
    random.shuffle(filled_positions)

    remaining_clues = len(filled_positions)
    for row, col in filled_positions:
        if remaining_clues <= clues:
            break

        original_value = board[row][col]
        board[row][col] = EMPTY
        if count_solutions(deep_copy(board)) == 1:
            remaining_clues -= 1
        else:
            board[row][col] = original_value


def generate_puzzle(clues: int = 35) -> tuple[Board, Board]:
    """Generate a puzzle and its completed solution."""
    board = create_empty_board()
    fill_board(board)
    solution = deep_copy(board)
    remove_cells(board, clues)
    puzzle = deep_copy(board)
    return puzzle, solution
