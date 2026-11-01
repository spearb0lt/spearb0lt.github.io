---
layout: page
title: Self-Hosted News Aggregator
description: A news aggregator that reads your sources, works out which stories are the same story, groups the rest into events, and writes a daily digest with the links attached.
img: assets/img/project/newsroom-news-agent.jpg
importance: 4
category: nlp
tags: [nlp, web-scraping, deduplication, clustering, summarization, rag, self-hosted, on-device, fastapi, nextjs, onnx]
---

{% assign pt = site.data.project_tags %}{% assign all_families = 'domain,method,stack,meta' | split: ',' %}{% assign fams = pt.families_on.project_pages | default: all_families %}{% if pt.enabled and pt.show_on.project_pages and page.tags %}<div class="proj-tags proj-tags-page pt-style-{{ pt.style.project_pages | default: 'soft' }}">{% for t in page.tags %}{% assign fam = pt.map[t] | default: pt.default_family %}{% if fams contains fam %}<span class="proj-tag pt-{{ fam }} pt-tag-{{ t | slugify }}">{{ t }}</span>{% endif %}{% endfor %}</div>{% endif %}

**Links:** [GitHub repository](https://github.com/spearb0lt/Self-Hosted-News-Research-Agent)

**Newsroom** is a news aggregator that reads your sources so you do not have to open twelve tabs. It pulls from RSS, sitemaps, aggregators and APIs, works out which stories are the same story, groups what is left into events, and writes a short daily digest with the links attached.

It runs with no API keys at all. Deduplication uses a 23 MB sentence encoder bundled into the deployment rather than a hosted service. Adding one LLM key upgrades the digest from headlines to written summaries.

## Ten bounded stages

Each stage is bounded and resumable, which is what lets the whole thing run inside a 300-second serverless function as well as on a machine with no time limit.

```
ingest     read every configured source, respecting robots.txt and rate limits
extract    fetch each article's full text, because feed summaries are thin
embed      turn each article into a vector
dedup      drop articles that are the same story as one already held
cluster    group the survivors into events, one event per real world happening
classify   assign each event a theme from this workspace's own taxonomy
summarise  write a short factual account of each event from its coverage
digest     assemble the bullets, Markdown, HTML and JSON
enrich     entities, sentiment and stance (optional, runs last on purpose)
deliver    email, Slack, Discord, Telegram or a webhook, when you ask for it
```

A **workspace** is one beat, with its own sources, theme taxonomy and schedule. Eight presets ship ready to use, every feed in them verified live. One real run of the `global-tech` preset against the live web: 8 sources with 7 answering, 100 articles seen and 98 new, 67 full texts extracted, 101 embedded, 89 events summarised, and a digest of 6 bullets across 7 themed sections.

## Deduplication is where it earns its keep

Four layers run in increasing order of cost:

1. **Canonical URL.** Tracking parameters, AMP suffixes, `www.`, `m.` and fragments are stripped before hashing, so `example.com/story?utm_source=x` and `www.example.com/story/` are one article rather than two.
2. **Content hash.** Catches a byte-identical reprint.
3. **SimHash.** A 64-bit locality-sensitive fingerprint over word trigrams, catching syndicated wire copy that each outlet lightly reworded. No model involved.
4. **Embedding cosine.** Catches independent reporting of the same event.

Layer 4 carries a measured weakness that a threshold alone cannot fix, so a contradiction guard sits behind it rather than the threshold being tuned until the problem disappears.

## Reading a beat, and researching one topic

The digest answers "what happened on my beat today". Every workspace carries the same five tabs: **Digest** groups events under the workspace's own themes, showing which outlets carried each and where the accounts diverge; **Raw** is the same window with no editorial layer, which never calls a language model and so costs nothing; **Sources** lists what the beat reads with each source's last result, and takes OPML in and out; **Chat** answers questions against what the workspace actually collected and quotes the articles it used; **Settings** holds the taxonomy, keyword rules and delivery.

Keyword rules come in three lists. **Exclude** drops a story at ingest, before anything is spent on it. **Boost** lifts a story up the digest without hiding anyone else's. **Include** is a whitelist, and layering one on feeds that are already topical throws away most of the beat, which is worth knowing before adding one.

Research answers the other question, "what is there about this, right now", without creating a workspace first. It fans out across every usable backend at once, merges duplicates, fetches article text and ranks what is left against the query, in three modes: just the ranked articles with no model called, a written cited brief, or a claim check that groups sources by whether they state the opposite, support it, or say nothing either way. A search can then be saved as a workspace, built from the outlets that actually answered it.

## How it is laid out

The server splits into a runtime that detects serverless versus server and exposes a capability matrix, one schema over SQLite and Postgres, 19 LLM providers behind a per-request keyring, 11 embedding backends with per-backend thresholds, 18 source adapters sharing one polite HTTP client, the ten pipeline stages with a resumable runner, and separate modules for research, claims, delivery, grounded question answering, the cost meter and the eight presets.
