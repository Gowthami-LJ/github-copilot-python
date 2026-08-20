// Client-side rendering and interaction for the Flask-backed Sudoku
const SIZE = 9;
let puzzle = [];
let prefilled = new Set();
let feedbackRequest = 0;

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
  renderPuzzle(data.puzzle, data.prefilled);
  document.getElementById('message').innerText = '';
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
    msg.style.color = '#d32f2f';
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
      inp.className = 'sudoku-cell incorrect';
    }
  }
  if (data.complete) {
    msg.style.color = '#388e3c';
    msg.innerText = 'Congratulations! You solved it!';
  } else if (incorrect.size > 0) {
    msg.style.color = '#d32f2f';
    msg.innerText = 'Some cells are incorrect.';
  } else {
    msg.innerText = '';
  }
}

async function checkSolution() {
  await checkCurrentBoard();
}

// Wire buttons
window.addEventListener('load', () => {
  document.getElementById('new-game').addEventListener('click', newGame);
  document.getElementById('check-solution').addEventListener('click', checkSolution);
  // initialize
  newGame();
});