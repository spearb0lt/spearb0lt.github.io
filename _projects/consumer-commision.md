---
layout: page
title: Consumer Commission Complaint Agent
description: A guided intake that turns a consumer's own account of what went wrong into a file-ready complaint petition, routed to the correct Commission.
img: assets/img/project/consumer-commision.jpg
importance: 3
category: agentic-ai/llm
tags: [llms, legal-tech, document-generation, fastapi, hackathon]
---

{% assign pt = site.data.project_tags %}{% assign all_families = 'domain,method,stack,meta' | split: ',' %}{% assign fams = pt.families_on.project_pages | default: all_families %}{% if pt.enabled and pt.show_on.project_pages and page.tags %}<div class="proj-tags proj-tags-page pt-style-{{ pt.style.project_pages | default: 'soft' }}">{% for t in page.tags %}{% assign fam = pt.map[t] | default: pt.default_family %}{% if fams contains fam %}<span class="proj-tag pt-{{ fam }} pt-tag-{{ t | slugify }}">{{ t }}</span>{% endif %}{% endfor %}</div>{% endif %}

**Links:** [GitHub repository](https://github.com/spearb0lt/Consumer-Commission-Complaint-Agent) and [demo walkthrough](https://github.com/spearb0lt/Consumer-Commission-Complaint-Agent#demo) (6m 18s, captioned)

**Nyaya Setu** is a guided intake for the Consumer Protection Act, 2019, built for the ILTN Vibeathon. It turns a consumer's own account of what went wrong into a file-ready complaint petition, routes it to the correct Commission, and hands back the exact paperwork checklist for e-Daakhil.

## The problem

An Indian consumer with a genuine grievance faces three walls before they can even file.

**Which Commission?** Pecuniary jurisdiction shifted under the 2021 Rules and territorial jurisdiction has four separate limbs under Section 34(2). Getting it wrong means a return of the papers weeks later.

**How is a complaint written?** A consumer complaint is a pleading. It needs a cause title, numbered paragraphs each beginning with "That", statutory grounds, a prayer, a verification and a sworn affidavit. Very few people filing in person have ever seen one.

**What has to be attached?** The registry rejects filings for a missing annexure, an unsigned verification, or a Memo of Parties without a phone number, and each rejection costs weeks.

Advocates solve all three in an afternoon and charge accordingly. That fee is often larger than the amount in dispute, which is exactly why so many small consumer claims are simply abandoned.

## The eight steps

An eight-step intake collects the category (six cover the bulk of consumer disputes, each mapped to the provisions it pleads), the plain-language account with an AI assist that reorganises it chronologically and names the details still missing, the parties with the validation a Memo of Parties needs, the dates and amounts that drive limitation and the pecuniary forum, the reliefs that each become a numbered prayer, the evidence with each attachment lettered as an annexure, an editable review of every particular, and finally the complaint itself as DOCX and PDF with a filing checklist and the jurisdiction reasoning.

## The design decision that matters

**The jurisdiction engine never touches a model.** The Commission tier, the territorial options, the limitation position and the indicative fee are all computed from the Act and the 2021 Rules in a dedicated module. Those are the outputs a user would actually rely on, so they are deterministic, auditable and identical on every run.

The model is used for exactly one thing: turning the user's own account into the Statement of Facts, under a system prompt that forbids inventing any fact and marks anything missing as `[to be filled]`. Everything else in the pleading (the cause title, the grounds, the prayer, the verification and the affidavit) is assembled deterministically from the structured intake. With no API key configured at all the app still produces a complete, filable pleading from a built-in template. It never hard-fails on a missing key.

## What the generated complaint contains

A seven-page pleading in Times New Roman, in the order a Commission registry expects it: cause title naming the correct Commission and bench location, memo of parties with the `... COMPLAINANT` and `... OPPOSITE PARTY` tags, list of dates and events, a statement of facts running 11 to 15 numbered paragraphs each beginning with "That", grounds keyed to the provisions the category attracts, a lettered prayer with one clause per relief sought, the list of annexures, the verification, and an affidavit with its own verification and attestation block. Rupee figures are written throughout as `Rs. 62,990/- (Rupees Sixty Two Thousand Nine Hundred and Ninety Only)`, with Indian digit grouping and lakh or crore wording.

One assembly step feeds three renderings: the pleading is built once into a list of typed blocks, and the DOCX writer, the PDF writer and the browser preview all render from that same list, so the three outputs cannot drift apart.

## Any one key is enough, and it need not be yours

Groq, Google Gemini, Cloudflare Workers AI, OpenAI and Hugging Face all speak the OpenAI chat-completions protocol, so one HTTP client serves all five. A visitor can paste their own key and have it tested on the spot; it is kept in their browser, sent as a request header with their own calls, and never written to the server's disk, logs or store. Anything set in the environment acts as a default for visitors who have not brought one. The router tries providers in preference order and fails over on any error, and a provider that fails hard goes into a short cooldown rather than being retried on every request. Token budgets are deliberately small so a full session fits inside a free allowance: 2600 output tokens for a complete draft and 900 for the assist.

## Scope

This produces a draft, not legal advice, and the app says so on every screen. Pecuniary limits and filing fees have changed several times since 2019; the values shipped are current as of the 2021 Rules and are flagged as indicative. Uploaded files are held in memory-backed temporary storage and dropped when the session expires.

The application was rebuilt from Streamlit onto FastAPI with a no-build front end, because Streamlit re-runs the whole script on every interaction and cannot accept a visitor's own API key per request. The original Streamlit version is preserved unchanged on its own branch.
