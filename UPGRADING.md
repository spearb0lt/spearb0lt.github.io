# Upgrading this site (plain-English guide)

## Short version: you do NOT have to upgrade
This site is "frozen" to specific theme versions (the `= 1.0.x` numbers in `Gemfile`).
It will keep working exactly as it is, forever. Upgrading is **optional** — only do it
if a newer theme version has a feature or fix you actually want.

Your own content is always safe: `_config.yml`, everything in `_data/`, `_pages/`,
`_projects/`, `_news/`, `_bibliography/`, `assets/img/`, `serve.ps1`, `bin/`. Theme
updates never touch these.

The **only** file that overlaps with the theme is `assets/css/main.scss` (it holds a
copy of the theme's stylesheet plus my custom tweaks at the bottom). It's the one file
to glance at after an upgrade.

---

## How to check if there's a newer version
- al-folio releases: https://github.com/alshedivat/al-folio/releases
- The theme's building blocks are Ruby "gems" (e.g. `al_folio_core`). Their latest
  versions are on https://rubygems.org (search `al_folio_core`, `al_folio_cv`, etc.).

You'll see the version you currently use in `Gemfile`, e.g.:
```
gem 'al_folio_core', '= 1.0.11'
```
The `1.0.11` is the version. A newer number there means an upgrade is available.

---

## The simple upgrade recipe (90% of the time)
1. Save your work first: commit everything (`git add -A && git commit -m "before upgrade"`).
2. In `Gemfile`, change the version numbers to the newer ones
   (e.g. `al_folio_core '= 1.0.11'` -> `'= 1.2.0'`). Keep the `plugins:` list in
   `_config.yml` matching.
3. Run the site locally to test:  `.\serve.ps1`   (open http://127.0.0.1:8080/)
4. Look at the pages that use custom styling: **CV**, **About**, **Projects**,
   **Repositories**, **Movies**, **Reads**.
5. If everything looks fine -> push. If only the **CV** or **About** styling looks off,
   the fix is almost always in `assets/css/main.scss` (re-sync the `@use` list at its
   top with the theme's new `main.scss`; keep the "Custom overrides" section at the
   bottom). Ask for help if unsure.

That's it. If step 3 won't build, undo the version change and you're back to normal.

---

## Optional power-user tools (safe to ignore)
The theme ships helper commands you can run inside Docker. They auto-check config and
track your one override file. You do NOT need them for a normal upgrade.
```
docker compose exec jekyll bash -lc "bundle exec al-folio upgrade audit"
docker compose exec jekyll bash -lc "bundle exec al-folio upgrade apply --safe"
docker compose exec jekyll bash -lc "bundle exec al-folio upgrade overrides audit"
```

---

## Rule of thumb
- Nothing broken, no feature you need? **Don't upgrade.**
- Want a new feature/fix? Bump versions, run `.\serve.ps1`, check the pages, push.
- Stuck? The only tricky file is `assets/css/main.scss`.




-----------




## What's safe across upgrades (your content — leave it, it just works)
_config.yml, everything in _data/ (cv.yml, movies.yml, reads.yml, repositories.yml, socials.yml…), your _pages/*, _projects/*, _news/*, _bibliography/papers.bib, assets/img/*, serve.ps1, bin/add_movies.py, BingSiteAuth.xml. Also all the custom CSS/HTML I embedded inside page bodies (the <<>style>> blocks and suggestion forms in about/movies/books/reads/repositories) — those live in your files, so upgrades don't touch them.

 one thing to manage: assets/css/main.scss
It's a local copy of the theme's stylesheet (its @use import list) plus your custom section at the bottom. This is the only "override," and al-folio has a built-in system to track exactly this.

Upgrade playbook (run the CLI inside Docker, since you don't have Ruby locally)
Commit everything first, ideally on a new branch, so you can diff/rollback.
Bump the version pins in Gemfile (currently al_folio_core '= 1.0.11', al_folio_cv '= 1.0.0', al_icons '= 1.0.0', al_search '= 1.0.2', al_math '= 1.0.1', al_citations '= 1.0.1') to the new releases, and keep the plugins: list in _config.yml in sync.
Start the container, then run these inside it:

docker compose exec jekyll bash -lc "bundle update"
docker compose exec jekyll bash -lc "bundle exec al-folio upgrade audit"          # flags config-contract issues (blocking)
docker compose exec jekyll bash -lc "bundle exec al-folio upgrade apply --safe"   # safe automatic codemods
docker compose exec jekyll bash -lc "bundle exec al-folio upgrade overrides audit" # records your override -> .al-folio-overrides.yml (commit it)
docker compose exec jekyll bash -lc "bundle exec al-folio upgrade overrides diff assets/css/main.scss"
If step 5's diff shows the gem's main.scss changed, re-sync only the @use block at the top of your assets/css/main.scss to match the new version — keep your "Custom overrides" section at the bottom untouched. (I left a comment in that file saying exactly this.)
Rebuild (.\serve.ps1) and eyeball the pages below.
Post-upgrade watch-list (re-check these, since they lean on theme classes/templates)
CV: location centering, removed section bullets (#experience + .card li …), the Projects divider, and the right-side .edu-score. These also rely on al_folio_cv outputting area/location as raw HTML (so the <br> and <span class="edu-score"> in cv.yml render). If a future al_folio_cv changes its template, tweak those.
About: .more-info centering + the profile-image aspect-ratio (in about.md's <>style>).
Movies/Books/Reads/Repositories: self-contained, should be fine.
For a major jump (v1 → v2) read the release notes — there can be breaking changes (e.g., Bootstrap-compat is slated for removal in v2). Minor/patch bumps are low-risk with the flow above.

Want me to run overrides audit now to create the baseline .al-folio-overrides.yml (so future diffs work), or leave upgrading entirely to you when the time comes?

## My 4 questions
1. Are all my changes in main.scss? No.
Your changes are spread across many of your own files (like _data/cv.yml, _data/movies.yml, your pages, images, etc.). Those are 100% yours and never clash with theme updates.

main.scss is special for one reason only: it's the single file where I had to keep a copy of one of the theme's own files (to add the CV/about styling). So it's the only file that "overlaps" with the theme. That's why it's the only one to watch during an upgrade — not because your changes live there.

Think of it like this:

Your content files = your furniture. Safe, always yours.
main.scss = the one wall you repainted that the landlord (theme) also owns. If the landlord renovates that wall, you check your paint still fits.
2. Branch vs main, and "bump the version pins"

Branch: just a safety net. You can push straight to main — it's your site, totally fine. A branch is only "safer" because if the upgrade breaks something, your live site stays untouched until you're happy. For a personal site, doing it on main (after committing first) is perfectly OK.
"Bump the version pins": In your Gemfile there are lines like gem 'al_folio_core', '= 1.0.11'. The 1.0.11 is the version number ("pin" = locked to that version). "Bump" just means change that number to a newer one (e.g., 1.0.11 → 1.2.0) to pull in the update. That's literally it.
3. Steps 3–5 (the commands) — why?
Those were optional helper tools the theme ships. Honestly, for a beginner the simple upgrade is just:

Change the version numbers in Gemfile.
Run your site locally (.\serve.ps1) and look at it.
If it looks fine, push. If something looks off (most likely only the CV/about styling), tell me and I'll fix main.scss.
The commands I listed (audit, apply --safe, overrides diff) are convenience tools that auto-check and auto-fix small things. You can skip them and just eyeball the site. They're "nice to have," not required.

4. What's .al-folio-overrides.yml / the "baseline"?
It's a tiny bookkeeping file that would record "Shubhro keeps his own copy of main.scss." Its only purpose: later, the helper tool can tell you "the theme changed its version of this file, go check yours." It's an optional convenience tied to those optional commands. You don't need it unless you use them.