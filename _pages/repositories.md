---
layout: page
permalink: /repositories/
title: repositories
description: My GitHub profile and a selection of repositories I have been working on.
nav: true
nav_order: 4
---

<style>
  .gh-profile {
    display: flex;
    align-items: center;
    gap: 1rem;
    margin: 1.5rem 0 2rem;
    padding: 1rem 1.2rem;
    border: 1px solid var(--global-divider-color, rgba(0,0,0,.1));
    border-radius: 12px;
    text-decoration: none !important;
    color: inherit;
    max-width: 420px;
    transition: box-shadow .15s ease, transform .15s ease;
  }
  .gh-profile:hover { box-shadow: 0 6px 20px rgba(0,0,0,.12); transform: translateY(-2px); }
  .gh-profile img { width: 64px; height: 64px; border-radius: 50%; }
  .gh-profile .gh-name { font-weight: 600; color: var(--global-theme-color, #b509ac); }
  .gh-profile .gh-sub { font-size: .85rem; color: var(--global-text-color-light, #828282); }

  .repo-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(270px, 1fr));
    gap: 1rem;
    margin: 1.25rem 0 2rem;
  }
  .repo-card {
    display: flex;
    flex-direction: column;
    border: 1px solid var(--global-divider-color, rgba(0,0,0,.1));
    border-radius: 12px;
    padding: 1rem 1.1rem;
    text-decoration: none !important;
    background: var(--global-card-bg-color, #fff);
    transition: box-shadow .15s ease, transform .15s ease;
  }
  .repo-card:hover { box-shadow: 0 6px 20px rgba(0,0,0,.12); transform: translateY(-3px); }
  .repo-card .rc-name { font-weight: 600; color: var(--global-theme-color, #b509ac); word-break: break-word; margin-bottom: .4rem; }
  .repo-card .rc-desc { font-size: .9rem; color: var(--global-text-color, #333); line-height: 1.45; flex-grow: 1; }
  .repo-card .proj-tags { margin-top: .6rem; }
  .repo-card .rc-lang { font-size: .78rem; color: var(--global-text-color-light, #828282); margin-top: .7rem; }
  .repo-card .rc-lang::before { content: "\25CF"; color: var(--global-theme-color, #b509ac); margin-right: .4rem; }
</style>

## GitHub profile

<a class="gh-profile" href="https://github.com/spearb0lt" target="_blank" rel="noopener">
  <img src="https://github.com/spearb0lt.png" alt="spearb0lt avatar" loading="lazy">
  <span>
    <span class="gh-name">@spearb0lt</span><br>
    <span class="gh-sub">View my full profile and all repositories on GitHub</span>
  </span>
</a>

## Repositories

{% assign pt = site.data.project_tags %}
{% assign show_tags = false %}
{% if pt.enabled and pt.show_on.repositories %}{% assign show_tags = true %}{% endif %}
{% assign tag_style = pt.style.repositories | default: 'soft' %}
{% assign all_families = 'domain,method,stack,meta' | split: ',' %}
{% assign card_families = pt.families_on.repositories | default: all_families %}
{% if pt.max_on_cards and pt.max_on_cards > 0 %}{% assign cap = pt.max_on_cards %}{% else %}{% assign cap = 9999 %}{% endif %}

<div class="repo-grid">
  {% for repo in site.data.repositories.repo_cards %}
    <a class="repo-card" href="{{ repo.url }}" target="_blank" rel="noopener">
      <span class="rc-name">{{ repo.name }}</span>
      <span class="rc-desc">{{ repo.desc }}</span>
      {% capture repo_tags_csv %}{% for t in repo.tags %}{% assign fam = pt.map[t] | default: pt.default_family %}{% if card_families contains fam %}{{ t }},{% endif %}{% endfor %}{% endcapture %}
      {% assign repo_tags = repo_tags_csv | split: ',' %}
      {% if show_tags and repo_tags.size > 0 %}
        <span class="proj-tags pt-style-{{ tag_style }}">
          {% for t in repo_tags %}
            {% assign fam = pt.map[t] | default: pt.default_family %}
            <span class="proj-tag pt-{{ fam }} pt-tag-{{ t | slugify }}{% if forloop.index0 >= cap %} pt-overflow{% endif %}">{{ t }}</span>
          {% endfor %}
          {% assign extra = repo_tags.size | minus: cap %}
          {% if extra > 0 %}<span class="proj-tag pt-more">+{{ extra }}</span>{% endif %}
        </span>
      {% endif %}
      {% if repo.lang %}<span class="rc-lang">{{ repo.lang }}</span>{% endif %}
    </a>
  {% endfor %}
</div>

Special mention: [my-codegen-api2](https://github.com/spearb0lt/my-codegen-api2) is powered by my [CodeGen-Hacker-Cup-AI-devkit](https://github.com/spearb0lt/CodeGen-Hacker-Cup-AI-devkit), the toolkit behind my Global Rank 10 finish in the Meta Hacker Cup 2025 (AI Track).
