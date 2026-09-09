---
layout: page
title: Federated Heart Disease Prediction
description: Predicting heart disease from clinical biomarkers using federated learning.
img: assets/img/project/federated_heart_disease.jpg
importance: 3
category: biomedical
tags: [biomedical, federated-learning, privacy, tabular]
---

{% assign pt = site.data.project_tags %}{% assign all_families = 'domain,method,stack,meta' | split: ',' %}{% assign fams = pt.families_on.project_pages | default: all_families %}{% if pt.enabled and pt.show_on.project_pages and page.tags %}<div class="proj-tags proj-tags-page pt-style-{{ pt.style.project_pages | default: 'soft' }}">{% for t in page.tags %}{% assign fam = pt.map[t] | default: pt.default_family %}{% if fams contains fam %}<span class="proj-tag pt-{{ fam }} pt-tag-{{ t | slugify }}">{{ t }}</span>{% endif %}{% endfor %}</div>{% endif %}

**Links:** [GitHub repository](https://github.com/spearb0lt/Heart-Disease-Prediction-with-Biomarkers-using-Federated-Learning)

A federated learning study that predicts heart disease from clinical biomarkers without ever centralising patient records, so hospitals or clinics could collaborate on a shared model while keeping their data local.

## Details

- Trains on a dataset of **918 subjects with 11 clinical features**, including age, sex, chest pain type, resting blood pressure, cholesterol, fasting blood sugar, resting ECG, maximum heart rate, exercise-induced angina, oldpeak and ST slope, predicting the presence of heart disease.
- Uses a federated setup where each client trains locally and only model updates are shared and aggregated into a global model, preserving the privacy of sensitive medical data.
- Sits alongside my other federated-learning work as an exploration of privacy-preserving machine learning applied to healthcare biomarkers.
