from typing import Any

from flask import Flask, jsonify, render_template, request

from sudoku import generator, validator

app = Flask(__name__)

# Keep a simple in-memory store for current puzzle and solution
CURRENT = {
    "puzzle": None,
    "solution": None,
    "hints_used": 0,
}

@app.route('/')
def index() -> str:
    """Render the Sudoku home page."""
    return render_template('index.html')

@app.route('/new')
def new_game() -> Any:
    """Generate a puzzle and return its clues as JSON."""
    difficulty = request.args.get("difficulty", "medium").lower()
    clues = generator.DIFFICULTY_CLUES.get(
        difficulty, generator.DIFFICULTY_CLUES["medium"]
    )
    puzzle, solution = generator.generate_puzzle(clues)
    CURRENT["puzzle"] = puzzle
    CURRENT["solution"] = solution
    CURRENT["hints_used"] = 0
    prefilled = [
        [row, col]
        for row in range(generator.SIZE)
        for col in range(generator.SIZE)
        if puzzle[row][col] != generator.EMPTY
    ]
    return jsonify({"puzzle": puzzle, "prefilled": prefilled})


@app.route("/hint", methods=["POST"])
def hint() -> Any:
    """Fill and return one currently empty, editable cell."""
    solution = CURRENT.get("solution")
    puzzle = CURRENT.get("puzzle")
    if solution is None or puzzle is None:
        return jsonify({"error": "No game in progress"}), 400

    data = request.get_json(silent=True) or {}
    board = data.get("board")
    if not isinstance(board, list):
        return jsonify({"error": "A board is required to request a hint"}), 400

    for row in range(generator.SIZE):
        for col in range(generator.SIZE):
            if puzzle[row][col] == generator.EMPTY and board[row][col] == generator.EMPTY:
                CURRENT["hints_used"] += 1
                return jsonify(
                    {
                        "row": row,
                        "col": col,
                        "value": solution[row][col],
                        "hints_used": CURRENT["hints_used"],
                    }
                )

    return jsonify({"error": "The board is already complete"}), 400

@app.route('/check', methods=['POST'])
def check_solution() -> Any:
    """Compare the submitted board with the current puzzle solution."""
    data = request.json
    board = data.get('board')
    solution = CURRENT.get('solution')
    if solution is None:
        return jsonify({'error': 'No game in progress'}), 400
    incorrect = validator.find_conflicts(board, solution)
    complete = not incorrect and all(
        cell != generator.EMPTY for row in board for cell in row
    )
    return jsonify({'incorrect': incorrect, 'complete': complete})

if __name__ == '__main__':
    app.run(debug=True)