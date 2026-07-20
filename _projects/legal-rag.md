---
layout: page
title: Indian Legal RAG
description: A citation-grounded retrieval-augmented chatbot over Indian statutes and case law.
img: assets/img/project/legal-rag.jpg
importance: 2
category: nlp
---

**Links:** [GitHub repository](https://github.com/spearb0lt/Legal-RAG)

A retrieval-augmented generation app over Indian statutes and cases that forces **every answer to carry verifiable, paragraph-level citations** back to the indexed corpus. It was built to address a gap surfaced by IL-TUR (ACL 2024): frontier LLMs underperform Indian-domain models on retrieval-heavy Indian legal tasks, so the system pairs a dedicated Indian-legal corpus with disciplined retrieval and a synthesis step that refuses to make claims its retrieval did not ground.

## How it works

- **Hybrid retrieval** combines dense vector embeddings with BM25 keyword search, fused using reciprocal rank fusion (RRF), so the system catches both semantically similar passages and exact statutory language.
- **Grounded synthesis** only asserts what the retrieved passages support, and attaches the citations for each claim.

## Two modes

- **Q&A mode:** ask questions about Indian statutes, cases and doctrines and receive cited answers.
- **Case Outcome Prediction mode:** describe a case, find similar past cases, and see their verdicts along with an assessment of what to expect.
