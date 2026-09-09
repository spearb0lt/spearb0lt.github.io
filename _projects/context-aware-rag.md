---
layout: page
title: Context-Aware Multimodal Knowledge Retrieval
description: A fully multimodal RAG pipeline for PDFs that retrieves across text, tables, figures and formulas with cited answers.
img: assets/img/project/context-aware-rag.jpg
importance: 1
category: nlp
tags: [nlp, rag, multimodal, document-ai, clip, gemini]
---

{% assign pt = site.data.project_tags %}{% assign all_families = 'domain,method,stack,meta' | split: ',' %}{% assign fams = pt.families_on.project_pages | default: all_families %}{% if pt.enabled and pt.show_on.project_pages and page.tags %}<div class="proj-tags proj-tags-page pt-style-{{ pt.style.project_pages | default: 'soft' }}">{% for t in page.tags %}{% assign fam = pt.map[t] | default: pt.default_family %}{% if fams contains fam %}<span class="proj-tag pt-{{ fam }} pt-tag-{{ t | slugify }}">{{ t }}</span>{% endif %}{% endfor %}</div>{% endif %}

**Links:** [GitHub repository](https://github.com/spearb0lt/Context-Aware-Multimodal-Knowledge-Retrieval-System)

A production-grade, fully multimodal Retrieval-Augmented Generation (RAG) pipeline that turns any PDF into a queryable knowledge base. Unlike traditional RAG systems that only handle text, it processes and retrieves from text passages, tables, figures, formulas and form fields at the same time, and grounds every answer in the source document.

## How it works

The document is parsed with Docling (IBM's PDF parser) into its constituent elements, each of which is preserved in its **original form** in a docstore. Embeddings are used only for retrieval lookup, while the LLM always receives the raw original content (actual table HTML, full text, real image) for answer generation. Three parallel retrieval pipelines run on every query:

- **Pipeline A (summary-based):** BGE embeddings of LLM-written summaries catch semantic questions such as "what is the main contribution?".
- **Pipeline B (raw-atomic):** BGE embeddings of the raw content catch exact-value questions such as "what is the BLEU score for the base model?", matching the underlying table directly.
- **Pipeline C (CLIP visual):** CLIP text-to-image similarity catches visual questions such as "the transformer architecture diagram", retrieving the most relevant figure.

Summaries are produced by Groq LLaMA 3.3 70B for text and tables and by Gemini 2.5 Flash vision for images, embedded with BGE-base-en-v1.5.

Two stages sharpen what those pipelines return. **HyDE** (hypothetical document expansion) has the model draft an answer to the question first and searches with that instead of the raw query, which closes the vocabulary gap between how a question is asked and how a paper phrases the answer. A **cross-encoder reranker** (`ms-marco-MiniLM-L-6-v2`) then rescores the retrieved candidates by reading each one against the query jointly, rather than trusting the independent vector similarities that surfaced them.

The result sets are merged and deduplicated, and Gemini generates a comprehensive, source-cited answer that references text, table data and image insights together.
