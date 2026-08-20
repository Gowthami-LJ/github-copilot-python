from typing import Any

from flask import Flask, jsonify, render_template, request

from sudoku import generator, validator

app = Flask(__name__)

# Keep a simple in-memory store for current puzzle and solution
CURRENT = {
    'puzzle': None,
    'solution': None
}

@app.route('/')
def index() -> str:
    """Render the Sudoku home page."""
    return render_template('index.html')

@app.route('/new')
def new_game() -> Any:
    """Generate a puzzle and return its clues as JSON."""
    clues = int(request.args.get('clues', 35))
    puzzle, solution = generator.generate_puzzle(clues)
    CURRENT['puzzle'] = puzzle
    CURRENT['solution'] = solution
    return jsonify({'puzzle': puzzle})

@app.route('/check', methods=['POST'])
def check_solution() -> Any:
    """Compare the submitted board with the current puzzle solution."""
    data = request.json
    board = data.get('board')
    solution = CURRENT.get('solution')
    if solution is None:
        return jsonify({'error': 'No game in progress'}), 400
    incorrect = validator.find_conflicts(board, solution)
    return jsonify({'incorrect': incorrect})

if __name__ == '__main__':
    app.run(debug=True)