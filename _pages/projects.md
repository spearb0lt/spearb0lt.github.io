---
layout: page
title: projects
permalink: /projects/
description: A selection of my research and engineering projects.
nav: true
nav_order: 2.5
display_categories: [nlp, time-series/pdm, agentic-ai/llm, cv, biomedical, data-analytics, optimization/or, open-source/packages, useful-tools]
horizontal: false
---

<!-- pages/projects.md -->

<!--
  The vertical card below is a local copy of al_folio_core's _includes/projects.liquid
  with two additions: the tag row, and the data-pf-* attributes the filter bar reads.
  It is inlined here rather than kept as a local `_includes/projects.liquid` override
  because test/style_contract.js fails the build if the starter owns an `_includes/`
  directory at all.

  Everything about tags and the filter is switched from _data/project_tags.yml:
  `enabled`, `style` (soft/solid/ghost), `max_on_cards`, `show_on.projects` and
  `search.*`. Set `enabled: false` there and this page renders exactly as it did
  before tags existed. Colours and the filter-bar styling live in
  assets/css/main.scss; the filter behaviour in assets/js/projects-filter.js.

  The `horizontal: true` layout still delegates to the gem include, so it renders
  without tags and without the filter bar.
-->

{% assign pt = site.data.project_tags %}
{% assign show_tags = false %}
{% if pt.enabled and pt.show_on.projects %}{% assign show_tags = true %}{% endif %}
{% assign show_search = false %}
{% if show_tags and pt.search.enabled and page.horizontal != true %}{% assign show_search = true %}{% endif %}
{% assign clickable = false %}
{% if show_search and pt.search.clickable_tags %}{% assign clickable = true %}{% endif %}
{% assign tag_style = pt.style.projects | default: 'soft' %}
{% comment %}Fallback list is only used if families_on is deleted from the data file entirely.{% endcomment %}
{% assign all_families = 'domain,method,stack,meta' | split: ',' %}
{% assign card_families = pt.families_on.projects | default: all_families %}
{% if pt.max_on_cards and pt.max_on_cards > 0 %}{% assign cap = pt.max_on_cards %}{% else %}{% assign cap = 9999 %}{% endif %}
{% assign filter_by = pt.search.filter_by | default: 'tags' %}
{% assign filter_mode = pt.search.filter_mode | default: 'any' %}
{% assign mono = pt.monochrome.enabled %}
{% comment %}Options for the Filter dropdown: either every section category, or every tag a card is allowed to show.{% endcomment %}
{% if filter_by == 'categories' %}
{% assign filter_options = site.projects | map: 'category' | uniq | sort %}
{% else %}
{% capture facet_csv %}{% for p in site.projects %}{% for t in p.tags %}{% assign fam = pt.map[t] | default: pt.default_family %}{% if card_families contains fam %}{{ t }},{% endif %}{% endfor %}{% endfor %}{% endcapture %}
{% assign filter_options = facet_csv | split: ',' | uniq | sort %}
{% endif %}

{% comment %}One loop covers both modes: a real category list, or one synthetic pass over every project.{% endcomment %}
{% if site.enable_project_categories and page.display_categories %}
{% assign groups = page.display_categories %}
{% else %}
{% assign groups = '__all__' | split: ',' %}
{% endif %}

{% if show_search %}

<div class="pf-anchor"><div class="projects-filter" data-pf-filter-by="{{ filter_by }}" data-pf-filter-mode="{{ filter_mode }}">
  <div class="pf-row">
    <span class="pf-input-wrap"><input type="text" class="pf-input" autocomplete="off" spellcheck="false" aria-label="Search projects" placeholder="{{ pt.search.placeholder | default: 'Search' | escape }}"><button type="button" class="pf-clear" aria-label="Clear search">&times;</button></span>
    <span class="pf-facet">
      <button type="button" class="pf-toggle" aria-expanded="false" aria-haspopup="true">{% if filter_by == 'categories' %}Categories{% else %}Filter{% endif %}<span class="pf-badge" hidden></span><span class="pf-caret" aria-hidden="true"></span></button>
      <span class="pf-menu" hidden>
        <span class="pf-menu-list">{% for opt in filter_options %}<label class="pf-opt"><input type="checkbox" value="{{ opt | escape }}">{{ opt }}</label>{% endfor %}</span>
        <span class="pf-menu-foot"><span class="pf-count"></span><button type="button" class="pf-reset">clear</button></span>
      </span>
    </span>
  </div>
</div></div>
{% endif %}

{% comment %}
pt-mono wraps the chips AND the grid together: the active-filter chips in
.pf-active are clones of the pills on cards inside .projects, and both need
to pick up the same override for monochrome mode to look consistent.
{% endcomment %}

<div class="pf-scope{% if mono %} pt-mono{% endif %}">
{% if show_search %}<div class="pf-active" aria-live="polite"></div>{% endif %}

<div class="projects{% if clickable %} pf-clickable{% endif %}">
{% for category in groups %}
  {% if category == '__all__' %}
    {% assign sorted_projects = site.projects | sort: "importance" %}
  {% else %}
    {% assign sorted_projects = site.projects | where: "category", category | sort: "importance" %}
  {% endif %}
  <div data-pf-section>
    {% unless category == '__all__' %}
      <a id="{{ category }}" href=".#{{ category }}">
        <h2 class="category">{{ category }}</h2>
      </a>
    {% endunless %}
    {% if page.horizontal %}
      <div class="container">
        <div class="row row-cols-1 row-cols-md-2">
          {% for project in sorted_projects %}
            {% include projects_horizontal.liquid %}
          {% endfor %}
        </div>
      </div>
    {% else %}
      <div class="row row-cols-1 row-cols-md-3">
        {% for project in sorted_projects %}
          {% capture pf_text %}{{ project.title }} {{ project.description }} {{ project.category }} {{ project.tags | join: ' ' }}{% endcapture %}
          <div class="col" data-pf-text="{{ pf_text | strip_newlines | escape }}" data-pf-tags="{{ project.tags | join: '|' | escape }}" data-pf-cat="{{ project.category | escape }}">
            <a href="{% if project.redirect %}{{ project.redirect }}{% else %}{{ project.url | relative_url }}{% endif %}">
              <div class="card h-100 hoverable">
                {% if project.img %}
                  {% include figure.liquid loading="eager" path=project.img sizes="250px" alt="project thumbnail" class="card-img-top" %}
                {% endif %}
                <div class="card-body">
                  <h2 class="card-title">{{ project.title }}</h2>
                  <p class="card-text">{{ project.description }}</p>
                  {% comment %}Keep only the families families_on.projects allows, then cap what is left.{% endcomment %}
                  {% capture card_tags_csv %}{% for t in project.tags %}{% assign fam = pt.map[t] | default: pt.default_family %}{% if card_families contains fam %}{{ t }},{% endif %}{% endfor %}{% endcapture %}
                  {% assign card_tags = card_tags_csv | split: ',' %}
                  {% if show_tags and card_tags.size > 0 %}
                    <div class="proj-tags pt-style-{{ tag_style }}">
                      {% for t in card_tags %}
                        {% assign fam = pt.map[t] | default: pt.default_family %}
                        <span class="proj-tag pt-{{ fam }} pt-tag-{{ t | slugify }}{% if forloop.index0 >= cap %} pt-overflow{% endif %}" data-pf-tag="{{ t | escape }}">{{ t }}</span>
                      {% endfor %}
                      {% assign extra = card_tags.size | minus: cap %}
                      {% if extra > 0 %}
                        <span class="proj-tag pt-more" role="button" tabindex="0" aria-label="Show {{ extra }} more tags">+{{ extra }}</span>
                      {% endif %}
                    </div>
                  {% endif %}
                </div>
              </div>
            </a>
          </div>
        {% endfor %}
      </div>
    {% endif %}
  </div>
{% endfor %}
{% if show_search %}<div class="pf-empty">No projects match that search.</div>{% endif %}
</div>
</div>

{% if show_search %}<script defer src="{{ '/assets/js/projects-filter.js' | relative_url | bust_file_cache }}"></script>{% endif %}
