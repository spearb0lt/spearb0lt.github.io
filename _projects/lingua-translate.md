---
layout: page
title: Multilanguage On-Device Translator
description: Translation and speech for 61 languages, running on local weights first and falling back to free services only when it has to.
img: assets/img/project/lingua-translate.jpg
importance: 1
category: speech
tags: [nlp, speech, machine-translation, transliteration, on-device, self-hosted, evaluation, fastapi, transformers, whisper, live-demo]
---

{% assign pt = site.data.project_tags %}{% assign all_families = 'domain,method,stack,meta' | split: ',' %}{% assign fams = pt.families_on.project_pages | default: all_families %}{% if pt.enabled and pt.show_on.project_pages and page.tags %}<div class="proj-tags proj-tags-page pt-style-{{ pt.style.project_pages | default: 'soft' }}">{% for t in page.tags %}{% assign fam = pt.map[t] | default: pt.default_family %}{% if fams contains fam %}<span class="proj-tag pt-{{ fam }} pt-tag-{{ t | slugify }}">{{ t }}</span>{% endif %}{% endfor %}</div>{% endif %}

**Links:** [live demo (lite edition)](https://lingua-translate-smoky.vercel.app) and [GitHub repository](https://github.com/spearb0lt/Lingua-Translate)

**Lingua** translates between 61 Indian and world languages, built to run on your own hardware first and to fall back to free services only when it has to. Four things separate it from a thin wrapper around a translation API.

## It reads romanized Indic text

`mera naam rahul hai` is Hindi typed in Latin letters. Lingua detects that, converts it to `मेरा नाम राहुल है`, shows you what it understood, and translates from there. Fixing the script first is not cosmetic, and measured against Google's own endpoint it is strictly better:

| input                                  | sent as typed                  | sent as native script   |
| -------------------------------------- | ------------------------------ | ----------------------- |
| `ami tomake bhalobashi` (bn to en)     | returned untranslated          | **i love you**          |
| `naan unnai kaadhalikkiren` (ta to hi) | transliterated, not translated | **मुझे तुमसे प्यार है** |
| `amar nam gobindo` (as to en)          | `love me gobindo`              | **Our name is Govinda** |

That last row is the exact example Google's own UI returns for `sl=as&tl=en`.

## It prefers local weights

IndicTrans2 (MIT) for English to and from 22 Indian languages and Indic to Indic, NLLB-200 for everything else, and a two-hop English pivot for Indic to foreign, which measurably beats NLLB direct. All run on a 4 GB laptop GPU or CPU only. Every request walks a tier ladder and the response records which rung answered:

```
Tier 0  LOCAL      IndicTrans2 · pivot_en · NLLB-200   open weights, on your machine
Tier 1  FREE_WEB   Google gtx · Google clients5        keyless, no account
Tier 2  FREE_API   MyMemory · LibreTranslate           free tiers, documented
Tier 3  FREEMIUM   only if you configure a key         off by default
```

The lowest tier that can serve the pair wins. Capping it per request (`max_tier: "LOCAL"`) gives a strictly offline translation or an error.

## Telling apart languages that share a script

Devanagari carries Hindi, Marathi, Nepali, Sanskrit, Maithili, Bodo, Dogri and Konkani; Bengali script carries Bengali and Assamese; Arabic script carries Urdu, Sindhi and Kashmiri. Assuming the most common one is not a rounding error, it changes meaning. `माझे नाव राहुल आहे` read as Hindi becomes "My boat is Rahul" and read as Marathi becomes "My name is Rahul", because नाव is _boat_ in Hindi and _name_ in Marathi.

Disambiguation uses two signals. Signature characters are decisive: Assamese writes `ৰ` and `ৱ` where Bengali writes `র` and `ব`, and Sindhi and Kashmiri each have letters Urdu never uses. Otherwise it falls back to function-word lexicons, copulas and pronouns, because they appear in nearly every sentence and rarely cross over. It reports honest confidence and defers to a provider that can detect for itself below a threshold. 11 of 11 languages are now identified correctly, offline, with no extra dependency; before this, 5 of 6 Devanagari languages were silently read as Hindi.

## It checks its own output

Small models garble proper nouns across scripts. NLLB-600M renders "Rahul" into Japanese as `ラहुल`, Devanagari spliced into katakana, and does it even when handed clean English input, so no amount of routing fixes it. A sanity check catches it: a translation whose target script is Japanese should not contain Devanagari. Latin is always allowed, since names, acronyms and loanwords appear in Latin letters in every language, Japanese may mix kana with Han, Korean may mix Hangul with Han, and anything under 2% of characters is treated as incidental. A wrong-script result falls through to an engine that gets it right rather than being served.

It can also estimate its own accuracy. Ask for a check and the translation is fed back through a _different_ engine and scored with chrF, an F-score over character n-grams chosen because it needs no tokeniser, which matters when the languages include Japanese and Tamil. `best_of: 3` runs three engines and keeps the highest scorer, with one grader scoring every candidate, because grading each with a different engine is not a comparison.

## Coverage, measured rather than assumed

|                       | total  | Indian (of 23) | foreign (of 38) |
| --------------------- | ------ | -------------- | --------------- |
| translation           | **61** | 23             | 38              |
| speech-to-text        | **60** | 23             | 37              |
| text-to-speech        | **53** | 15             | 38              |
| of which work offline | 26     | 13             | 13              |

Speech-to-text chains two engines. Whisper is the only one that can _identify_ an unknown language, so it always runs first on auto-detect; IndicConformer-600M covers all 22 scheduled languages, including the eight Whisper cannot transcribe at all, and is more accurate on the rest. Text-to-speech chains three, with MMS-TTS running fully offline and providing the only voice that exists for Assamese, Odia and Maithili. Eight languages have no voice anywhere public, which is a gap in what has been built in the world rather than in the app.

## Things that were in the way

**Google's free endpoint fingerprints the TLS handshake, not the headers.** It returns HTTP 429 to `httpx` and `requests` even with browser-identical headers, while `curl` with the same headers gets 200. Header spoofing does not fix it, which is the single thing most tutorials get wrong. The fix is `curl_cffi`, which presents a real browser handshake and has wheels for both `win_amd64` and `manylinux aarch64`.

**transformers 5 breaks IndicTrans2 at import.** It moved `PreTrainedTokenizerBase` out of `transformers.tokenization_utils`, and both IndicTransToolkit and IndicTrans2's own modelling file still import it from there, so the failure happens before any download. The requirements pin `transformers>=4.44,<5`.

The engine knows nothing about HTTP: the full edition and the network-only lite edition are both thin shells over the same `Router`, and adding a provider is one class and one line.
