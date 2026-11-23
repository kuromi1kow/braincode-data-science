(() => {
  "use strict";
  const key = "braincode-course-theme";
  const palette = document.getElementById("dark-palette");
  const chromeColor = document.getElementById("dark-chrome");
  const systemMedia = palette.media;
  const systemDark = window.matchMedia("(prefers-color-scheme: dark)");
  let preference;
  let toggle, systemButton;

  function savedChoice() {
    try { return localStorage.getItem(key); } catch { return null; }
  }

  function isDark() {
    return preference === "dark" || (preference === "system" && systemDark.matches);
  }

  function updateButtons() {
    if (!toggle) return;
    const dark = isDark();
    toggle.setAttribute("aria-pressed", String(dark));
    toggle.title = dark ? "Включить светлую тему" : "Включить тёмную тему";
    systemButton.setAttribute("aria-pressed", String(preference === "system"));
  }

  function apply(value) {
    preference = value === "dark" || value === "light" ? value : "system";
    const media = preference === "system" ? systemMedia : preference === "dark" ? "screen" : "not all";
    palette.media = media;
    chromeColor.media = media;
    updateButtons();
  }

  function choose(value) {
    apply(value);
    try {
      if (value === "system") localStorage.removeItem(key);
      else localStorage.setItem(key, value);
    } catch { /* The choice still applies to this page. */ }
  }

  apply(savedChoice());
  document.addEventListener("DOMContentLoaded", () => {
    toggle = document.getElementById("theme-toggle");
    systemButton = document.getElementById("theme-system");
    updateButtons();
    toggle.addEventListener("click", () => choose(isDark() ? "light" : "dark"));
    systemButton.addEventListener("click", () => choose("system"));
  });
  systemDark.addEventListener("change", updateButtons);
  window.addEventListener("storage", event => {
    if (event.key === key || event.key === null) apply(savedChoice());
  });
  window.addEventListener("pageshow", event => {
    if (event.persisted) apply(savedChoice());
  });
})();
