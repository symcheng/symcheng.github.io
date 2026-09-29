'use strict';
const toggle = document.querySelector('.language-toggle');
const themeToggle = document.querySelector('.theme-toggle');
let currentLanguage = 'en';

function currentTheme() {
  return document.documentElement.dataset.theme === 'light' ? 'light' : 'dark';
}

function updateThemeButton() {
  const dark = currentTheme() === 'dark';
  const chinese = currentLanguage === 'zh';
  const label = chinese ? (dark ? '切换至浅色模式' : '切换至深色模式') : (dark ? 'Switch to light mode' : 'Switch to dark mode');
  themeToggle.setAttribute('aria-label', label);
  themeToggle.setAttribute('title', label);
  themeToggle.querySelector('.theme-label').textContent = chinese ? (dark ? '浅色' : '深色') : (dark ? 'Light' : 'Dark');
}

function updatePageUrl() {
  const url = new URL(window.location.href);
  if (currentLanguage === 'zh') url.searchParams.set('lang', 'zh');
  else url.searchParams.delete('lang');
  url.searchParams.set('theme', currentTheme());
  // Some browsers prohibit query changes to file: history entries.
  // The selected preferences still travel through links in that case.
  try {
    window.history.replaceState({}, '', url);
  } catch (error) {
    if (window.location.protocol !== 'file:' || error.name !== 'SecurityError') throw error;
  }
}

function syncPageLinks() {
  document.querySelectorAll('a[href]').forEach(link => {
    const url = new URL(link.getAttribute('href'), window.location.href);
    // Match protocols as well as origins: file: and mailto: both have opaque origins.
    if (url.protocol !== window.location.protocol || url.origin !== window.location.origin || /\.pdf$/i.test(url.pathname)) return;
    if (currentLanguage === 'zh') url.searchParams.set('lang', 'zh');
    else url.searchParams.delete('lang');
    // Explicit themes also work between file: pages with isolated or unavailable storage.
    url.searchParams.set('theme', currentTheme());
    link.setAttribute('href', url.href);
  });
}

function setTheme(theme, remember = true) {
  document.documentElement.dataset.theme = theme === 'dark' ? 'dark' : 'light';
  document.documentElement.style.colorScheme = currentTheme();
  document.querySelector('meta[name="theme-color"]').content = currentTheme() === 'dark' ? '#111c18' : '#173e35';
  if (remember) {
    try {
      window.localStorage.setItem('song-cheng-theme', currentTheme());
    } catch {
      // The URL carries this choice even when browser storage is unavailable.
    }
  }
  updateThemeButton();
  updatePageUrl();
  syncPageLinks();
}

function setLanguage(language, updateUrl = false) {
  currentLanguage = language === 'zh' ? 'zh' : 'en';
  const chinese = currentLanguage === 'zh';
  document.documentElement.lang = chinese ? 'zh-CN' : 'en';
  document.querySelectorAll('[data-en][data-zh]').forEach(element => {
    element.textContent = element.dataset[currentLanguage];
    element.lang = chinese ? 'zh-CN' : 'en';
  });
  document.querySelectorAll('[data-content-en][data-content-zh]').forEach(element => {
    element.setAttribute('content', element.getAttribute(`data-content-${currentLanguage}`));
  });
  document.querySelectorAll('[data-aria-label-en][data-aria-label-zh]').forEach(element => {
    element.setAttribute('aria-label', element.getAttribute(`data-aria-label-${currentLanguage}`));
  });
  document.querySelectorAll('[data-alt-en][data-alt-zh]').forEach(element => {
    element.alt = element.getAttribute(`data-alt-${currentLanguage}`);
  });
  toggle.innerHTML = chinese ? 'EN <span aria-hidden="true">↔</span>' : '中文 <span aria-hidden="true">↔</span>';
  toggle.setAttribute('aria-label', chinese ? 'Switch to English' : 'Switch to Chinese');
  const navigation = document.querySelector('.navigation');
  navigation.setAttribute('aria-label', chinese ? '主导航' : 'Main navigation');
  const portrait = document.querySelector('.hero-portrait img');
  if (portrait) portrait.alt = chinese ? '程嵩的蜡笔插画肖像，背景黑板上写有 PEPS 波函数公式和方格张量网络图。' : 'Crayon illustration of Song Cheng in front of a chalkboard with a PEPS wavefunction formula and square-lattice tensor network diagrams.';
  updateThemeButton();
  if (updateUrl) updatePageUrl();
  syncPageLinks();
}

toggle.addEventListener('click', () => setLanguage(currentLanguage === 'en' ? 'zh' : 'en', true));
themeToggle.addEventListener('click', () => setTheme(currentTheme() === 'light' ? 'dark' : 'light'));
setLanguage(new URLSearchParams(window.location.search).get('lang') === 'zh' ? 'zh' : 'en');

// Reconcile pages restored from the browser's back/forward cache with a newer choice.
window.addEventListener('pageshow', event => {
  if (!event.persisted) return;
  try {
    const saved = window.localStorage.getItem('song-cheng-theme');
    if (saved === 'dark' || saved === 'light') setTheme(saved, false);
  } catch {
    // The page retains its current theme if storage is restricted.
  }
});
