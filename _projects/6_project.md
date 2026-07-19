---
layout: page
title: Consumer Commission Complaint Agent
description: A guided-intake agent that turns a plain-language grievance into a file-ready Indian Consumer Commission complaint.
img: assets/img/proj_6.jpg
importance: 3
category: applications
---

**Links:** [GitHub repository](https://github.com/spearb0lt/Consumer-Commission-Complaint-Agent) and [live demo](https://consumer-commission-complaint.streamlit.app/)

A Streamlit-hosted, guided-intake agent that turns a consumer's plain-language account of a grievance into a **file-ready Consumer Commission complaint petition**. It drafts the petition in authentic Indian legal pleading style, routes it to the correct commission, and packages it as a downloadable DOCX and PDF along with an e-Daakhil filing checklist, so a non-lawyer can go from a problem description to a submission-ready document.

## How it works

- A **six-step wizard** collects the facts of the grievance in plain language.
- **Jurisdiction routing** selects the correct District, State or National commission based on the claim value, following the 2021 Pecuniary Rules.
- A **constrained Gemini pipeline** produces authentic pleading language: numbered "That..." paragraphs, third-person formal voice, inline Consumer Protection Act 2019 citations, `Rs. X/- (Rupees X Only)` monetary notation, `Annexure` exhibit labelling and a numbered grounds section, matching the style of real filings before District Consumer Commissions across several states.
- **Document generation** exports a clean DOCX and PDF ready to attach to the filing.

If the live demo has gone to sleep, give it a moment to spin back up on first load.
