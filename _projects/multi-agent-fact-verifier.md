---
layout: page
title: Multi-Agent Fact Verifier
description: A supervised team of nine LLM agents that researches the open web, checks every claim against the sources it actually read, and writes a cited report.
img: assets/img/project/multi-agent-fact-verifier.jpg
importance: 1
category: agents/agentic-ai
tags: [llms, agents, multi-agent, fact-checking, rag, web-scraping, evaluation, fastapi, nextjs, gemini, groq]
---

{% assign pt = site.data.project_tags %}{% assign all_families = 'domain,method,stack,meta' | split: ',' %}{% assign fams = pt.families_on.project_pages | default: all_families %}{% if pt.enabled and pt.show_on.project_pages and page.tags %}<div class="proj-tags proj-tags-page pt-style-{{ pt.style.project_pages | default: 'soft' }}">{% for t in page.tags %}{% assign fam = pt.map[t] | default: pt.default_family %}{% if fams contains fam %}<span class="proj-tag pt-{{ fam }} pt-tag-{{ t | slugify }}">{{ t }}</span>{% endif %}{% endfor %}</div>{% endif %}

**Links:** [GitHub repository](https://github.com/spearb0lt/Multi-Agent-Fact-Verifier)

A supervised team of LLM agents researches a question on the open web, checks every claim against the sources it actually read, and writes a cited report. Claims that fail verification never reach the report; the ones that do carry their sources, and the report says what was thrown out and why.

## Why it is not a prompt chain in a costume

Most "AI research agent" projects are one model called four times and described in agent vocabulary. Each of the claims below is checkable from the run itself:

|                                        | How you can check it                                                                                       |
| -------------------------------------- | ---------------------------------------------------------------------------------------------------------- |
| nine roles, not one prompt             | each has its own model tier, tools and prompt; the per-agent cost table shows who did the work             |
| agents choose their own actions        | a reason-and-act loop, with every tool call recorded with arguments and result in the `tool_calls` table   |
| they collaborate rather than chain     | a shared blackboard and a message bus; `mas messages <run>` prints who told whom what                      |
| verification deletes rather than flags | a claim the Fact Checker rejects never reaches the Writer, and the report lists the exclusions             |
| contradiction is detected              | vectors find claims about the same subject, and a Reconciler rules on only those pairs                     |
| two feedback loops                     | the Supervisor can send researchers back out, the Critic can send the draft back, both bounded by counters |
| runs survive the process               | queue and blackboard checkpointed after every step, so a run pauses on one machine and resumes on another  |

## Two workflows on one kernel

The `research_report` graph takes a topic: a Planner produces subquestions, N Researchers run in parallel, an Analyst turns findings into claims, N Fact Checkers verify in parallel, a Reconciler rules on conflicts, and a Supervisor either sends researchers back out for gaps or sends the work to the Writer, Editor and Critic, the last of which can send the draft back to be revised.

The `claim_check` graph takes a single claim, plans three angles, and runs three Researchers in parallel, deliberately searching separately for it, against it and around it. One agent asked to "research this claim" searches for the claim and finds only the confirming half. It runs about five times cheaper than a full report.

Adding the second graph required no change to the orchestrator, the blackboard, the budget guard or the UI.

## Verification that is willing to say no

From an actual run, unedited, where it refuses to state the well-known consensus because it could not verify it from sources it read:

> **What the evidence says**
>
> - Intermittent fasting is unlikely to cause significant loss of lean body mass, especially with moderate to high protein intake [S1].
> - Infrequent meal feeding and prolonged fasting may be suboptimal for supporting muscle protein remodeling [S2].
>
> **How this was checked**
> Verdict: **unverifiable**. Confidence in this ruling: high. Independent outlets behind the ruling: 2.

The supporting search found a source saying fasting does not cost muscle; the refuting search found a peer-reviewed paper saying it may. The Fact Checker ruled the comparison unverifiable rather than picking a side.

## Stopping costs nothing

Every ceiling pauses a run rather than killing it, and so does a spent free-tier quota. Everything gathered stays on the blackboard. A run started in the terminal can be paused from the browser and resumed by a scheduled job, because a run lives in the database rather than in a process, and it can be resumed onto a different provider when the first one runs out.

Below the ceiling it degrades rather than failing: past 70% of budget the strong roles drop to the cheap model and the Planner asks fewer questions, so the result is a smaller finished report instead of a larger unfinished one.

The dollar figure is an estimate at the provider's published list price, charged or not. A model with no published price reports as _unpriced_ rather than as free, because a zero meaning "nobody entered a number" reads exactly like a zero meaning "this cost nothing". Across seven completed runs on Cloudflare `llama-3.3-70b`, a claim check took 79 to 98 seconds and 33k to 62k tokens, and a full report took 3.5 to 5 minutes and 77k to 92k tokens. Neither was billed.

Wall clock is set by the provider's tokens-per-minute allowance far more than by the work, so the sensible unit to budget in is tokens, and the clock is a property of the provider you chose.

## Nineteen providers behind one interface

Free tiers (Gemini, Groq, Cloudflare Workers AI, Cerebras, SambaNova), paid (OpenAI, Anthropic, Mistral, DeepSeek, Together, Fireworks, xAI, Perplexity, OpenRouter, Hugging Face) and local with no key (Ollama, LM Studio, llama.cpp, vLLM). One key is enough to run the whole team, because roles are assigned a _tier_ rather than a model: the cheap tier takes the Researcher, Fact Checker and Supervisor, where the work is high volume and mechanical, and the strong tier takes the Planner, Analyst, Writer, Editor and Critic, which run once or twice a run and set the quality of everything.

Tool calling uses each provider's native function calling where it exists, across the sixteen OpenAI-compatible adapters, and a JSON protocol in the prompt everywhere else. Both paths are tested, because a bug in one is invisible from the other.
