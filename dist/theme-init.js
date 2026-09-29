// Apply the saved palette before the first paint. New visitors start in dark mode.
(() => {
  const requested = new URLSearchParams(window.location.search).get('theme');
  let saved;
  try {
    saved = window.localStorage.getItem('song-cheng-theme');
  } catch {
    // Direct file previews and restricted browsers may not expose storage.
  }
  const theme = [requested, saved].find(value => value === 'light' || value === 'dark') || 'dark';
  document.documentElement.dataset.theme = theme;
  document.documentElement.style.colorScheme = theme;
  document.querySelector('meta[name="theme-color"]').content = theme === 'dark' ? '#1a2b23' : '#173e35';
})();
