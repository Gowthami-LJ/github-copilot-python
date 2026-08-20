let intervalId = null;
let startedAt = null;
let elapsedSeconds = 0;

function getElapsedSeconds() {
  if (startedAt === null) {
    return elapsedSeconds;
  }
  return Math.floor((Date.now() - startedAt) / 1000);
}

function formatElapsed(seconds) {
  const minutes = Math.floor(seconds / 60);
  const remainingSeconds = seconds % 60;
  return `${String(minutes).padStart(2, '0')}:${String(remainingSeconds).padStart(2, '0')}`;
}

function start(onTick = () => {}) {
  reset();
  startedAt = Date.now();
  onTick(0);
  intervalId = setInterval(() => onTick(getElapsedSeconds()), 1000);
}

function stop() {
  if (startedAt !== null) {
    elapsedSeconds = getElapsedSeconds();
  }
  startedAt = null;
  if (intervalId !== null) {
    clearInterval(intervalId);
    intervalId = null;
  }
  return elapsedSeconds;
}

function reset() {
  stop();
  elapsedSeconds = 0;
}

export {formatElapsed, getElapsedSeconds, reset, start, stop};
