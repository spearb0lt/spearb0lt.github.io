---
layout: page
title: reads
permalink: /reads/
# nav: true
published: false # set to true (or remove this line) to bring the page back
nav: false
nav_order: 5
description: Blogs, papers, posts and other things I have read and found interesting, with my own notes.
---

<style>
  .read-card {
    border: 1px solid var(--global-divider-color, rgba(0, 0, 0, 0.1));
    border-radius: 12px;
    padding: 1rem 1.2rem;
    margin: 0.9rem 0;
    background: var(--global-card-bg-color, #fff);
  }
  .read-meta { display: flex; align-items: center; gap: 0.6rem; margin-bottom: 0.35rem; }
  .read-type {
    font-size: 0.7rem;
    font-weight: 700;
    letter-spacing: 0.03em;
    text-transform: uppercase;
    color: #fff;
    background: var(--global-theme-color, #b509ac);
    padding: 0.12rem 0.5rem;
    border-radius: 999px;
  }
  .read-date { font-size: 0.78rem; color: var(--global-text-color-light, #828282); }
  .read-title {
    font-size: 1.05rem;
    font-weight: 600;
    color: var(--global-theme-color, #b509ac);
    text-decoration: none !important;
  }
  .read-title:hover { text-decoration: underline !important; }
  .read-source { font-size: 0.82rem; color: var(--global-text-color-light, #828282); margin-top: 0.15rem; }
  .read-note { font-size: 0.92rem; line-height: 1.5; margin: 0.6rem 0 0; }

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

A running collection of blogs, papers, posts and other things I have read and found worth keeping, along with my own notes on each.

{% for it in site.data.reads.items %}
<div class="read-card">
  <div class="read-meta">
    {% if it.type %}<span class="read-type">{{ it.type }}</span>{% endif %}
    {% if it.date %}<span class="read-date">{{ it.date }}</span>{% endif %}
  </div>
  <a class="read-title" href="{{ it.url }}" target="_blank" rel="noopener">{{ it.title }}</a>
  {% if it.source %}<div class="read-source">{{ it.source }}</div>{% endif %}
  {% if it.note %}<p class="read-note">{{ it.note | markdownify }}</p>{% endif %}
</div>
{% endfor %}

<hr class="suggest-divider">

<details class="suggest-details">
<summary>Have something I should read?</summary>
<p class="suggest-intro">Come across a great blog, paper or post? Send it over and I might add it here.</p>

<form id="read-suggest" class="suggest-form">
  <input type="hidden" name="access_key" value="3800b398-13c6-478e-8f80-4ba6a73373ff">
  <input type="hidden" name="subject" value="New read suggestion from your portfolio">
  <input type="hidden" name="from_name" value="Portfolio reads page">
  <input type="checkbox" name="botcheck" class="sf-hp" tabindex="-1" autocomplete="off">

  <label for="rs-title">Title or link *</label>
  <input id="rs-title" type="text" name="item" required placeholder="e.g. a blog, paper or post">

  <label for="rs-link">Link (optional)</label>
  <input id="rs-link" type="url" name="link" placeholder="https://...">

  <label for="rs-type">Type (optional)</label>
  <input id="rs-type" type="text" name="type" list="rs-type-list" placeholder="e.g. Paper, Blog, Post">
  <datalist id="rs-type-list">
    <option value="Paper"></option>
    <option value="Blog"></option>
    <option value="Post"></option>
    <option value="Video"></option>
    <option value="Article"></option>
  </datalist>

  <label for="rs-why">Why is it worth reading? (optional)</label>
  <input id="rs-why" type="text" name="why" placeholder="A line on what makes it interesting">

  <label for="rs-from">Your name (optional)</label>
  <input id="rs-from" type="text" name="from" placeholder="So I know who to thank">

  <button type="submit">Send suggestion</button>
  <p class="sf-result" role="status" aria-live="polite"></p>
</form>
</details>

<script>
  (function () {
    var f = document.getElementById("read-suggest");
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
