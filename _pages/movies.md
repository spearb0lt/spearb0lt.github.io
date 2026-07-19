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
