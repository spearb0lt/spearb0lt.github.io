---
layout: page
title: Face Liveliness Detection
description: A lightweight, fast anti-spoofing model that tells real faces from fake images and videos.
img: assets/img/project/face-liveliness.jpg
importance: 2
category: cv
tags: [cv, security, anti-spoofing, deep-learning, real-time, opencv]
---

{% assign pt = site.data.project_tags %}{% assign all_families = 'domain,method,stack,meta' | split: ',' %}{% assign fams = pt.families_on.project_pages | default: all_families %}{% if pt.enabled and pt.show_on.project_pages and page.tags %}<div class="proj-tags proj-tags-page pt-style-{{ pt.style.project_pages | default: 'soft' }}">{% for t in page.tags %}{% assign fam = pt.map[t] | default: pt.default_family %}{% if fams contains fam %}<span class="proj-tag pt-{{ fam }} pt-tag-{{ t | slugify }}">{{ t }}</span>{% endif %}{% endfor %}</div>{% endif %}

**Links:** [GitHub repository](https://github.com/spearb0lt/Face-Liveliness-Detection-Using-DL)

A deep learning model for face liveliness detection that distinguishes between real and fake (spoofed) faces, intended to harden face-recognition and other security systems against presentation attacks such as a photo or video held up to the camera.

## Highlights

- **Lightweight and fast**, with a detection speed of about 30ms, which makes it practical for real-time use in security pipelines.
- Ships as a complete, reproducible pipeline rather than just a model:
  - `gather_examples.py` extracts face crops from video streams to build a real-versus-fake dataset.
  - `livenessnet.py` defines the compact convolutional network used for classification.
  - `liveness_demo.py` runs the trained model live on a webcam feed.
- Uses an OpenCV deep-learning face detector (a Caffe model) to localise faces before the liveness classifier decides whether each detected face is genuine.
