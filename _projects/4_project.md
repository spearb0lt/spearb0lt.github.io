---
layout: page
title: CodeGen - Autonomous Competitive Programming Solver
description: An end-to-end AI solver built for the Meta Hacker Cup 2025 AI Track.
img: assets/img/proj_4.jpg
importance: 1
category: applications
---

**Links:** [my-codegen-api2 (production API)](https://github.com/spearb0lt/my-codegen-api2) and [CodeGen-Hacker-Cup-AI-devkit (devkit)](https://github.com/spearb0lt/CodeGen-Hacker-Cup-AI-devkit)

The system behind my **Global Rank 10** finish in the Meta Hacker Cup 2025 (AI Track). The AI Track is a parallel competition where participants build AI systems to solve the same algorithmic problems that top human programmers tackle. This project is a purpose-built, end-to-end autonomous solver that accepts a full problem package and returns a validated solution in a single API call.

## How it works

- A FastAPI server (deployed on Render) accepts a problem package (statement, sample input/output and optional images) and generates an optimal Python solution using Google's Gemini LLM.
- A complete multimodal pipeline fetches, decodes and passes problem diagrams to the model, since Hacker Cup statements frequently embed graphs and figures served from CDN URLs.
- The solver enforces the strict competitive-programming I/O format (for example `Case #1: 42`) by running each candidate against the sample data before returning it.
- On failure it regenerates iteratively, feeding the error back to the model for up to four attempts, and dedicated endpoints re-run solutions on real competition inputs with LLM-based debugging.

## Results

The system solved problems in the upper-medium to hard range, including "Designing Paths" (Round 2) and "Treehouse Telegram" (Round 3), estimated at roughly 2200 to 2500 rating, involving graph algorithms, number theory and careful complexity analysis.

## Special mention: the devkit

The [CodeGen-Hacker-Cup-AI-devkit](https://github.com/spearb0lt/CodeGen-Hacker-Cup-AI-devkit) documents the full evolution of the solver, from the initial prototypes through the final multimodal API, and ships the reusable client-side automation tools (the `CP_GEN` toolkit) used to call the deployed API and test solutions during the contest.
