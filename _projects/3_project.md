---
layout: page
title: Context-Aware Multimodal Knowledge Retrieval
description: A multimodal RAG system that parses, summarises and retrieves images, tables, equations and text with source-cited answers.
img: assets/img/1.jpg
importance: 3
category: work
---

A context-aware retrieval system that understands documents the way a person does, treating images, tables, equations, graphs and text as distinct modalities rather than flattening everything into plain text.

## How it works

- Built a context-aware parser that automatically extracts and separately processes multimodal content, summarising each modality into vector embeddings.
- Employed modality-specific pipelines and selected the most appropriate LLM per content type to improve summary quality, storing embeddings and summaries in ChromaDB using Hugging Face embeddings.
- Designed a multi-vector retrieval strategy that links document summaries back to their original content for better context preservation.

## Results

On a query, the system retrieves the relevant multimodal content and generates comprehensive, source-cited answers that reference text, table data and image insights together.
