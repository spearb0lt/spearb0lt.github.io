---
layout: page
title: Olist Marketplace Intelligence
description: An end-to-end analyst project on Brazilian e-commerce data - a tested dbt/DuckDB warehouse, a causal study of late delivery, and an experiment design.
img: assets/img/project/olist-marketplace.jpg
importance: 1
category: data-analytics
tags: [analytics, causal-inference, experimentation, dbt, duckdb, tableau, llms, live-demo]
---

{% assign pt = site.data.project_tags %}{% assign all_families = 'domain,method,stack,meta' | split: ',' %}{% assign fams = pt.families_on.project_pages | default: all_families %}{% if pt.enabled and pt.show_on.project_pages and page.tags %}<div class="proj-tags proj-tags-page pt-style-{{ pt.style.project_pages | default: 'soft' }}">{% for t in page.tags %}{% assign fam = pt.map[t] | default: pt.default_family %}{% if fams contains fam %}<span class="proj-tag pt-{{ fam }} pt-tag-{{ t | slugify }}">{{ t }}</span>{% endif %}{% endfor %}</div>{% endif %}

**Links:** [GitHub repository](https://github.com/spearb0lt/Olist-Marketplace-Analytics) and [live dashboard on Tableau Public](https://public.tableau.com/app/profile/shubhro.dev/viz/olist_marketplace/0-Starthere)

> Late delivery causes a **1.70-point drop** in customer review score (95% CI [−1.76, −1.67]) and raises the chance of a 1–2 star review by **44.8 percentage points**, and the failing leg is carrier transit, not the seller.

An end-to-end analyst project on the Olist Brazilian e-commerce dataset: a tested dbt/DuckDB warehouse, a documented metric layer, a quasi-experimental causal study and a randomised-experiment design parameterised from real baselines. The whole thing runs in about 90 seconds from a clean clone, with no credentials and no cloud.

It is deliberately the most-used e-commerce dataset on Kaggle, so the baseline is familiar and the difference is easy to calibrate.

## The business question

A marketplace VP has one budget. Logistics wants to cut delivery times; Growth wants to fund customer retention. Which one pays, and how confident can we be?

## Retention: the wrong answer and the right one

`customer_id` in this dataset is issued fresh per order, so any cohort analysis keyed on it is **mathematically forced to 0%** retention. Re-keyed on `customer_unique_id`, the true repeat rate is **3.00%**, and the cohort triangle is still essentially empty. That is reported as the finding rather than worked around: 96.88% of people ordered exactly once in 25 months, so a customer-retention programme has almost no population to act on. The signal lives on the **supply** side instead (46.1% of sellers survive six months) and in category repeat propensity, which spans 7.5×.

## Does late delivery _cause_ dissatisfaction?

Lateness is not randomly assigned, so the estimate is escalated in steps and each adjustment's movement is reported: a naive difference in means of −1.7273, an OLS fit with distance, category, state and month fixed effects at −1.6757, and a 1:1 propensity-matched ATT of **−1.7138** over 7,606 pairs. Controls absorbed only 0.78% of the naive estimate.

The claim is then attacked from four directions: every covariate balances to |SMD| < 0.03 after matching; a negative control confirms lateness does not predict things chosen before delivery; 200 placebo reassignments put the observed effect **103 placebo standard deviations** away from noise; and an **E-value of 11.17** says an unmeasured confounder would need a risk ratio above 11.17 with both lateness and bad reviews to explain it away. The dose-response is monotonic across all eight buckets. The identifying assumption is stated explicitly so it can be challenged, and the main weakness (seller identity is not controlled for) is named in the memo.

## Which leg fails, and the experiment that would confirm it

Carrier transit is the culprit: 7.84 days on time versus 25.66 days when late, a 3.3× blow-out, against 2.1× for the seller's own handover leg. Rio de Janeiro is the geographic outlier, breaching at 13.47% on only 489 km.

The follow-up experiment is designed from measured parameters rather than assumptions: randomisation at **zip-code prefix** stratified by state, an ICC of 0.0221 giving a design effect of 1.1512, an MDE of 0.15 review points reaching power in about two weeks, and CUPED variance reduction **measured at 2.68%** rather than the 30–50% the textbooks quote.

## Can an LLM be trusted with these questions?

The last module is a governed analytics copilot built as a measured comparison, not a demo. Two arms answer the same 56-question labelled eval set: a **semantic layer** where the model may only pick from a governed catalogue and a deterministic compiler writes the SQL, versus **text-to-SQL** where the model writes the query itself.

Neither simply wins, and that is the finding. Text-to-SQL scores higher overall (91.3% vs 89.1%) because it can answer multi-step questions the catalogue deliberately excludes, but within catalogue scope the semantic layer is more accurate (95.3%), more stable across repeats, abstains correctly 100% of the time, and **never fabricated an answer**, against a 16.7% hallucination rate for text-to-SQL. Both hallucinations were fluent and completely invented: a gross profit margin, when the dataset contains no cost data at all, and a Net Promoter Score, which is not computable from 1–5 review scores.

Across all eight candidate models the semantic layer wins every time, and text-to-SQL accuracy varies **4.3× more** with model choice, so a governed layer moves correctness out of the model and into the catalogue, and a small cheap model becomes viable.
