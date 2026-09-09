---
layout: page
title: Universal Human Communication Interface (UHCI)
description: An offline communication app for Deaf and non-speaking users, with twelve input channels feeding one message box.
img: assets/img/project/uhci-signbridge.jpg
importance: 1
category: cv
tags: [cv, audio, accessibility, hci, sign-language, speech, on-device, real-time, mediapipe]
---

{% assign pt = site.data.project_tags %}{% assign all_families = 'domain,method,stack,meta' | split: ',' %}{% assign fams = pt.families_on.project_pages | default: all_families %}{% if pt.enabled and pt.show_on.project_pages and page.tags %}<div class="proj-tags proj-tags-page pt-style-{{ pt.style.project_pages | default: 'soft' }}">{% for t in page.tags %}{% assign fam = pt.map[t] | default: pt.default_family %}{% if fams contains fam %}<span class="proj-tag pt-{{ fam }} pt-tag-{{ t | slugify }}">{{ t }}</span>{% endif %}{% endfor %}</div>{% endif %}

**Links:** [GitHub repository](https://github.com/spearb0lt/Universal-Human-Communication-Interface-UHCI)

A local, offline communication app (shipped under the name **SignBridge**) for Deaf and non-speaking people. Twelve different input channels (morse keyed by a blink or a tap, sign language, lip reading, eye gaze, air-writing, a head-driven cursor, braille held up to the camera) all feed one message box, which can then be spoken aloud, flashed as morse, or typed straight into WhatsApp or Notepad.

**Everything runs on your machine.** No API keys, no accounts, no network at runtime. Every model is open-weight, downloaded once, and can be deleted. Nothing the user says, signs or types leaves the computer. The codebase is roughly 129 modules and 38,600 lines, covered by 1,044 passing tests.

## Getting words out: twelve input channels

- **Morse** through 12 different keys: blink, wink, blink-and-hold, lips, fist, pinch, index finger, eyebrow, nod, a torch shone at the camera, an audible tap, or a lip pucker.
- **Sign language** over a 2,000-word ASL vocabulary, plus one-handed **fingerspelling** for names.
- **Lip reading**, **eye gaze** (16 screen regions, two steps per letter), **air-writing** by pinching and drawing in the air, and a **head-driven cursor** for an on-screen keyboard.
- **Hand gestures** (7 built in, plus any the user teaches it in about ten minutes), two-arm **semaphore** for letters and numbers, **braille** cards held up to the camera (Grade 1 and full UEB Grade 2), and **facial expressions** that mark a question or a wh-question.

## Getting words in, so it is a conversation

Speech-to-text turns a spoken sentence into text in about 0.5 s, a live transcript runs roughly 0.8 s behind the speaker without ever rewriting itself, and text-to-speech (Kokoro, with an instant system-voice fallback) speaks the reply. Outgoing messages can also be played back as sign-language clips, morse, braille, semaphore diagrams or NATO spelling.

## Measured, not quoted

Every performance number in the repository was measured on the development machine (a Windows 11 laptop with an RTX 3050 and a 640×480 webcam), not taken from a paper:

- Capture holds **30.4 fps** with face, hands and pose tracked together.
- Sign recognition reaches **65.8% top-1**; fingerspelling **96.2%** across 26 letters.
- Air-writing recognised **180/180** letters and digits across five pinch styles.
- Braille Grade 2 decoding is **99.9951%** exact over 370,105 words checked against liblouis 3.38.0, with all 18 failures listed.
- Gaze produced 0 false selections in 120 s of resting and 48/48 deliberate selections.

## Architecture

Heavy models sit behind a `Protocol` and run as persistent subprocess workers in a second virtual environment, so the GUI environment stays light and a model crash cannot take the window down. Qt widgets are only ever touched from the GUI thread; anything crossing back from a worker is posted through a dedicated helper. The perception layer, one decoder module per input channel, the sign and lip-reading stacks, speech, output formats and the PySide6 UI are each isolated packages.
