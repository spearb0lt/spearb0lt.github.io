---
layout: book-shelf
title: bookshelf
permalink: /books/
published: false # set to true (or remove this line) to bring the page back
nav: true
collection: books
---

> What an astonishing thing a book is. It's a flat object made from a tree with flexible parts on which are imprinted lots of funny dark squiggles. But one glance at it and you're inside the mind of another person, maybe somebody dead for thousands of years. Across the millennia, an author is speaking clearly and silently inside your head, directly to you. Writing is perhaps the greatest of human inventions, binding together people who never knew each other, citizens of distant epochs. Books break the shackles of time. A book is proof that humans are capable of working magic.
>
> -- Carl Sagan, Cosmos, Part 11: The Persistence of Memory (1980)

## Books that I am reading, have read, or will read

<div id="book-suggest-wrap">
<style>
  .suggest-form {
    max-width: 380px;
    margin: 1.5rem 0 1rem;
    padding: 0.9rem 1rem;
    border: 1px solid var(--global-divider-color, rgba(0, 0, 0, 0.1));
    border-radius: 10px;
    background: var(--global-card-bg-color, #fff);
  }
  .suggest-form label { display: block; font-size: 0.76rem; font-weight: 600; margin: 0.5rem 0 0.2rem; }
  .suggest-form input[type="text"], .suggest-form input[type="url"] {
    width: 100%;
    box-sizing: border-box;
    padding: 0.4rem 0.55rem;
    border: 1px solid var(--global-divider-color, rgba(0, 0, 0, 0.15));
    border-radius: 7px;
    background: var(--global-bg-color, #fff);
    color: var(--global-text-color, #111);
    font-size: 0.85rem;
  }
  .suggest-form button {
    margin-top: 0.85rem;
    padding: 0.4rem 0.95rem;
    border: none;
    border-radius: 7px;
    background: var(--global-theme-color, #b509ac);
    color: #fff;
    font-weight: 600;
    font-size: 0.85rem;
    cursor: pointer;
  }
  .suggest-form button:hover { opacity: 0.9; }
  .suggest-form .sf-result { margin: 0.7rem 0 0; font-size: 0.82rem; min-height: 1.2em; }
  .suggest-form .sf-hp { position: absolute; left: -9999px; }

  .suggest-divider { border: none; border-top: 1px solid var(--global-divider-color, rgba(0, 0, 0, 0.1)); margin: 3.5rem 0 1.5rem; }
  .suggest-details { margin: 0 0 2.5rem; }
  .suggest-details > summary {
    display: inline-block;
    cursor: pointer;
    list-style: none;
    padding: 0.45rem 1rem;
    border: 1px solid var(--global-theme-color, #b509ac);
    border-radius: 8px;
    color: var(--global-theme-color, #b509ac);
    font-weight: 600;
    font-size: 0.88rem;
    user-select: none;
  }
  .suggest-details > summary::-webkit-details-marker { display: none; }
  .suggest-details > summary::before { content: "\2709\FE0E  "; }
  .suggest-details > summary:hover { background: var(--global-theme-color, #b509ac); color: #fff; }
  .suggest-details[open] > summary { margin-bottom: 0.2rem; }
  .suggest-intro { font-size: 0.9rem; margin: 0.4rem 0 0; }
  .suggest-details .suggest-form { margin-top: 0.5rem; }
</style>

<hr class="suggest-divider">

<details class="suggest-details">
<summary>Suggest me books to read</summary>
<p class="suggest-intro">Read something great? Recommend it and I might add it to the shelf.</p>

<form id="book-suggest" class="suggest-form">
  <input type="hidden" name="access_key" value="3800b398-13c6-478e-8f80-4ba6a73373ff">
  <input type="hidden" name="subject" value="New book suggestion from your portfolio">
  <input type="hidden" name="from_name" value="Portfolio bookshelf page">
  <input type="checkbox" name="botcheck" class="sf-hp" tabindex="-1" autocomplete="off">

  <label for="bs-book">Book title *</label>
  <input id="bs-book" type="text" name="book" required placeholder="e.g. Deep Learning">

  <label for="bs-author">Author (optional)</label>
  <input id="bs-author" type="text" name="author" placeholder="e.g. Ian Goodfellow">

  <label for="bs-why">Why should I read it? (optional)</label>
  <input id="bs-why" type="text" name="why" placeholder="A line on what makes it worth reading">

  <label for="bs-pdf">Link to a PDF (optional)</label>
  <input id="bs-pdf" type="url" name="pdf_link" placeholder="https://...">

  <label for="bs-buy">Link to buy (optional)</label>
  <input id="bs-buy" type="url" name="buy_link" placeholder="https://...">

  <label for="bs-from">Your name (optional)</label>
  <input id="bs-from" type="text" name="from" placeholder="So I know who to thank">

  <button type="submit">Send suggestion</button>
  <p class="sf-result" role="status" aria-live="polite"></p>
</form>
</details>

<script>
  (function () {
    function moveToEnd() {
      var wrap = document.getElementById("book-suggest-wrap");
      // move the suggestion box below the book grid (the layout renders it above by default)
      if (wrap && wrap.parentNode) wrap.parentNode.appendChild(wrap);
    }
    if (document.readyState === "loading") {
      document.addEventListener("DOMContentLoaded", moveToEnd);
    } else {
      moveToEnd();
    }
    var f = document.getElementById("book-suggest");
    if (!f) return;
    var res = f.querySelector(".sf-result");
    f.addEventListener("submit", function (e) {
      e.preventDefault();
      res.textContent = "Sending...";
      fetch("https://api.web3forms.com/submit", {
        method: "POST",
        body: new FormData(f),
        headers: { Accept: "application/json" }
      })
        .then(function (r) { return r.json(); })
        .then(function (j) {
          if (j.success) { res.textContent = "Thanks! Your suggestion was sent."; f.reset(); }
          else { res.textContent = "Something went wrong. Please try again."; }
        })
        .catch(function () { res.textContent = "Network error. Please try again."; });
    });
  })();
</script>
</div>
