"""Backward-compatible imports for the legacy Sudoku logic module."""

from sudoku.generator import (
    EMPTY,
    SIZE,
    create_empty_board,
    deep_copy,
    fill_board,
    generate_puzzle,
    remove_cells,
)
from sudoku.solver import is_safe
