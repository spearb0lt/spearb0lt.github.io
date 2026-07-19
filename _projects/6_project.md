---
layout: page
title: Consumer Commission Complaint Agent
description: A guided-intake agent that turns a plain-language grievance into a file-ready Indian Consumer Commission complaint.
img: assets/img/5.jpg
importance: 3
category: applications
---

**Links:** [GitHub](https://github.com/spearb0lt/Consumer-Commission-Complaint-Agent) and [Live demo](https://consumer-commission-complaint.streamlit.app/)

A Streamlit-hosted guided-intake agent that turns a consumer's plain-language account of a grievance into a **file-ready Consumer Commission complaint petition**, drafted in Indian legal pleading style, jurisdiction-routed per the 2021 Pecuniary Rules and packaged as a downloadable DOCX and PDF with an e-Daakhil filing checklist.

## Highlights

- A six-step intake wizard that collects the facts of the grievance in plain language.
- Jurisdiction routing that picks the correct District, State or National commission based on the claim value.
- A constrained Gemini pipeline that produces authentic pleading language: numbered "That..." paragraphs, third-person formal voice, inline CPA 2019 citations, `Rs. X/- (Rupees X Only)` notation, annexure labelling and a numbered grounds section.

If the live demo is asleep, give it a moment to wake up on first load.
