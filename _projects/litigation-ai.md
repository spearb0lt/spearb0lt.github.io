---
layout: page
title: LitigatAI
description: An AI-powered litigation and dispute-resolution platform for Indian legal practice.
img: assets/img/project/litigation-ai.jpg
importance: 1
category: agentic-ai/llm
---

**Links:** [GitHub repository](https://github.com/spearb0lt/LitigatAI) and [live demo](https://litigat-ai.streamlit.app/)

LitigatAI is a Streamlit-based AI platform built for Indian advocates, litigation interns and legal researchers. It brings together **10 integrated tools** that automate the most time-consuming parts of legal practice, from extracting key dates out of a case file to drafting counter-arguments against an opponent's pleadings, so that practitioners can spend their time on strategy rather than paperwork.

## Under the hood

- A multi-page Streamlit web app organised around the 10 tools.
- A layered LLM stack chosen for both quality and speed: **Google Gemini 2.5 Flash** as the primary model, **Groq Llama 3.3 70B** for fast routing tasks, and an OpenAI-compatible endpoint as a fallback.
- Each tool is designed around a real litigation workflow, keeping outputs grounded in the documents the user provides.

If the live demo has gone to sleep, give it a moment to spin back up on first load.
