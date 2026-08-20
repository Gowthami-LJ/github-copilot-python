const STORAGE_KEY = 'sudokuTheme';
const DARK_THEME = 'dark';
const LIGHT_THEME = 'light';

function getStorage() {
  try {
    return window.localStorage;
  } catch (error) {
    return null;
  }
}

function getSavedTheme() {
  const storage = getStorage();
  if (storage === null) return LIGHT_THEME;

  try {
    return storage.getItem(STORAGE_KEY) === DARK_THEME
      ? DARK_THEME
      : LIGHT_THEME;
  } catch (error) {
    return LIGHT_THEME;
  }
}

function applyTheme(theme) {
  const selectedTheme = theme === DARK_THEME ? DARK_THEME : LIGHT_THEME;
  document.documentElement.dataset.theme = selectedTheme;
  const toggle = document.getElementById('theme-toggle');
  if (toggle !== null) {
    const isDark = selectedTheme === DARK_THEME;
    toggle.textContent = isDark ? 'Light mode' : 'Dark mode';
    toggle.setAttribute('aria-pressed', String(isDark));
  }
  return selectedTheme;
}

function saveTheme(theme) {
  const storage = getStorage();
  if (storage === null) return;

  try {
    storage.setItem(STORAGE_KEY, theme);
  } catch (error) {
    // Continue with the current theme when storage is unavailable or full.
  }
}

function initialize() {
  return applyTheme(getSavedTheme());
}

function toggle() {
  const nextTheme = document.documentElement.dataset.theme === DARK_THEME
    ? LIGHT_THEME
    : DARK_THEME;
  applyTheme(nextTheme);
  saveTheme(nextTheme);
  return nextTheme;
}

export {initialize, toggle};
