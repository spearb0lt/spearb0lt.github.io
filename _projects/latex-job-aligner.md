---
layout: page
title: Job-Aligner
description: A tool to tailor a LaTeX resume to any job description and compile a submission-ready PDF.
img: assets/img/project/latex-job-aligner.jpg
importance: 1
category: useful-tools
tags: [tools, llms, automation, latex, chrome-extension]
---

{% assign pt = site.data.project_tags %}{% assign all_families = 'domain,method,stack,meta' | split: ',' %}{% assign fams = pt.families_on.project_pages | default: all_families %}{% if pt.enabled and pt.show_on.project_pages and page.tags %}<div class="proj-tags proj-tags-page pt-style-{{ pt.style.project_pages | default: 'soft' }}">{% for t in page.tags %}{% assign fam = pt.map[t] | default: pt.default_family %}{% if fams contains fam %}<span class="proj-tag pt-{{ fam }} pt-tag-{{ t | slugify }}">{{ t }}</span>{% endif %}{% endfor %}</div>{% endif %}

**Links:** [GitHub repository](https://github.com/spearb0lt/Job-Aligner-Latex-to-PDF-Generator)

A local web app, also usable as a Chrome extension, that lets you tailor every section of your LaTeX resume for a specific job and compile straight to a submission-ready PDF, using the **exact same fonts and layout** as your original resume. It removes the usual pain of manually commenting LaTeX in and out for each application.

## Features

- **Toggle anything** with checkboxes across all six sections (Education, Skills, Experience, Projects, Publications, Achievements). Skills toggle per individual skill, and Experience and Projects toggle both per entry and per bullet.
- **Bring back commented-out content:** each section surfaces the entries you previously commented out of your LaTeX, so you can re-enable an old project or extra skill with a single tick.
- **Rich editing:** add new entries with rich-text formatting and drag to reorder them.
- **Optional LLM assist:** paste a job description and let an LLM pre-select the most relevant content for that role.
- **Safe by design:** your original `base.tex` is never modified; all output is written to a separate folder, so you can regenerate freely.
