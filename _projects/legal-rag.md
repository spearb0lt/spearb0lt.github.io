---
layout: page
title: Indian Legal RAG
description: Citation-grounded research over Indian statutes and judgments, where every citation is verified against the passage it names before the answer is shown.
img: assets/img/project/legal-rag.jpg
importance: 3
category: nlp
tags: [nlp, legal-tech, rag, hybrid-search, bm25, on-device, fastapi, hackathon]
---

{% assign pt = site.data.project_tags %}{% assign all_families = 'domain,method,stack,meta' | split: ',' %}{% assign fams = pt.families_on.project_pages | default: all_families %}{% if pt.enabled and pt.show_on.project_pages and page.tags %}<div class="proj-tags proj-tags-page pt-style-{{ pt.style.project_pages | default: 'soft' }}">{% for t in page.tags %}{% assign fam = pt.map[t] | default: pt.default_family %}{% if fams contains fam %}<span class="proj-tag pt-{{ fam }} pt-tag-{{ t | slugify }}">{{ t }}</span>{% endif %}{% endfor %}</div>{% endif %}

**Links:** [GitHub repository](https://github.com/spearb0lt/Legal-RAG) and [demo walkthrough](https://github.com/spearb0lt/Legal-RAG#demo) (5m 28s, captioned)

**Nyaya** is citation-grounded research over a corpus of Indian statutes and judgments, built for the ILTN Vibeathon. Ask a question and it searches 19,144 passages drawn from 1,411 documents, answers only from what it found, and tags every claim with the paragraph behind it. When the corpus does not hold the answer, the app says so instead of filling the gap from memory.

## Four modes

- **Research.** A question goes through a router that rewrites it for retrieval, then hybrid search over dense vectors and BM25, then synthesis constrained to the retrieved passages. Every `[S#]` tag in the answer is clickable and scrolls to the exact paragraph, with the quoted span highlighted inside it.
- **Outcomes.** Describe a matter and it finds the closest cases in a labelled corpus of Indian decisions, reports how each was actually decided, and explains what separates the two groups. It reports a pattern in past cases rather than predicting a result, and the interface says so on every report.
- **Your own documents.** Upload a contract, a notice or a judgment. It is chunked and embedded in memory for the session and searched alongside the corpus, so an answer can cite your clause and a statute in the same breath. Nothing is written to disk.
- **Search.** Raw retrieval with no model in the loop, showing the dense and keyword rank of every hit. Free, needs no key, and answers in about 20 ms.

## How the answer is kept honest

Retrieval-augmented generation usually stops at putting sources in the prompt and trusting the output. Three things here go further.

**Citations are verified, not assumed.** The model must return the `chunk_id` of the passage behind each claim. Each one is checked against the passages actually retrieved, and the quote is matched against that passage's text. A citation naming a passage that was never retrieved, or quoting words that are not in it, is marked unverified and the answer header reports how many failed.

**A wrong guess cannot hide a source.** The router suggests document types, but that suggestion only nudges ranking and never filters. This mattered in practice: asking whether privacy is a fundamental right reads as a concept question, the router restricted retrieval to statutes, and that dropped _Puttaswamy_, the judgment that decided it. Making the hint a preference instead of a filter moved _Puttaswamy_ to the top result.

**Nothing fails closed.** No key gives retrieval-only results. A router failure falls back to the raw question. A synthesis failure still returns the retrieved passages. A rate-limited provider hands off to the next one. The app is never a blank screen.

## Runs without an API key

Embeddings run locally on CPU through an ONNX build of MiniLM, so retrieval never depends on an API. With nothing configured you still get ranked, cited passages, and the app says plainly that it is in retrieval-only mode. Five providers are supported when you do want prose over the passages (Groq, Gemini, Cloudflare Workers AI, OpenAI and Hugging Face), and configuring several turns them into a fallback chain. A visitor can also paste their own key, which is held in their browser and never stored on the server.

## Fitting a legal corpus into 512 MB

The original prototype carried a 516 MB ChromaDB directory, which does not fit on a free instance at all. The deployable version replaces it with three artifacts: `vectors.npy` at 29 MB, memory-mapped so the OS pages it rather than the process holding it; `chunks.sqlite` at 40 MB, read-only and queried for the handful of rows in a result set; and `bm25.npz` at 10 MB, with BM25 weights precomputed as a sparse matrix. A keyword query becomes one sparse column slice and a row sum instead of a scan, which is why search returns in about 20 ms. The embedding model is ONNX rather than PyTorch, keeping roughly 800 MB of CUDA and torch wheels out of the image.

## Corpus and limits

19,144 passages across 1,411 documents: 19,023 judgment passages from [IL-TUR](https://huggingface.co/datasets/Exploration-Lab/IL-TUR) (ACL 2024), 116 statute passages covering the IPC, the IT Act 2000 and the Consumer Protection Act 2019, and 5 constitutional articles. Landmark judgments include _Kesavananda Bharati_, _Maneka Gandhi_, _Vishaka_, _Shreya Singhal_ and _Puttaswamy_.

The bail dataset is in Hindi, so English descriptions retrieve it less reliably than the judgment corpus, and the app warns about this wherever that dataset is selected rather than presenting weak results as strong ones. A 38-check smoke test covers health, retrieval quality, citation verification, uploads, outcome analysis, input validation and static assets.

The application was rebuilt from Streamlit onto FastAPI with a no-build front end, because Streamlit re-runs the whole script on every interaction and cannot accept a visitor's own API key per request. The original Streamlit version is preserved unchanged on its own branch.
