/**
 * NXTWALK Theme Engine
 * Manages Dark/Light mode, localStorage persistence, prefers-color-scheme,
 * and smooth transitions between visual themes.
 */

const STORAGE_KEY = 'nxtwalk-theme';
const THEMES = {
  DARK: 'dark',
  LIGHT: 'light',
};

/**
 * Returns user's active theme preference
 */
export function getTheme() {
  const saved = localStorage.getItem(STORAGE_KEY);
  if (saved && (saved === THEMES.DARK || saved === THEMES.LIGHT)) {
    return saved;
  }
  if (window.matchMedia && window.matchMedia('(prefers-color-scheme: light)').matches) {
    return THEMES.LIGHT;
  }
  return THEMES.DARK;
}

/**
 * Applies the specified theme to the root element and updates metadata
 */
export function applyTheme(theme) {
  document.documentElement.setAttribute('data-theme', theme);
  localStorage.setItem(STORAGE_KEY, theme);

  // Update mobile status bar theme color
  const metaThemeColor = document.getElementById('meta-theme-color');
  if (metaThemeColor) {
    metaThemeColor.setAttribute('content', theme === THEMES.LIGHT ? '#f8f9fc' : '#080b10');
  }

  // Update theme toggle button accessibility state
  const toggles = document.querySelectorAll('.theme-toggle');
  toggles.forEach((btn) => {
    btn.setAttribute('aria-pressed', theme === THEMES.LIGHT ? 'true' : 'false');
    btn.setAttribute('aria-label', theme === THEMES.LIGHT ? 'Switch to dark mode' : 'Switch to light mode');
    btn.setAttribute('title', theme === THEMES.LIGHT ? 'Switch to dark mode' : 'Switch to light mode');
  });

  // Broadcast theme change event for charts or dynamic components
  window.dispatchEvent(new CustomEvent('nxtwalk:themechange', { detail: { theme } }));
}

/**
 * Toggles between Dark and Light mode with smooth CSS transitions
 */
export function toggleTheme() {
  const currentTheme = document.documentElement.getAttribute('data-theme') || getTheme();
  const nextTheme = currentTheme === THEMES.DARK ? THEMES.LIGHT : THEMES.DARK;
  applyTheme(nextTheme);
}

/**
 * Initializes theme listener on toggles and system preference changes
 */
export function initializeTheme() {
  const current = getTheme();
  applyTheme(current);

  // Attach click handler to all theme toggles
  document.addEventListener('click', (event) => {
    const toggleBtn = event.target.closest('.theme-toggle');
    if (toggleBtn) {
      event.preventDefault();
      toggleTheme();
    }
  });

  // Listen to system preference changes if user hasn't explicitly set preference
  if (window.matchMedia) {
    window.matchMedia('(prefers-color-scheme: light)').addEventListener('change', (e) => {
      if (!localStorage.getItem(STORAGE_KEY)) {
        applyTheme(e.matches ? THEMES.LIGHT : THEMES.DARK);
      }
    });
  }
}
