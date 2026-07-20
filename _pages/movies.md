---
layout: page
title: movies
permalink: /movies/
description: Some of the movies and shows I have watched and loved, grouped by genre. Hover a poster for the title, click to open its IMDb page.
nav: false
---

<style>
  .movie-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(140px, 1fr));
    gap: 1rem;
    margin: 1rem 0 2.5rem;
  }
  .movie {
    position: relative;
    display: block;
    aspect-ratio: 2 / 3;
    border-radius: 10px;
    overflow: hidden;
    box-shadow: 0 3px 12px rgba(0, 0, 0, 0.18);
    text-decoration: none !important;
  }
  .movie img {
    width: 100%;
    height: 100%;
    object-fit: cover;
    display: block;
    transition: transform 0.35s ease;
  }
  .movie:hover img { transform: scale(1.07); }
  .movie .movie-title {
    position: absolute;
    left: 0;
    right: 0;
    bottom: 0;
    padding: 2.2rem 0.6rem 0.6rem;
    background: linear-gradient(transparent, rgba(0, 0, 0, 0.88));
    color: #fff;
    font-size: 0.85rem;
    line-height: 1.25;
    opacity: 0;
    transition: opacity 0.25s ease;
  }
  .movie:hover .movie-title,
  .movie:focus .movie-title { opacity: 1; }
</style>

{% for genre in site.data.movies.genres %}

## {{ genre.name }}

<div class="movie-grid">
  {% for m in genre.movies %}
  <a class="movie" href="{{ m.imdb }}" title="{{ m.title }}" target="_blank" rel="noopener">
    <img src="{{ m.poster | relative_url }}" alt="{{ m.title }} poster" loading="lazy">
    <span class="movie-title">{{ m.title }}</span>
  </a>
  {% endfor %}
</div>

{% endfor %}

<style>
  .movie-suggest {
    max-width: 340px;
    margin: 1rem 0 2rem;
    padding: 0.9rem 1rem;
    border: 1px solid var(--global-divider-color, rgba(0, 0, 0, 0.1));
    border-radius: 10px;
    background: var(--global-card-bg-color, #fff);
  }
  .movie-suggest label { display: block; font-size: 0.76rem; font-weight: 600; margin: 0.5rem 0 0.2rem; }
  .movie-suggest input[type="text"] {
    width: 100%;
    box-sizing: border-box;
    padding: 0.4rem 0.55rem;
    border: 1px solid var(--global-divider-color, rgba(0, 0, 0, 0.15));
    border-radius: 7px;
    background: var(--global-bg-color, #fff);
    color: var(--global-text-color, #111);
    font-size: 0.85rem;
  }
  .movie-suggest button {
    margin-top: 0.8rem;
    padding: 0.4rem 0.95rem;
    border: none;
    border-radius: 7px;
    background: var(--global-theme-color, #b509ac);
    color: #fff;
    font-weight: 600;
    font-size: 0.85rem;
    cursor: pointer;
  }
  .movie-suggest button:hover { opacity: 0.9; }
  .movie-suggest .ms-result { margin: 0.7rem 0 0; font-size: 0.82rem; min-height: 1.2em; }
  .movie-suggest .ms-hp { position: absolute; left: -9999px; }

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
  .suggest-details .movie-suggest, .suggest-details .suggest-form { margin-top: 0.5rem; }
</style>

<hr class="suggest-divider">

<details class="suggest-details">
<summary>Have good recommmendation?</summary>
<p class="suggest-intro">Seen something you think I should watch? Send it my way and it might end up on this page.</p>

<form id="movie-suggest" class="movie-suggest">
  <!-- Get a free access key at https://web3forms.com (enter your email, it is emailed to you),
       then replace the placeholder below. Suggestions are emailed to that address. -->
  <input type="hidden" name="access_key" value="3800b398-13c6-478e-8f80-4ba6a73373ff">
  <input type="hidden" name="subject" value="New movie suggestion from your portfolio">
  <input type="hidden" name="from_name" value="Portfolio movies page">
  <input type="checkbox" name="botcheck" class="ms-hp" tabindex="-1" autocomplete="off">

  <label for="ms-movie">Movie or show *</label>
  <input id="ms-movie" type="text" name="movie" required placeholder="e.g. Whiplash">

  <label for="ms-category">Category (optional)</label>
  <input id="ms-category" type="text" name="category" list="ms-genre-list" placeholder="e.g. Thriller">
  <datalist id="ms-genre-list">
    {% for genre in site.data.movies.genres %}<option value="{{ genre.name }}"></option>{% endfor %}
  </datalist>

  <label for="ms-from">Your name (optional)</label>
  <input id="ms-from" type="text" name="from" placeholder="So I know who to thank">

  <button type="submit">Send suggestion</button>
  <p class="ms-result" role="status" aria-live="polite"></p>
</form>
</details>

<script>
  (function () {
    var f = document.getElementById("movie-suggest");
    if (!f) return;
    var res = f.querySelector(".ms-result");
    f.addEventListener("submit", function (e) {
      e.preventDefault();
      if (f.access_key.value.indexOf("YOUR_WEB3FORMS") === 0) {
        res.textContent = "The suggestion form is not configured yet.";
        return;
      }
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
