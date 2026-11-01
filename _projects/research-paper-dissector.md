---
layout: page
title: Research Paper Dissector & Interrogator
description: Upload a research paper and interrogate every figure, table, equation and claim in it, with citations that point at a bounding box on a page.
img: assets/img/project/research-paper-dissector.jpg
importance: 3
category: nlp
tags: [nlp, document-ai, rag, hybrid-search, bm25, multimodal, self-hosted, on-device, fastapi, nextjs, onnx, live-demo]
---

{% assign pt = site.data.project_tags %}{% assign all_families = 'domain,method,stack,meta' | split: ',' %}{% assign fams = pt.families_on.project_pages | default: all_families %}{% if pt.enabled and pt.show_on.project_pages and page.tags %}<div class="proj-tags proj-tags-page pt-style-{{ pt.style.project_pages | default: 'soft' }}">{% for t in page.tags %}{% assign fam = pt.map[t] | default: pt.default_family %}{% if fams contains fam %}<span class="proj-tag pt-{{ fam }} pt-tag-{{ t | slugify }}">{{ t }}</span>{% endif %}{% endfor %}</div>{% endif %}

**Links:** [live app](https://dissect-sepia.vercel.app) and [GitHub repository](https://github.com/spearb0lt/Research-Paper-Dissector)

**Dissect** takes a research paper and lets you interrogate every figure, table, equation and claim in it, with citations that point at a real region of a real page. It works with no API key at all: parsing, figure and table extraction, keyword and semantic search and the whole browsing surface are local and free. A model key adds written answers and the analysis lenses on top, and is never required.

## The element is the unit

A paper becomes rows rather than text. Paragraphs, headings, tables with their grids, figures with their images, display equations, captions, footnotes and references each carry their page, bounding box, reading order and the heading trail they sit under. Retrieval, citation, the galleries and the reader overlay all read those same rows, which is why a citation can always point back at a region of a page rather than at a page number.

The reader draws that parse on the real page. A table whose columns are wrong, a figure cropped badly or a heading that was missed all become obvious the moment the boxes are outlined.

## Retrieval that can find a number

BM25 over a tokeniser that keeps `41.0`, `BLEU-4`, `p<0.05` and `10^-4` whole, fused with exact dense cosine by reciprocal rank fusion. Dense retrieval alone cannot tell 41.0 from 41.8, which is why asking a text-only RAG system for a score from a results table fails so often. A question naming "Figure 3" or "Table 2" is treated as an exact lookup and pinned to the top, because ranking it as a topic loses it: "figure" matches every figure in the paper.

There is no vector database. A paper is a few hundred to a few thousand chunks, and at 384 dimensions a numpy matmul against all of them is exact and sub-millisecond, with no index to build and no service to run. Dropping Chroma is also what makes the serverless tier possible.

## Two tiers that look the same from downstream

Nothing after the parser knows which tier ran, which is what lets a paper parsed deeply on a laptop be served from a deployment that could never have parsed it.

|                     | fast                               | deep                        |
| ------------------- | ---------------------------------- | --------------------------- |
| needs               | PyMuPDF, pdfplumber, ~25 MB        | Docling, PyTorch, ~2.5 GB   |
| runs on             | anything, including serverless     | a laptop, a VM, a container |
| the Attention paper | 2.5 s                              | 250 s                       |
| figures found       | 3                                  | 6                           |
| column structure    | inferred from whitespace corridors | TableFormer                 |

### Reading a booktabs table without rules

Scientific papers overwhelmingly use booktabs style: horizontal rules above the header, below it and at the foot, and no vertical rules at all. That defeats every table finder looking for intersecting lines, and inferring both axes from whitespace is worse than useless, as pdfplumber and PyMuPDF each demonstrated by turning page 3 of "Attention Is All You Need" into a 22 by 8 table of word fragments and finding seventeen tables in a paper that has four.

The parser instead groups aligned horizontal rules into bands, clusters words into rows by vertical centre, and finds column boundaries by projecting every word onto the x-axis and taking the corridors no word covers in essentially any row. Measured against five hand-checked tables, including the thirteen-column ablation grid in the Transformer paper and the eleven-column benchmark table in ColPali, it gets the exact column count on four and splits one column too many on the fifth. A regression eval locks that result in.

### Finding display equations

The obvious test, "does this line use a maths font", does not work, because in a LaTeX paper body and maths fonts mix constantly inside ordinary prose. What separates a display equation is that it contains no body text font at all. That test finds exactly the four display equations in the Transformer paper with no false positives, where the first version found 27 because author footnote asterisks and the `<pad>` and `<EOS>` tokens on the attention visualisation pages are also set in no body font.

## Decisions worth naming

**Citations are validated after generation.** A reference to an excerpt that was never supplied is stripped, so a fabricated citation cannot reach the screen looking like provenance. The claim survives visibly uncited, which is the honest outcome.

**Contextual retrieval without the bill.** Most of what an LLM-written context sentence supplies is the chunk's position in the document, which the parser already knows exactly, so each chunk gets its paper title, heading trail and label prepended. Deterministic, free, and it still works with no key.

**Local embeddings win even when a hosted key is present.** Vectors from two backends are not comparable, so whichever backend indexed a paper is the only one that can search it. Ranking by quality instead is a trap: installing the server extras adds a higher-scoring model, the automatic choice silently changes, and every existing index stops being searchable.

**Fetching a user-supplied URL is a request forgery primitive**, so every host is resolved and checked against the private ranges before connecting and again on each redirect hop, and the response is accepted only if it starts with the PDF magic bytes.

Fifteen analysis lenses sit on top, each a retrieval recipe plus a prompt, and one can be run across the whole library with results appearing as they land. A retrieved figure is attached to the request as an actual image where the provider accepts one, so a question about a chart is answered by reading the axes rather than by paraphrasing the caption, and the answer says which of the two happened.
