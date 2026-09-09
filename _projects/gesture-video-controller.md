---
layout: page
title: Gesture Video Controller
description: A webcam hand-tracking system to control video playback and system actions with gestures.
img: assets/img/project/gesture-video-controller.jpg
importance: 3
category: useful-tools
tags: [cv, tools, hci, real-time, mediapipe]
---

{% assign pt = site.data.project_tags %}{% assign all_families = 'domain,method,stack,meta' | split: ',' %}{% assign fams = pt.families_on.project_pages | default: all_families %}{% if pt.enabled and pt.show_on.project_pages and page.tags %}<div class="proj-tags proj-tags-page pt-style-{{ pt.style.project_pages | default: 'soft' }}">{% for t in page.tags %}{% assign fam = pt.map[t] | default: pt.default_family %}{% if fams contains fam %}<span class="proj-tag pt-{{ fam }} pt-tag-{{ t | slugify }}">{{ t }}</span>{% endif %}{% endfor %}</div>{% endif %}

**Links:** [GitHub repository](https://github.com/spearb0lt/Gesture-Video-Controller)

A lightweight hand-tracking control system that lets you drive media, browser and system actions using intuitive hand gestures through your webcam, with no keyboard or remote needed. It supports both single-hand and dual-hand operation.

## Single-hand gestures

A rich gesture vocabulary maps hand poses to actions, for example an open palm for play or pause, a peace sign to rewind, a single index finger to skip forward, different finger counts for volume up and down, a thumb-and-three-finger pose for fullscreen, thumb-only and pinky-only for scrolling, and an index-plus-pinky hold for 2x playback. A gesture must be held steadily for about 0.2 seconds before it triggers, which avoids accidental activations.

## Dual-hand mode

In dual-hand mode each hand is tracked independently and supports its own set of gestures, doubling the available controls for finer, faster interaction.
