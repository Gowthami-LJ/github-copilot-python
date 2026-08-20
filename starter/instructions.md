# Copilot Instructions for Sudoku Refactor Project

## Project Context
This is a Flask-based Sudoku game being refactored from legacy code into a
modern, modular, full-featured web app. Follow these standards for all
suggestions and generated code.

## Python Standards
- Target Python 3.10+, use type hints on all function signatures
- Use docstrings (Google style) for all non-trivial functions
- Wrap I/O and logic that can fail (file access, puzzle generation, request
  parsing) in try/except with meaningful error messages — no silent failures
- Prefer pure functions for puzzle logic (generation, validation, solving)
  so they're easy to unit test
- Follow PEP 8; use `black`-style formatting

## Project Structure
- Keep Flask routes thin — business logic (puzzle generation, validation,
  scoring) belongs in separate modules under a `sudoku/` package, not in
  `app.py`
- Modules: `sudoku/generator.py`, `sudoku/validator.py`, `sudoku/solver.py`,
  `routes.py` (single file, registered on the Flask app — no blueprints
  needed at this scale)
- Templates in `templates/`, static assets in `static/` (`static/css`,
  `static/js`)

## Frontend Standards
- Plain CSS with CSS custom properties (variables) for theming — required
  for dark mode to work cleanly
- Mobile-first responsive design using flexbox/grid, test at 375px and
  1440px widths minimum
- No inline styles in HTML/templates; keep all styling in CSS files
- Plain vanilla JavaScript, split into modules by concern: `timer.js`,
  `board.js`, `leaderboard.js`, `theme.js` — avoid one giant script file
- No frontend framework/build step; app is server-rendered via Jinja2

## Testing
- Use `pytest` for backend tests
- Every new backend feature (puzzle generation, validation, hint logic)
  needs at least one test before being considered done
- Run `pytest` after every meaningful change and before moving to the next
  feature

## Working Style
- When generating a new feature, explain the approach briefly before writing
  code
- Flag any suggestion that introduces a new dependency — I want to approve
  new packages explicitly
- If a suggestion seems overly complex for the problem, offer a simpler
  alternative alongside it