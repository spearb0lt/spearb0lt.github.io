---
layout: page
title: LitigatAI
description: An AI workbench for Indian litigation practice - ten tools covering a matter from the first brief to the final filing.
img: assets/img/project/litigation-ai.jpg
importance: 1
category: agentic-ai/llm
tags: [llms, legal-tech, agents, document-generation, fastapi, hackathon, live-demo]
---

{% assign pt = site.data.project_tags %}{% assign all_families = 'domain,method,stack,meta' | split: ',' %}{% assign fams = pt.families_on.project_pages | default: all_families %}{% if pt.enabled and pt.show_on.project_pages and page.tags %}<div class="proj-tags proj-tags-page pt-style-{{ pt.style.project_pages | default: 'soft' }}">{% for t in page.tags %}{% assign fam = pt.map[t] | default: pt.default_family %}{% if fams contains fam %}<span class="proj-tag pt-{{ fam }} pt-tag-{{ t | slugify }}">{{ t }}</span>{% endif %}{% endfor %}</div>{% endif %}

**Links:** [live app](https://litigatai.onrender.com), [GitHub repository](https://github.com/spearb0lt/LitigatAI) and [demo walkthrough](https://github.com/spearb0lt/LitigatAI#demo) (6m 17s, captioned)

An AI workbench for Indian litigation practice, built for the ILTN Vibeathon. Ten tools cover a matter from the first brief to the final filing, in one web app deployable on a free instance in a few minutes. It is a FastAPI service with a hand-written single page front end: no build step, no Node toolchain, no database server required.

## The ten tools

| Tool                | What it gives you                                                                                                     |
| ------------------- | --------------------------------------------------------------------------------------------------------------------- |
| List of Dates       | Every material date pulled out of a case file into a court-ready chronology you can edit and export                   |
| Judgment Summariser | A structured brief: case details, facts, issues, arguments, held, ratio, significance                                 |
| Authority Check     | Whether a cited judgment is still good law, with the citing judgments that decide it                                  |
| Translate and OCR   | Text out of scans, any Indian language into English, then a question box over the document                            |
| Legal Research      | Cited answers on Indian law, grounded in Indian Kanoon retrieval, or drawn from an uploaded judgment                  |
| Prompt Enhancer     | A rough question rewritten into a structured research instruction, handed straight to Legal Research                  |
| Bare Acts           | Eleven Indian statutes indexed section by section, with amendment history and an ask box on any provision             |
| Document Drafter    | Plaints, written statements, arbitration pleadings, counter claims, notices and applications, citations marked inline |
| Counter Arguments   | Every claim in the other side's pleading extracted, rated, rebutted, then assembled into a written statement          |
| Court Tracker       | A hearing diary with next dates, outcomes, status and an eCourts CNR lookup                                           |

Every answer exports as DOCX, PDF, CSV, Markdown or plain text.

## Bring your own key, and the plumbing that makes that safe

The app works with Groq, Google Gemini, Cloudflare Workers AI, OpenAI and Hugging Face, and needs exactly one of them. The key can come from either side: a visitor pastes their own into the top bar and it is tested against the provider on the spot, or the operator sets one in the environment as a default. A visitor's key always wins for their own request, and the panel labels which is which so nobody has to guess whose credit a call is spending. That is what lets the app be hosted publicly on a free plan without the operator paying for anyone's inference.

Handling someone else's credential carefully is most of the work:

- It is read from a request header into a context variable that lives for one request and is dropped when it ends. The provider adapters are process-wide singletons, so the adapter is shared but the credential never is.
- Model lists and SDK clients are cached under a SHA-256 fingerprint of the key, never under the provider name alone, so one visitor's cached state is never handed to another.
- Nothing logs a key. The config endpoint reports only _which_ providers a request has a key for, never the value.
- A credential over 512 characters, or carrying anything outside printable ASCII, is rejected before it can reach an upstream `Authorization` header.
- Responses are sent `Cache-Control: no-store`, because a response can depend on the caller's key.
- A key the provider rejects is deleted from the browser rather than retried on every later call.

Cloudflare is the one provider that cannot be configured with a key alone, because its account id sits in the request URL rather than a header. Both halves are required, the provider reports itself unavailable with that reason when only one is present, and the account id is validated as letters and digits only before being placed in the URL, so a crafted value cannot escape its path segment.

## Two details worth naming

**Model lists are live.** On startup each provider is asked what it can actually serve, and the picker shows the intersection of that with a curated short list. A model the provider retires disappears on its own and new ones appear without a code change.

**Vision is tracked per model.** Scanned PDFs and images need a model that can read pictures. The app knows which ones can, and when the selected model cannot it names the ones that can rather than failing obscurely.

Routing is strict throughout: the provider and model chosen in the picker are what get called, with no silent switch to a different provider. When one rate-limits you, the app says so and tells you what to do about it.

## How it is put together

Three of the five providers speak the OpenAI chat-completions protocol, so they share one adapter with different base URLs, and a registry module is the only thing the tools talk to. That is why adding a provider is a small change in one file. Services are split by workflow: document extraction with vision OCR, an Indian Kanoon client, analysis, research, drafting, the statute library, the case tracker and the export builders.

The front end is vanilla JavaScript, hash-routed, with no framework and no build step. One file builds the DOM directly against a design system of CSS custom properties, so light and dark are one set of token definitions rather than two stylesheets. The markdown renderer is written in the file, which keeps model output rendering dependency-free and lets citation markers, verification flags and source references carry their own styling.

## Limits stated plainly

Every draft and every research answer is a first draft: the app marks uncertain citations as `verify` and repeats the warning on screen and in every exported document, but checking an authority remains the advocate's responsibility. Indian Kanoon is optional, and without a token Legal Research and Authority Check answer from the model's own knowledge and say so. The eCourts CNR lookup is captcha-protected and often fails, so manual entry is the reliable route. OCR reads the first eight pages by default and needs a provider with a vision model.

The application was rebuilt from Streamlit onto FastAPI, because Streamlit re-runs the whole script on every interaction and cannot accept a visitor's own API key per request. The original Streamlit version is preserved unchanged on its own branch.
