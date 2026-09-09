---
layout: page
title: BidRAG
description: Open-source RAG extraction for bidding and tender documents, running locally end to end with citations back to the source page.
img: assets/img/project/bidrag.jpg
importance: 2
category: nlp
tags: [nlp, rag, document-ai, self-hosted, docling, pgvector, fastapi, angular]
---

{% assign pt = site.data.project_tags %}{% assign all_families = 'domain,method,stack,meta' | split: ',' %}{% assign fams = pt.families_on.project_pages | default: all_families %}{% if pt.enabled and pt.show_on.project_pages and page.tags %}<div class="proj-tags proj-tags-page pt-style-{{ pt.style.project_pages | default: 'soft' }}">{% for t in page.tags %}{% assign fam = pt.map[t] | default: pt.default_family %}{% if fams contains fam %}<span class="proj-tag pt-{{ fam }} pt-tag-{{ t | slugify }}">{{ t }}</span>{% endif %}{% endfor %}</div>{% endif %}

**Links:** [GitHub repository](https://github.com/spearb0lt/BidRAG)

Upload an RFQ, tender or contract. BidRAG parses its layout, tables and signatures, embeds it into a vector store, and answers a configurable list of commercial and technical questions (rated voltage, busbar current, panel counts, delivery schedule), with each answer traceable back to the page it came from.

**Everything runs locally and free except the language model.** Layout analysis, OCR, embeddings, the vector store, file storage, authentication and email all work with no account and no bill. You bring one API key, or none at all if you run a model with Ollama.

BidRAG is an open-source reimplementation of **Bidify**, the internal application I worked on during my internship at Siemens ([write-up](https://blogs.sw.siemens.com/energy-utilities/2025/04/30/accelerate-your-energy-business-bid-and-tender-process-efficiency-by-25-using-ai/)). It is built entirely on open-source technology, covers the same feature set, and runs lighter than the closed-source original.

## Swappable at every layer

One environment variable per layer, with a free and offline option as the default everywhere:

- **Language model.** Any OpenAI-compatible endpoint, OpenAI, Gemini, Groq, Hugging Face, Ollama, in-process `transformers`, or AWS Bedrock (the original stack). A separate variable can point query expansion at a cheaper model than answering.
- **Embeddings.** Local `sentence-transformers` (BGE-small by default), Ollama, any hosted `/embeddings` endpoint, or Bedrock Titan.
- **Document extraction.** Docling for local layout analysis, table-structure recognition and OCR, or Amazon Textract, which keeps two genuine advantages: signature detection and per-element confidence.
- **Storage, auth and notifications.** Local disk or S3/MinIO, email-and-password or any OIDC issuer, and none/log/SMTP/webhook.

## Chunking and retrieval as configuration

RAG quality is mostly decided by two choices, how a document is cut up and how passages are found again, so both are switchable in a config file with no code change. Chunking runs layout-aware (boundaries follow the document's own headings), recursive, or semantic; retrieval runs dense, BM25, hybrid RRF, cross-encoder rerank, HyDE, or HyDE plus rerank.

Tables, images, signatures and form groups stay **atomic** under every chunking strategy, because splitting a rate table by character count destroys it. Only narrative text is affected.

## Keeping extraction swappable

The chunking pipeline is around 2,700 lines written against Amazon Textract's block graph, and rewriting it for a second backend would have meant re-tuning extraction quality from scratch. So it was not rewritten: **every backend emits the same block graph.** Textract's output passes through untouched, and Docling's document model is translated into that shape at the boundary, so downstream code cannot tell the difference.

## The stack

An Angular frontend talks to a FastAPI backend over REST and JWT; a separate AI service handles ingestion and answering, with Celery on Redis for background work, a headless LibreOffice service for `.docx` conversion, and Postgres with pgvector (HNSW index over cosine distance) as the store. Every step (cost, ingestion trace, refined queries, the exact prompt, and which chunks an answer actually cited) is visible in Langfuse.
