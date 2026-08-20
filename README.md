# Sudoku Game (Flask)

A full-featured Sudoku web app, refactored from a legacy Flask starter project
using GitHub Copilot. Generates puzzles with a guaranteed unique solution,
supports three difficulty levels, hints, live/explicit answer checking, a
timer, a persistent Top 10 leaderboard, and light/dark themes.

## Features

- Puzzle generation with guaranteed unique solutions (backtracking solver
  with early-exit solution counting)
- Difficulty levels: Easy (45 clues), Medium (35 clues), Hard (~25 clues)
- Locked prefilled cells
- Live, per-cell feedback as you type
- Explicit "Check" button for full-board review
- Hint button (fills and locks one correct cell, tracked per game)
- Completion detection with a congratulatory message
- Timer (mm:ss), starts on new game, stops on completion
- Top 10 fastest times, persisted in localStorage (name, time, difficulty,
  hints used)
- Light/dark mode toggle, persisted across sessions
- Responsive layout (mobile through desktop)

## Setup

1. Clone the repo and navigate to the `starter` folder:
```bash
   git clone <your-repo-url>
   cd github-copilot-python/starter
```

2. Create and activate a virtual environment:
```bash
   python -m venv .venv
   # Windows PowerShell:
   .\.venv\Scripts\Activate.ps1
   # macOS/Linux:
   source .venv/bin/activate
```

3. Install dependencies:
```bash
   pip install -r requirements.txt
```

4. Run the app:
```bash
   python app.py
```

5. Open `http://127.0.0.1:5000` in your browser.

## Running Tests

```bash
pytest
```

All backend logic (puzzle generation, uniqueness validation, routes, hint
and check endpoints, solution-privacy) is covered by the test suite in
`tests/`.

## Project Structure

starter/
├── app.py # Flask routes
├── sudoku/
│ ├── generator.py # Puzzle generation, difficulty clue counts
│ ├── validator.py # Board validation, conflict detection
│ └── solver.py # Constraint checking, solution counting (MRV)
├── static/
│ ├── main.js
│ ├── timer.js
│ ├── leaderboard.js
│ ├── theme.js
│ └── styles.css
├── templates/
│ └── index.html
├── tests/
│ ├── test_app.py
│ └── test_sudoku.py
├── instructions.md # Copilot context/style guide used for this project
└── Screenshots/ # Required milestone screenshots


## Working with GitHub Copilot

This project was refactored and extended using GitHub Copilot (Agent mode)
in VS Code, guided by an `instructions.md` file describing the project's
coding standards (modular structure, type hints, docstrings, CSS-variable
theming, testing requirements).

Development followed a "start broad, then narrow" approach: the legacy code
was first refactored into a modular `sudoku/` package (generator, validator,
solver) with behavior unchanged, then features were added incrementally,
running the test suite after every change.

A few notable places where I evaluated and adjusted Copilot's output rather
than accepting it as-is:

- **Puzzle uniqueness**: The original legacy `remove_cells()` removed cells
  randomly with no uniqueness check, which could produce puzzles with
  multiple solutions. I asked Copilot to add a `count_solutions()` function
  and rewrite cell removal to verify uniqueness before committing to each
  removal.
- **Performance**: The uniqueness-checked generation was initially slow
  (~4s for Hard difficulty). I asked Copilot to optimize `count_solutions`
  with an empty-cell tracking + minimum-remaining-values heuristic, which
  brought Hard generation down to under a second on average.
- **Solution privacy**: When adding live feedback and hints, I explicitly
  asked Copilot not to expose the full solution to the client. It
  implemented server-side checking via `/check` and `/hint`, returning only
  the specific data needed (conflict coordinates, one hint cell), and added
  tests confirming the solution is never present in API responses.
- **Test suite bug**: While adding hints, Copilot noticed an existing test
  incorrectly assumed Hard difficulty always produces exactly 25 clues,
  when the uniqueness-preserving remover sometimes stops at 26+ to avoid
  ambiguous puzzles. This was corrected rather than silently ignored.

See the `Screenshots/` folder for prompt/response evidence from each major
milestone.

## Note on Difficulty Clue Counts

Because puzzle generation prioritizes a unique solution over hitting an
exact clue count, "Hard" difficulty targets 25 clues but may occasionally
settle for slightly more if removing further cells would create an
ambiguous (multi-solution) puzzle.
