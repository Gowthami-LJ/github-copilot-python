// Client-side rendering and interaction for the Flask-backed Sudoku
import {
  formatElapsed,
  getElapsedSeconds,
  start as startTimer,
  stop as stopTimer,
} from './timer.js';
import {addEntry, getTopEntries} from './leaderboard.js';
import {initialize as initializeTheme, toggle as toggleTheme} from './theme.js';

initializeTheme();

const SIZE = 9;
let puzzle = [];
let prefilled = new Set();
let feedbackRequest = 0;
let completionRecorded = false;
let hintsUsed = 0;

function createBoardElement() {
  const boardDiv = document.getElementById('sudoku-board');
  boardDiv.innerHTML = '';
  for (let i = 0; i < SIZE; i++) {
    const rowDiv = document.createElement('div');
    rowDiv.className = 'sudoku-row';
    for (let j = 0; j < SIZE; j++) {
      const input = document.createElement('input');
      input.type = 'text';
      input.maxLength = 1;
      input.className = 'sudoku-cell';
      input.dataset.row = i;
      input.dataset.col = j;
      input.addEventListener('input', async (e) => {
        const val = e.target.value.replace(/[^1-9]/g, '');
        e.target.value = val;
        await checkCurrentBoard();
      });
      rowDiv.appendChild(input);
    }
    boardDiv.appendChild(rowDiv);
  }
}

function renderPuzzle(puz, lockedCells) {
  puzzle = puz;
  prefilled = new Set(lockedCells.map(([row, col]) => row * SIZE + col));
  createBoardElement();
  const boardDiv = document.getElementById('sudoku-board');
  const inputs = boardDiv.getElementsByTagName('input');
  for (let i = 0; i < SIZE; i++) {
    for (let j = 0; j < SIZE; j++) {
      const idx = i * SIZE + j;
      const val = puzzle[i][j];
      const inp = inputs[idx];
      if (prefilled.has(idx)) {
        inp.value = val;
        inp.disabled = true;
        inp.className = 'sudoku-cell prefilled';
      } else {
        inp.value = '';
        inp.disabled = false;
        inp.className = 'sudoku-cell';
      }
    }
  }
}

async function newGame() {
  const difficulty = document.getElementById('difficulty').value;
  const res = await fetch(`/new?difficulty=${encodeURIComponent(difficulty)}`);
  const data = await res.json();
  feedbackRequest += 1;
  completionRecorded = false;
  hintsUsed = 0;
  renderPuzzle(data.puzzle, data.prefilled);
  startTimer(updateTimerDisplay);
  document.getElementById('message').innerText = '';
}

function updateTimerDisplay(seconds = getElapsedSeconds()) {
  document.getElementById('timer').innerText = formatElapsed(seconds);
}

function getCurrentBoard() {
  const boardDiv = document.getElementById('sudoku-board');
  const inputs = boardDiv.getElementsByTagName('input');
  const board = [];
  for (let i = 0; i < SIZE; i++) {
    board[i] = [];
    for (let j = 0; j < SIZE; j++) {
      const idx = i * SIZE + j;
      const val = inputs[idx].value;
      board[i][j] = val ? parseInt(val, 10) : 0;
    }
  }
  return {board, inputs};
}

async function requestHint() {
  const {board, inputs} = getCurrentBoard();
  const res = await fetch('/hint', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({board})
  });
  const data = await res.json();
  const msg = document.getElementById('message');
  if (data.error) {
    msg.className = 'message-error';
    msg.innerText = data.error;
    return;
  }

  const idx = data.row * SIZE + data.col;
  const input = inputs[idx];
  input.value = data.value;
  input.disabled = true;
  input.className = 'sudoku-cell hint';
  prefilled.add(idx);
  hintsUsed = data.hints_used;
  msg.className = 'message-info';
  msg.innerText = `Hint used: ${data.hints_used}`;
}

function recordCompletion() {
  stopTimer();
  if (completionRecorded) return;

  completionRecorded = true;
  const enteredName = window.prompt('Enter your name for the leaderboard:');
  const name = enteredName && enteredName.trim() ? enteredName.trim() : 'Anonymous';
  addEntry({
    name,
    elapsedTime: getElapsedSeconds(),
    difficulty: document.getElementById('difficulty').value,
    hints_used: hintsUsed,
  });
  renderLeaderboard();
}

function renderLeaderboard() {
  const body = document.getElementById('leaderboard-body');
  body.innerHTML = '';
  getTopEntries().forEach((entry, index) => {
    const row = document.createElement('tr');
    const values = [
      index + 1,
      entry.name,
      formatElapsed(entry.elapsedTime),
      entry.difficulty,
      entry.hints_used,
    ];
    values.forEach((value) => {
      const cell = document.createElement('td');
      cell.textContent = value;
      row.appendChild(cell);
    });
    body.appendChild(row);
  });
}

async function checkCurrentBoard() {
  const requestId = ++feedbackRequest;
  const {board, inputs} = getCurrentBoard();
  const res = await fetch('/check', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({board})
  });
  const data = await res.json();
  if (requestId !== feedbackRequest) return;
  const msg = document.getElementById('message');
  if (data.error) {
    msg.className = 'message-error';
    msg.innerText = data.error;
    return;
  }
  const incorrect = new Set(
    data.incorrect
      .filter(([row, col]) => board[row][col] !== 0)
      .map(([row, col]) => row * SIZE + col)
  );
  for (let idx = 0; idx < inputs.length; idx++) {
    const inp = inputs[idx];
    if (inp.disabled) continue;
    inp.className = prefilled.has(idx)
      ? 'sudoku-cell prefilled'
      : 'sudoku-cell';
    if (incorrect.has(idx)) {
      inp.className = 'sudoku-cell live-incorrect';
    }
  }
  if (data.complete) {
    recordCompletion();
    msg.className = 'message-success';
    msg.innerText = 'Congratulations! You solved it!';
  } else if (incorrect.size > 0) {
    msg.className = 'message-error';
    msg.innerText = 'Some cells are incorrect.';
  } else {
    msg.className = '';
    msg.innerText = '';
  }
}

async function checkBoard() {
  const requestId = ++feedbackRequest;
  const {board, inputs} = getCurrentBoard();
  const res = await fetch('/check', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({board})
  });
  const data = await res.json();
  if (requestId !== feedbackRequest) return;

  const msg = document.getElementById('message');
  if (data.error) {
    msg.className = 'message-error';
    msg.innerText = data.error;
    return;
  }

  const incorrect = new Set(
    data.incorrect
      .map(([row, col]) => row * SIZE + col)
  );
  for (let idx = 0; idx < inputs.length; idx++) {
    const inp = inputs[idx];
    if (inp.disabled) continue;
    inp.className = 'sudoku-cell';
    if (incorrect.has(idx)) {
      inp.className = 'sudoku-cell checked-incorrect';
    }
  }

  if (data.complete) {
    recordCompletion();
    msg.className = 'message-success';
    msg.innerText = 'Congratulations! You solved it!';
  } else if (incorrect.size > 0) {
    msg.className = 'message-error';
    msg.innerText = 'Check found incorrect cells.';
  } else {
    msg.className = '';
    msg.innerText = '';
  }
}

// Wire buttons
window.addEventListener('load', () => {
  initializeTheme();
  document.getElementById('theme-toggle').addEventListener('click', toggleTheme);
  document.getElementById('new-game').addEventListener('click', newGame);
  document.getElementById('hint').addEventListener('click', requestHint);
  document.getElementById('check').addEventListener('click', checkBoard);
  renderLeaderboard();
  // initialize
  newGame();
});