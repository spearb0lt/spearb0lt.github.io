// Click behaviour for the CV page download control (_includes/cv/render.liquid,
// configured in _pages/cv.md under `cv_downloads:`). Only loaded for the styles
// that actually open a menu: menu, menu-caret, split and split-divided.
//
// In the split styles the glyph is a plain link and is deliberately left alone
// here, so it downloads the short file without JS; only the caret is wired up.
(function () {
  const groups = document.querySelectorAll("[data-cv-dl]");
  if (!groups.length) return;

  function closeAll() {
    groups.forEach(function (group) {
      const menu = group.querySelector("[data-cv-dl-menu]");
      const trigger = group.querySelector("[data-cv-dl-trigger]");
      if (menu) menu.hidden = true;
      if (trigger) trigger.setAttribute("aria-expanded", "false");
    });
  }

  groups.forEach(function (group) {
    const trigger = group.querySelector("[data-cv-dl-trigger]");
    const menu = group.querySelector("[data-cv-dl-menu]");
    if (!trigger || !menu) return;

    trigger.addEventListener("click", function (event) {
      event.stopPropagation();
      const willOpen = menu.hidden;
      closeAll();
      menu.hidden = !willOpen;
      trigger.setAttribute("aria-expanded", String(willOpen));
    });

    menu.addEventListener("click", function (event) {
      event.stopPropagation();
    });
  });

  document.addEventListener("click", closeAll);
  document.addEventListener("keydown", function (event) {
    if (event.key === "Escape") closeAll();
  });
})();
