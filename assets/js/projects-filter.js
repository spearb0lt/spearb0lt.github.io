/**
 * Client-side filtering for /projects/.
 *
 * Markup lives in _pages/projects.md, styling in assets/css/main.scss, and the
 * on/off switches in _data/project_tags.yml. There is no index and no build
 * step: every card already carries its own searchable text in `data-pf-text`,
 * so this only ever hides and unhides nodes that are already on the page.
 *
 * Two filters combine:
 *   - the text box, an AND over whitespace-separated terms, matched against
 *     the card's title, description, category and EVERY tag it owns -- including
 *     the ones families_on hides from the card;
 *   - the Filter dropdown, which combines its ticked facets as OR or AND
 *     depending on _data/project_tags.yml's search.filter_mode ("any"/"all").
 *
 * The controls start hidden and are unhidden from here, which means a visitor
 * without JS sees the complete grid instead of a search box that does nothing.
 */
(function () {
  "use strict";

  function init() {
    var grid = document.querySelector(".projects");
    var bar = document.querySelector(".projects-filter");
    if (!grid || !bar) return;

    var input = bar.querySelector(".pf-input");
    var clearBtn = bar.querySelector(".pf-clear");
    var toggle = bar.querySelector(".pf-toggle");
    var menu = bar.querySelector(".pf-menu");
    var badge = bar.querySelector(".pf-badge");
    var countEl = bar.querySelector(".pf-count");
    var resetBtn = bar.querySelector(".pf-reset");
    var boxes = Array.prototype.slice.call(bar.querySelectorAll(".pf-opt input"));
    var activeBox = document.querySelector(".pf-active");
    var emptyEl = document.querySelector(".pf-empty");
    if (!input) return;

    // "tags" matches against a card's tag list, "categories" against its
    // section. Clicking a pill on a card only makes sense in tag mode.
    var facetMode = bar.getAttribute("data-pf-filter-by") === "categories" ? "categories" : "tags";
    var facetCombine = bar.getAttribute("data-pf-filter-mode") === "all" ? "all" : "any";
    var clickable = grid.classList.contains("pf-clickable") && facetMode === "tags";
    if (!clickable) grid.classList.remove("pf-clickable");

    var cards = Array.prototype.slice.call(grid.querySelectorAll("[data-pf-text]"));
    var sections = Array.prototype.slice.call(grid.querySelectorAll("[data-pf-section]"));
    var selected = [];
    var total = cards.length;

    // Cache each card's haystack once. Splitting a delimited string beats
    // re-querying the DOM on every keystroke.
    cards.forEach(function (card) {
      card._pfText = (card.getAttribute("data-pf-text") || "").toLowerCase();
      var tags = card.getAttribute("data-pf-tags") || "";
      card._pfTags = tags ? tags.split("|") : [];
      card._pfCat = card.getAttribute("data-pf-cat") || "";
    });

    function facetsOf(card) {
      return facetMode === "categories" ? [card._pfCat] : card._pfTags;
    }

    function matches(card, terms) {
      for (var i = 0; i < terms.length; i++) {
        if (card._pfText.indexOf(terms[i]) === -1) return false;
      }
      if (!selected.length) return true;

      var own = facetsOf(card);
      if (facetCombine === "all") {
        // AND: every ticked facet must be on the card.
        for (var j = 0; j < selected.length; j++) {
          if (own.indexOf(selected[j]) === -1) return false;
        }
        return true;
      }
      // OR (default): any one ticked facet on the card is enough.
      for (var k = 0; k < selected.length; k++) {
        if (own.indexOf(selected[k]) !== -1) return true;
      }
      return false;
    }

    // Minimal stand-in for CSS.escape, which Safari shipped late. Facets are
    // slugs in practice, so quoting the two characters that could break an
    // attribute selector is enough.
    function cssEscape(value) {
      return value.replace(/["\\]/g, "\\$&");
    }

    function renderActive() {
      if (!activeBox) return;
      activeBox.textContent = "";
      if (!selected.length) return;

      selected.forEach(function (facet) {
        // Reuse the pill that is already on a card so the colour family comes
        // along without duplicating the tag -> family map in JavaScript.
        var source = grid.querySelector('.card .proj-tag[data-pf-tag="' + cssEscape(facet) + '"]');
        var chip;
        if (source) {
          chip = source.cloneNode(true);
          chip.classList.remove("pt-overflow", "is-active");
        } else {
          chip = document.createElement("span");
          chip.className = "proj-tag";
          chip.textContent = facet;
        }
        chip.setAttribute("data-pf-tag", facet);
        chip.setAttribute("role", "button");
        chip.setAttribute("tabindex", "0");
        chip.setAttribute("aria-label", "Remove filter " + facet);
        chip.addEventListener("click", function () {
          toggleFacet(facet);
        });
        chip.addEventListener("keydown", function (e) {
          if (e.key === "Enter" || e.key === " ") {
            e.preventDefault();
            toggleFacet(facet);
          }
        });
        activeBox.appendChild(chip);
      });
    }

    function apply() {
      var query = input.value.trim().toLowerCase();
      var terms = query ? query.split(/\s+/) : [];
      var filtering = terms.length > 0 || selected.length > 0;
      var shown = 0;

      cards.forEach(function (card) {
        var ok = !filtering || matches(card, terms);
        card.classList.toggle("pf-hidden", !ok);
        if (ok) shown++;
      });

      // A category heading with nothing under it is noise, so drop the whole
      // block once every card inside it is hidden.
      var seenFirst = false;
      sections.forEach(function (section) {
        var visible = section.querySelector("[data-pf-text]:not(.pf-hidden)");
        section.classList.toggle("pf-hidden", !visible);
        // The topmost surviving section loses its heading's top margin, which
        // main.scss relies on to keep the gap under the page header constant.
        section.classList.toggle("pf-first", Boolean(visible) && !seenFirst);
        if (visible) seenFirst = true;
      });

      grid.classList.toggle("is-filtering", filtering);

      if (clickable) {
        var pills = grid.querySelectorAll(".card .proj-tag[data-pf-tag]");
        Array.prototype.forEach.call(pills, function (pill) {
          pill.classList.toggle("is-active", selected.indexOf(pill.getAttribute("data-pf-tag")) !== -1);
        });
      }

      boxes.forEach(function (box) {
        box.checked = selected.indexOf(box.value) !== -1;
      });

      if (badge) {
        badge.hidden = selected.length === 0;
        badge.textContent = selected.length ? String(selected.length) : "";
      }
      if (clearBtn) clearBtn.classList.toggle("is-visible", input.value.length > 0);
      if (emptyEl) emptyEl.classList.toggle("is-visible", shown === 0);
      if (countEl) {
        countEl.textContent = filtering ? shown + " of " + total : total + " projects";
      }

      renderActive();
    }

    function toggleFacet(facet) {
      var i = selected.indexOf(facet);
      if (i === -1) selected.push(facet);
      else selected.splice(i, 1);
      apply();
    }

    function openMenu(open) {
      if (!menu || !toggle) return;
      menu.hidden = !open;
      toggle.setAttribute("aria-expanded", open ? "true" : "false");
    }

    var debounce;
    input.addEventListener("input", function () {
      window.clearTimeout(debounce);
      debounce = window.setTimeout(apply, 90);
    });
    input.addEventListener("keydown", function (e) {
      if (e.key === "Escape") {
        input.value = "";
        apply();
      }
    });

    if (clearBtn) {
      clearBtn.addEventListener("click", function () {
        input.value = "";
        input.focus();
        apply();
      });
    }

    if (toggle) {
      toggle.addEventListener("click", function (e) {
        e.stopPropagation();
        openMenu(menu.hidden);
      });
    }
    boxes.forEach(function (box) {
      box.addEventListener("change", function () {
        toggleFacet(box.value);
      });
    });
    if (resetBtn) {
      resetBtn.addEventListener("click", function () {
        selected = [];
        input.value = "";
        apply();
      });
    }
    if (menu) {
      menu.addEventListener("click", function (e) {
        e.stopPropagation();
      });
    }
    document.addEventListener("click", function () {
      openMenu(false);
    });
    document.addEventListener("keydown", function (e) {
      if (e.key === "Escape") openMenu(false);
    });

    // One delegated listener on the grid covers the "+n" pills and, when
    // enabled, the tag pills themselves. Each card is wrapped in an <a> to the
    // project page, so both have to stop the click reaching that link.
    grid.addEventListener("click", function (e) {
      var more = e.target.closest ? e.target.closest(".pt-more") : null;
      if (more) {
        e.preventDefault();
        e.stopPropagation();
        var row = more.closest(".proj-tags");
        if (row) row.classList.add("is-expanded");
        return;
      }
      if (!clickable) return;
      var pill = e.target.closest ? e.target.closest(".card .proj-tag[data-pf-tag]") : null;
      if (!pill) return;
      e.preventDefault();
      e.stopPropagation();
      toggleFacet(pill.getAttribute("data-pf-tag"));
    });

    bar.classList.add("is-ready");
    apply();
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }
})();
