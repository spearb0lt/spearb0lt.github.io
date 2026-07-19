---
layout: page
permalink: /repositories/
title: repositories
description: My GitHub profile and a few repositories I have been working on.
nav: true
nav_order: 4
---

{% if site.data.repositories.github_users %}

## GitHub users

<div class="repositories d-flex flex-wrap flex-md-row flex-column justify-content-between align-items-center">
  {% for user in site.data.repositories.github_users %}
    {% include repository/repo_user.liquid username=user %}
  {% endfor %}
</div>

---

{% if site.repo_trophies.enabled %}
{% for user in site.data.repositories.github_users %}
{% if site.data.repositories.github_users.size > 1 %}

  <h4>{{ user }}</h4>
  {% endif %}
  <div class="repositories d-flex flex-wrap flex-md-row flex-column justify-content-between align-items-center">
  {% include repository/repo_trophies.liquid username=user %}
  </div>

---

{% endfor %}
{% endif %}
{% endif %}

{% if site.data.repositories.github_repos %}

## GitHub Repositories

Special mention: [my-codegen-api2](https://github.com/spearb0lt/my-codegen-api2) is powered by my [CodeGen-Hacker-Cup-AI-devkit](https://github.com/spearb0lt/CodeGen-Hacker-Cup-AI-devkit), the toolkit behind my Global Rank 10 finish in the Meta Hacker Cup 2025 (AI Track).

<div class="repositories d-flex flex-wrap flex-md-row flex-column justify-content-between align-items-center">
  {% for repo in site.data.repositories.github_repos %}
    {% include repository/repo.liquid repository=repo %}
  {% endfor %}
</div>

The cards above are rendered live by GitHub's stats service, which is occasionally unavailable. Here is the full list either way:

- [Text-to-Handwriting-converter](https://github.com/spearb0lt/Text-to-Handwriting-converter): converts typed text into realistic handwriting.
- [Consumer-Commission-Complaint-Agent](https://github.com/spearb0lt/Consumer-Commission-Complaint-Agent): AI agent that helps draft and file consumer commission complaints.
- [LitigatAI](https://github.com/spearb0lt/LitigatAI): AI assistant for legal research and litigation support.
- [Legal-RAG](https://github.com/spearb0lt/Legal-RAG): retrieval-augmented generation over legal documents.
- [my-codegen-api2](https://github.com/spearb0lt/my-codegen-api2): code generation API, powered by the [CodeGen-Hacker-Cup-AI-devkit](https://github.com/spearb0lt/CodeGen-Hacker-Cup-AI-devkit).
- [CodeGen-Hacker-Cup-AI-devkit](https://github.com/spearb0lt/CodeGen-Hacker-Cup-AI-devkit): the AI devkit behind my Global Rank 10 finish at Meta Hacker Cup 2025 (AI Track).
- [SENTRAL-Multi-Spectrum-Stock-Analysis](https://github.com/spearb0lt/SENTRAL-Multi-Spectrum-Stock-Analysis): multi-spectrum stock analysis fusing fundamentals, technicals and custom-LLM sentiment.
- [Context-Aware-Multimodal-Knowledge-Retrieval-System](https://github.com/spearb0lt/Context-Aware-Multimodal-Knowledge-Retrieval-System): multimodal RAG over images, tables, equations and text with source-cited answers.
- [Scania](https://github.com/spearb0lt/Scania): privacy-preserving predictive maintenance on the IDA 2024 SCANIA-X dataset.
- [Gesture-Video-Cotroller](https://github.com/spearb0lt/Gesture-Video-Cotroller): gesture-based lightweight video controller for streaming platforms.
- [Lung-Cancer-Detection-Using-DL](https://github.com/spearb0lt/Lung-Cancer-Detection-Using-DL): lung cancer detection using deep learning and soft attention.
- [Face-Liveliness-Detection-Using-DL](https://github.com/spearb0lt/Face-Liveliness-Detection-Using-DL): lightweight, fast face liveliness detection distinguishing real from fake images and videos (about 30ms).
{% endif %}
