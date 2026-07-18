---
layout: page
title: SENTRAL - Multi Spectrum Stock Analysis
description: A multi-spectrum stock analysis engine that fuses fundamentals, technicals and custom-LLM sentiment.
img: assets/img/7.jpg
importance: 2
category: work
---

SENTRAL is a multi-spectrum equity analysis system that blends classical financial analysis with modern LLM-driven sentiment to produce buy, hold and sell signals.

## Approach

- **Fundamental analysis:** evaluates target companies using 14 metrics (P/E, P/B, Debt, ROE and more) plus the Piotroski F-Score and Altman Z-Score via custom functions.
- **Technical analysis:** computes 18 indicators (EMA20/50, SMA20/50, RSI14, MACD, ATR and others) and runs peer comparisons across companies in the same sector.
- **News and sentiment:** collects news through seven APIs and web scraping, filters items by relevance, then feeds the curated corpus to 10 LLMs (including finance-tuned and SOTA reasoning models) for sentiment extraction and signal generation.
- **Forecasting and ensembling:** applies Transformer and LSTM models to forecast price trends, then ensembles sentiment with fundamental and technical indicators to compute buy/hold/sell probabilities.

## Impact

Ensembling all three spectra boosted a newbie portfolio by **+45% over five months**, with correlation and feature-importance visualisations supporting each decision.
