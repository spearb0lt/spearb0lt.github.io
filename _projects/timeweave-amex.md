---
layout: page
title: TimeWeave - Counterfactual Journey Engine
description: Cross-channel journey stitching for American Express - one identity, one timeline, and alternate futures ranked by observed outcome.
img: assets/img/project/timeweave-amex.jpg
importance: 2
category: data-analytics
tags: [analytics, identity-resolution, churn-prediction, causal-inference, duckdb, fastapi, react, hackathon]
---

{% assign pt = site.data.project_tags %}{% assign all_families = 'domain,method,stack,meta' | split: ',' %}{% assign fams = pt.families_on.project_pages | default: all_families %}{% if pt.enabled and pt.show_on.project_pages and page.tags %}<div class="proj-tags proj-tags-page pt-style-{{ pt.style.project_pages | default: 'soft' }}">{% for t in page.tags %}{% assign fam = pt.map[t] | default: pt.default_family %}{% if fams contains fam %}<span class="proj-tag pt-{{ fam }} pt-tag-{{ t | slugify }}">{{ t }}</span>{% endif %}{% endfor %}</div>{% endif %}

**Links:** [team repository](https://github.com/aayushdebugging/amex-hackathon)

A team hackathon project for American Express on cross-channel journey stitching, which I contributed the bulk of the implementation to. TimeWeave takes a customer's fragmented touches across four channels (app, web, call centre and in person), stitches them into **one identity and one journey**, explains **why** that customer is at risk, and then branches the journey into alternate futures ranked by outcome so an analyst can pick an action and fire it, with a human in the loop and an audit trail behind every decision.

Two things separate it from a dashboard:

- **It captures the anonymous signal everyone misses.** The pre-login web session where a customer searches "Cancel membership" is normally invisible, because it carries no account id. TimeWeave resolves it back to the person with a confidence score, a plain-English explanation, and a reversible un-merge.
- **It is honest about causality.** Every recommendation is labelled as an _observed retention rate within a cohort of similar journeys_: correlational, not a causal guarantee. Nothing in the UI or the API claims causal uplift.

The whole stack runs offline on embedded DuckDB: no servers, no API keys, no network calls required.

## Identity resolution

Resolution runs in two passes. The deterministic pass links authenticated account keys, phones on file, tokenized PANs and device ids at confidence 1.00, and additionally attributes earlier anonymous touches by **cookie continuation**: if the same ECID later appears in an authenticated event, every earlier touch on it belongs to that identity. That half is exact, not probabilistic.

The fuzzy pass scores anonymous sessions on a weighted evidence sum over device fingerprint (0.40), IP geolocation (0.20) and cookie continuation (0.31), capped at 0.99 so the system never claims certainty from probabilistic evidence. Above 0.85 it auto-merges; between 0.55 and 0.85 it routes to a human steward; below 0.55 it is surfaced as a guardrail ("we correctly did not merge this") rather than hidden.

Every merge is a first-class auditable record with its method, confidence, feature breakdown and explanation. Un-merging propagates: detach a customer's anonymous session and the cancel-page signal disappears from her feature vector, so her churn score and its attribution both recompute. A tokenized card that maps to more than one identity is deliberately **downgraded** to a household merge pending review, because individual-versus-household ambiguity is a real failure mode and resolving it silently would be wrong.

## Churn scoring with per-driver attribution

One feature definition is the single source of truth, read both by the synthetic world model that _draws_ the ground truth and by the classifier that _learns to predict_ it, so there is no drift between what happened and what was learned, and a recovered coefficient is evidence rather than coincidence. Seven features are extracted from the **stitched** journey, which is exactly the journey a human analyst sees.

The classifier is a genuinely trained logistic regression with two interchangeable backends behind one interface: scikit-learn when importable, and a pure-Python gradient-descent trainer with zero third-party dependencies otherwise.

Attribution is computed in **raw feature space** and then converted to percentage points by a leave-one-out marginal. Standardised contributions measure an effect relative to the population average, which makes a customer with none of a bad thing look protective and distorts the ordering; folding standardisation back out recovers the true per-driver effect. The marginal is evaluated in probability space so the sigmoid's nonlinearity is handled correctly, which turns log-odds into something a business audience can read: "removing the broken callback drops predicted churn by 26.4 points."

## Counterfactual cohorts

The honest core of the product. Rather than inventing retention numbers at display time, one generative world model produces the outcomes, and each branch reports the **observed retention rate within a matched cohort** of similar journeys, with its confidence band and the cohort size stated on screen. The recommended action is the one that repairs the top risk drivers, not the obvious discount, and the UI says so, including when the obvious move is the weak one.
