(() => {
  "use strict";
  const key = "braincode-course-theme";
  const palette = document.getElementById("dark-palette");
  const chromeColor = document.getElementById("dark-chrome");
  const systemMedia = palette.media;
  let choice;

  function savedChoice() {
    try { return localStorage.getItem(key); } catch { return null; }
  }

  function apply(value) {
    const theme = value === "dark" || value === "light" ? value : "system";
    const media = theme === "system" ? systemMedia : theme === "dark" ? "screen" : "not all";
    palette.media = media;
    chromeColor.media = media;
    if (choice) choice.value = theme;
  }

  // Apply the palette before the body is painted. System mode follows OS changes through CSS.
  apply(savedChoice());
  document.addEventListener("DOMContentLoaded", () => {
    choice = document.getElementById("theme-choice");
    apply(savedChoice());
    choice.closest("label").hidden = false;
    choice.addEventListener("change", () => {
      apply(choice.value);
      try {
        if (choice.value === "system") localStorage.removeItem(key);
        else localStorage.setItem(key, choice.value);
      } catch { /* The current page still uses the selected palette. */ }
    });
  });
  window.addEventListener("storage", event => {
    if (event.key === key || event.key === null) apply(savedChoice());
  });
  window.addEventListener("pageshow", event => {
    if (event.persisted) apply(savedChoice());
  });
})();
