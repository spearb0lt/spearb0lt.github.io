---
layout: page
title: Lichess Essentials
description: Five chess tools that fix the things I kept running into as a long-time Lichess user, published as six PyPI packages and hosted live.
img: assets/img/project/black-white-plastic-chess.webp
importance: 1
category: open-source/packages
tags: [chess, tools, pypi, self-hosted, stockfish, live-demo]
---

{% assign pt = site.data.project_tags %}{% assign all_families = 'domain,method,stack,meta' | split: ',' %}{% assign fams = pt.families_on.project_pages | default: all_families %}{% if pt.enabled and pt.show_on.project_pages and page.tags %}<div class="proj-tags proj-tags-page pt-style-{{ pt.style.project_pages | default: 'soft' }}">{% for t in page.tags %}{% assign fam = pt.map[t] | default: pt.default_family %}{% if fams contains fam %}<span class="proj-tag pt-{{ fam }} pt-tag-{{ t | slugify }}">{{ t }}</span>{% endif %}{% endfor %}</div>{% endif %}

**Links:** [GitHub repository](https://github.com/spearb0lt/Lichess-Essentials) and [`lichess-essentials` on PyPI](https://pypi.org/project/lichess-essentials/)

Five tools that fix the things I kept running into as a long-time Lichess user. Built for my own use, open-sourced in case they are useful to anyone else, published as six packages on PyPI and running live on one free Oracle Cloud ARM machine behind real HTTPS.

## Try them live

| App                                                                     | Access         |
| ----------------------------------------------------------------------- | -------------- |
| [Lichess Study to PDF](https://study.lichess-essentials.duckdns.org)    | open, no login |
| [ChessAnalyzer](https://analyzer.lichess-essentials.duckdns.org)        | shared login   |
| [Player-Prepper](https://prepper.lichess-essentials.duckdns.org)        | shared login   |
| [Repertoire-Creator](https://repertoire.lichess-essentials.duckdns.org) | shared login   |
| [Weakness-Report](https://weakness.lichess-essentials.duckdns.org)      | shared login   |

The four gated apps share one HTTP Basic login, `test` / `testpassword1234@`, published deliberately. The gate keeps crawlers and automated traffic off a free-tier box rather than securing anything, so the credentials are meant to be used. Your browser will ask for them the moment you open one of those four.

## The five apps

**Lichess Study to PDF** turns a study into a typeset chess book or a step-through PDF, every sideline, comment and annotation included, plus a browser interface with a live engine eval bar and a board you can play your own moves on. It imports private studies without a token.

**ChessAnalyzer** reviews any game with a local engine, whether it comes from Lichess, from Chess.com or from a PGN you paste. Accuracy and move labels are reported on both the Lichess and a Chess.com-style scale, with the rule behind every label written down and shown in the app. It has an eval graph, ranked engine lines, mouse-wheel stepping, and a live mode that follows a game while it is still being played, including Chess.com live games, which no documented API exposes. You can also arrange the pieces by hand for a game happening in front of you, say who is to move, and get the evaluation.

**Player-Prepper** scouts an opponent from their own games on either site: what they play per colour, where their own results say they leak points, and, measured against your repertoire, every position they steer into that you have no answer for, ranked by how many of their games would put you there. Its exploit tab crosses their habits with what the engine says you get, on an opportunity score whose factors you switch on and off, and it prints the lot as a prep sheet.

**Weakness-Report** reviews a few hundred of your own games and finds what you are actually bad at. It slices your history by the kind of position you were in (queenless middlegames, opposite-side castling, under thirty seconds, rook endings) and ranks each by how much it costs you _beyond your own average_, which is the difference between a true claim and a useful one.

**Repertoire-Creator** builds an opening repertoire locally: play or type the lines, annotate them, with a live eval bar and ranked engine suggestions, then publish it to Lichess as a study, drill yourself on it, or export it as a PDF. It knows which side you play, so it finds the positions you have no answer for. Its universal mode drops chapters entirely: record sequences, and everything you have written down becomes one book keyed by position that tells you your own move as you play, or says _gap_.

## How the five fit together

The apps read each other's folders and never write to them, so any of them can run beside any other. Study to PDF is installed as a library, which is how Repertoire-Creator, Player-Prepper and Weakness-Report get their engine ladder and PDF layouts instead of each carrying a second copy. Weakness-Report reads its review rules (accuracy, move labels, where the middlegame starts) from ChessAnalyzer, so that a game means the same thing in both apps: a weakness report _is_ an aggregation of that app's review, and the two are meant to agree.

Optional features are optional extras rather than a dependency everyone pays for, and each app names the command to run when you ask for something it has not got. PDF export from Repertoire-Creator, engine suggestions in Player-Prepper, board diagrams in a Weakness-Report and cloud-eval fallback in ChessAnalyzer are each their own extra.

## Packaging and release

Six packages ship to PyPI: the `lichess-essentials` meta-package that installs all five and gives you five commands, plus each app on its own for anyone who wants only one. Installed from pip there is no repository to sit beside, so each app uses the normal per-user data folder for the platform and prints its own path in the startup banner.

Releases run only on a version tag, so pushing to `main` changes nothing on PyPI, and the packages you did not touch are skipped rather than failing. Authentication is [Trusted Publishing](https://docs.pypi.org/trusted-publishers/) rather than an API token: GitHub proves the workflow's identity to PyPI over OpenID Connect and PyPI issues a short-lived token scoped to one project, so no long-lived credential lives in the repository or in GitHub secrets.

## Deployment, with its caveats stated

There are no user accounts behind that shared login, so saved data is shared between visitors too, and anything you put in should be treated as public. Do not paste a Lichess token you care about either, because four of the apps hold a pasted token in a process-wide global that would be used by every other visitor until that app restarts. Player-Prepper's scouting reports and Weakness-Report's history are gitignored: a report about a named person, and a page of numbers about how you play, are not things to publish by accident.

An engine is yours to supply. Install Stockfish from your package manager, put it on `PATH`, or point `STOCKFISH_PATH` at it, and ChessAnalyzer can also download one for you from its Engines tab. A LaTeX install unlocks the typeset chess-book export, and each app's startup banner reports whether it found them.
