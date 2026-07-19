---
layout: page
title: Indian Legal RAG
description: A citation-grounded retrieval-augmented chatbot over Indian statutes and case law.
img: assets/img/6.jpg
importance: 4
category: applications
---

**Links:** [GitHub](https://github.com/spearb0lt/Legal-RAG)

A retrieval-augmented generation app over Indian statutes and cases that forces every answer to carry verifiable, paragraph-level citations back to the indexed corpus.

## Motivation and approach

- Built to address a gap surfaced by IL-TUR (ACL 2024): frontier LLMs underperform Indian-domain models on retrieval-heavy Indian legal tasks.
- Pairs an Indian-legal corpus with hybrid retrieval (vector embeddings plus BM25, fused with reciprocal rank fusion) and a synthesis step that refuses to make claims its retrieval did not ground.

## Modes

- **Q&A mode:** ask questions about Indian statutes, cases and doctrines and get cited answers.
- **Case Outcome Prediction mode:** describe a case, find similar past cases and see their verdicts along with an assessment of what to expect.
