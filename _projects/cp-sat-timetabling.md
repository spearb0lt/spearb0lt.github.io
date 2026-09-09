---
layout: page
title: Non-conflicting Timetable Generator
description: University timetabling and exam scheduling as a constraint satisfaction problem, solved with OR-Tools CP-SAT and verified by an independent checker.
img: assets/img/project/time-table-cp-sat.jpg
importance: 1
category: optimization/or
tags: [optimization, constraint-programming, scheduling, or-tools, fastapi]
---

{% assign pt = site.data.project_tags %}{% assign all_families = 'domain,method,stack,meta' | split: ',' %}{% assign fams = pt.families_on.project_pages | default: all_families %}{% if pt.enabled and pt.show_on.project_pages and page.tags %}<div class="proj-tags proj-tags-page pt-style-{{ pt.style.project_pages | default: 'soft' }}">{% for t in page.tags %}{% assign fam = pt.map[t] | default: pt.default_family %}{% if fams contains fam %}<span class="proj-tag pt-{{ fam }} pt-tag-{{ t | slugify }}">{{ t }}</span>{% endif %}{% endfor %}</div>{% endif %}

**Links:** [GitHub repository](https://github.com/spearb0lt/CP-SAT-Based-Timetabling-and-Exam-Arrangement)

A universal university timetable system. It **builds** timetables from scratch, **proves** them free of conflicts with a checker that shares no code with the solver, and then **keeps them alive** as reality interferes: absences, weather, room losses, staff swaps, syllabus drift. An institution is a data folder, not a fork: point it at your CSVs and everything downstream works.

## Three guarantees

- **A conflict is impossible, not unlikely.** Clashes are detected at _student-equivalence-class_ level rather than cohort level. Two groups with different names can share students (a minor stream and the batch it draws from), and a name comparison would call that slot free while the same people are already in class.
- **Validity is checkable independently.** A separate verifier audits any timetable, including a hand-edited one, against 17 hard-constraint families and shares no code with the solver. A shared bug would make the check worthless, so the duplication is deliberate. The repair engine refuses to even _offer_ a proposal the verifier rejects.
- **It refuses rather than guesses.** No term dates? The dated layer says so and stops. Two people with the same initials in an imported file? Reported with candidates listed. Nobody asked a professor about Saturday? Treated as unavailable, not as consent.

## Generation: two stages, nine lexicographic objective tiers

Stage 1 decides time and people; stage 2 assigns concrete rooms by bipartite matching, which is polynomial and yields a precise infeasibility certificate ("these 4 events at Wed 10:00 compete for 1 room large enough") instead of a bare _infeasible_.

Objectives are **lexicographic, not a weighted sum**: solve tier _k_, freeze its optimum, solve tier _k+1_. That is what makes "why was my morning preference broken?" mechanically answerable: a non-zero optimum at tier _k_ means it lost to every tier above, and the tier above names the winner. A weighted sum cannot attribute anything. Admin-entered rules sit deliberately _above_ the built-in preference tiers, because a rule was typed by a human and a built-in tier is a heuristic nobody asked for.

## Diagnosis instead of "no solution found"

Pre-solve validation runs before any search and distinguishes **a shortage** from **a puzzle**: reporting "no solution found" after a ten-minute search when the real answer is "you are 108 teaching hours short" is treated as a defect. It separates delivery-hours from cohort-hours (one clubbed lecture to four batches is _one_ delivery-hour and _four_ cohort-hours; conflating them overstates staffing need by about 2×) and names a course with no competent instructor by name.

When an instance really is infeasible, CP-SAT assumption literals produce a **minimal conflicting set** plus ranked relaxation advice that is _tested_ by re-solving. A sensitivity pass asks which constraints are load-bearing. Two constraints are deliberately not relaxable: a timetable that double-books a student is not a worse timetable, it is not a timetable.

## Rules as data, and a dated calendar

Twelve rule types (same-day, before, minimum gap, fixed slot, room pinning, unavailability, day off, no first period and more) are rows in a table, enterable by form, by API or by an optional LLM assistant. Hard rules become constraints; soft rules form an objective tier. Every rule is validated against the live instance before storage, and one that references something the current semester lacks is shown as _unresolved_ and skipped, never guessed at.

A second, dated layer answers "what is actually happening on Tuesday the 12th?" as distinct from "what does a normal week look like?". It supports holidays, half-days with a cut-off period (which is also how a weather day is recorded), dated overrides, one-off sessions, phases and seasons. Instances are generated rather than stored, since 16 weeks × 565 events is derivable from the pattern plus deviations.

## Chapter-wise delivery and repair

A subject can be split across several professors, each teaching particular modules in a particular order. The ordering is the easy half; the consequence is the hard half, because a professor's timetable is then **not constant across the term** and phase boundaries come from delivered hours against module estimates rather than calendar dates. Concurrent delivery is modelled as a _band_ rather than a queue, handover feasibility decides whether a slot can stay put, and load spikes catch a professor whose entire term lands in one phase.

When something breaks, CP-SAT re-solves with the current timetable as hints plus a freeze window (genuine large-neighbourhood search), and returns up to three ranked alternatives at blast-radius caps of 1, 3, 5 and unbounded, so the smallest workable change is visible first.
