const STORAGE_KEY = 'sudokuLeaderboard';
const MAX_ENTRIES = 10;

function getStorage() {
  try {
    return window.localStorage;
  } catch (error) {
    return null;
  }
}

function isEntry(value) {
  return value !== null
    && typeof value === 'object'
    && typeof value.name === 'string'
    && Number.isFinite(value.elapsedTime)
    && typeof value.difficulty === 'string'
    && Number.isFinite(value.hints_used);
}

function sortEntries(entries) {
  return entries
    .filter(isEntry)
    .sort((first, second) => first.elapsedTime - second.elapsedTime)
    .slice(0, MAX_ENTRIES);
}

function loadEntries() {
  const storage = getStorage();
  if (storage === null) return [];

  try {
    const saved = JSON.parse(storage.getItem(STORAGE_KEY) || '[]');
    return Array.isArray(saved) ? sortEntries(saved) : [];
  } catch (error) {
    return [];
  }
}

function addEntry(entry) {
  const entries = sortEntries([...loadEntries(), entry]);
  const storage = getStorage();
  if (storage !== null) {
    try {
      storage.setItem(STORAGE_KEY, JSON.stringify(entries));
    } catch (error) {
      // Keep the current result available for this page even if storage fails.
    }
  }
  return entries;
}

function getTopEntries() {
  return loadEntries();
}

export {addEntry, getTopEntries, loadEntries};
