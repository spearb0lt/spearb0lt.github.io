---
layout: page
title: CodeGen - Autonomous Competitive Programming Solver
description: An end-to-end AI solver built for the Meta Hacker Cup 2025 AI Track.
img: assets/img/2.jpg
importance: 1
category: applications
---

**Links:** [my-codegen-api2 (API)](https://github.com/spearb0lt/my-codegen-api2) and [CodeGen-Hacker-Cup-AI-devkit (devkit)](https://github.com/spearb0lt/CodeGen-Hacker-Cup-AI-devkit)

The system behind my **Global Rank 10** finish in the Meta Hacker Cup 2025 (AI Track). It is an end-to-end autonomous solver that takes a full problem package and returns a validated solution in a single call.

## How it works

- Accepts a problem package (statement, sample input/output and optional images) and generates an optimal Python solution using Google's Gemini LLM through a FastAPI server deployed on Render.
- Runs a complete multimodal pipeline to fetch, decode and pass problem diagrams (often served from CDN URLs) to the model.
- Enforces the strict competitive-programming I/O format by running each candidate against the sample data before returning it.
- Regenerates iteratively on failure (up to four attempts), feeding the error back to the model, and exposes endpoints to re-run on real competition inputs with LLM-based debugging.

## Results

The system solved upper-medium to hard problems, including Round 2 "Designing Paths" and Round 3 "Treehouse Telegram" (estimated ~2200 to 2500 rating), which involve graph algorithms and number theory.

## Special mention: the devkit

The [CodeGen-Hacker-Cup-AI-devkit](https://github.com/spearb0lt/CodeGen-Hacker-Cup-AI-devkit) documents the full evolution of the solver (initial prototypes through the final multimodal API) and ships the reusable client-side automation tools (the `CP_GEN` toolkit) used to call the deployed API and test solutions during the contest.
