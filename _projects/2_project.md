---
layout: page
title: SENTRAL - Multi Spectrum Stock Analysis
description: An end-to-end equity analysis platform fusing fundamentals, technicals, multi-LLM sentiment and ML forecasting.
img: assets/img/proj_2.jpg
importance: 5
category: applications
---

**Links:** [GitHub repository](https://github.com/spearb0lt/SENTRAL-Multi-Spectrum-Stock-Analysis)

SENTRAL is an end-to-end, open-source stock analysis platform that blends classical financial analysis with modern LLM-driven sentiment and machine-learning forecasting to produce a single, explainable buy, hold or sell signal. It ships as two production-ready Streamlit apps (SENTRAL for deep single-stock analysis and a companion SCREENER inspired by screener.in and groww.in), backed by an 82-cell analysis notebook.

## The analysis pipeline

- **Fundamental scoring:** discounted cash flow (DCF), the Altman Z-Score, the Piotroski F-Score, Graham valuation and a wide set of financial ratios computed from statements.
- **Technical analysis:** 35 indicators (moving averages, RSI, MACD, ATR and more) alongside risk metrics, chart-pattern detection and seasonality analysis.
- **News and sentiment:** news is gathered from 13 sources (APIs, RSS feeds and Reddit), filtered for relevance, then scored by 10 sentiment models, including finance-tuned and reasoning LLMs.
- **ML forecasting:** LSTM and Transformer models forecast price trends, complemented by Monte Carlo simulation for uncertainty.
- **Signals and backtesting:** a composite engine fuses fundamentals, technicals and sentiment into a BUY/HOLD/SELL signal, and a 20-strategy backtesting module validates the approach before any decision.
- **Reporting:** every run produces an HTML and PDF report plus the underlying artefacts (forecasts, backtests, news corpus and trained models).

## Impact

Ensembling all three spectra, fundamentals, technicals and sentiment, boosted a beginner portfolio by **+45% over five months**, with correlation and feature-importance visualisations backing each recommendation.
