---
layout: page
title: SENTRAL - Multi Spectrum Stock Analysis
description: An end-to-end equity analysis platform fusing fundamentals, technicals, multi-LLM sentiment and ML forecasting.
img: assets/img/project/sentral-stock.jpg
importance: 3
category: data-analytics
tags: [finance, analytics, timeseries, llms, sentiment-analysis, forecasting]
---

{% assign pt = site.data.project_tags %}{% assign all_families = 'domain,method,stack,meta' | split: ',' %}{% assign fams = pt.families_on.project_pages | default: all_families %}{% if pt.enabled and pt.show_on.project_pages and page.tags %}<div class="proj-tags proj-tags-page pt-style-{{ pt.style.project_pages | default: 'soft' }}">{% for t in page.tags %}{% assign fam = pt.map[t] | default: pt.default_family %}{% if fams contains fam %}<span class="proj-tag pt-{{ fam }} pt-tag-{{ t | slugify }}">{{ t }}</span>{% endif %}{% endfor %}</div>{% endif %}

**Links:** [GitHub repository](https://github.com/spearb0lt/SENTRAL-Multi-Spectrum-Stock-Analysis)

SENTRAL is an end-to-end, open-source stock analysis platform that blends classical financial analysis with modern LLM-driven sentiment and machine-learning forecasting to produce a single, explainable buy, hold or sell signal. It ships as two production-ready Streamlit apps (SENTRAL for deep single-stock analysis and a companion SCREENER inspired by screener.in and groww.in), backed by an 82-cell analysis notebook.

## The analysis pipeline

- **Fundamental scoring:** discounted cash flow (DCF), the Altman Z-Score, the Piotroski F-Score, Graham valuation and a wide set of financial ratios computed from statements.
- **Technical analysis:** 35 indicators (moving averages, RSI, MACD, ATR and more) alongside risk metrics, chart-pattern detection and seasonality analysis.
- **News and sentiment:** news is gathered from 13 sources (APIs, RSS feeds and Reddit), filtered for relevance, then scored by 10 sentiment models, including finance-tuned and reasoning LLMs.
- **ML forecasting:** LSTM and Transformer models forecast price trends, complemented by Monte Carlo simulation for uncertainty.
- **Signals and backtesting:** a composite engine fuses fundamentals, technicals and sentiment into a BUY/HOLD/SELL signal, and a 20-strategy backtesting module validates the approach before any decision.
- **Reporting:** every run produces an HTML and PDF report plus the underlying artefacts (forecasts, backtests, news corpus and trained models).

## Validation before the signal

No recommendation ships unbacktested. Twenty strategies are replayed over the price history under explicit assumptions (0.1% commission round-trip, fully invested, close-price execution), and each reports Total Return, CAGR, Sharpe, Sortino, maximum drawdown, win rate, profit factor, trade count, Kelly criterion and a suggested stop-loss. Correlation and feature-importance visualisations sit behind each recommendation, so the composite signal can be traced back to the pillars that moved it.
