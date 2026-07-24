#!/usr/bin/env python3
"""
Local Google Scholar citation updater for al-folio's `_data/citations.yml`.

Why this exists: al-folio's bib.liquid bakes each paper's Google Scholar count into a
static shields.io badge at *build* time, reading the number from `_data/citations.yml`.
The count is NOT fetched from the visitor's browser and NOT fetched by the theme itself,
so the file just has to be correct. The bundled GitHub Action (bin/update_scholar_citations.py
+ .github/workflows/update-citations.yml) tries to fetch via `scholarly` from a GitHub
datacenter IP, which Google Scholar reliably blocks -- so it never updates the file.

This script fetches your PUBLIC Scholar profile from YOUR machine (home IP), parses the
per-paper citation counts, and writes `_data/citations.yml` directly. Google Scholar
sometimes blocks even a home IP (HTTP 403 / robot check); when the scrape fails it falls
back to the MANUAL_PUBLICATIONS values below so the badges still show a real number. Keep
those in sync with your profile and edit them by hand whenever Scholar blocks the read.

Only the Python standard library is required (no scholarly, no pyyaml).

Usage:
    python bin/update_citations_local.py              # try to scrape, else manual, then write
    python bin/update_citations_local.py --manual     # skip scraping, use MANUAL_* values
    python bin/update_citations_local.py --if-scraped # write ONLY if a live scrape succeeds
                                                      # (non-destructive; used by the pre-push hook)
"""
import datetime
import os
import re
import sys
import urllib.error
import urllib.request

SCHOLAR_ID = "rNBVr8gAAAAJ"

# Browser-like headers. Scholar 403s bare requests, so we mimic a real Chrome.
HEADERS = {
    "User-Agent": ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                   "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"),
    "Accept": ("text/html,application/xhtml+xml,application/xml;q=0.9,"
               "image/avif,image/webp,image/apng,*/*;q=0.8"),
    "Accept-Language": "en-US,en;q=0.9",
    "Referer": "https://scholar.google.com/",
    "Upgrade-Insecure-Requests": "1",
}

# ---------------------------------------------------------------------------
# MANUAL FALLBACK: used when Scholar blocks the scrape (403 / robot check) or when
# you run with --manual. Key = google_scholar_id (the `citation_for_view` suffix, the
# same value used in _bibliography/papers.bib). Value = (citation_count, title, year).
# Update these by hand when the numbers change and Scholar is blocking you.
MANUAL_PUBLICATIONS = {
    "u5HHmVD_uO8C": (
        3,
        "Lung Cancer Identification from CT Scans using a Soft-attention enabled "
        "Deep Transfer Learning Model",
        "2025",
    ),
}
# ---------------------------------------------------------------------------

HERE = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.dirname(HERE)
OUT_FILE = os.path.join(REPO_ROOT, "_data", "citations.yml")


def scrape_scholar():
    """Fetch and parse the public profile. Returns {pub_id: (count, title, year)}.

    Raises on block/parse failure so the caller can fall back to MANUAL_*.
    """
    url = f"https://scholar.google.com/citations?user={SCHOLAR_ID}&hl=en&cstart=0&pagesize=100"
    req = urllib.request.Request(url, headers=HEADERS)
    html = urllib.request.urlopen(req, timeout=30).read().decode("utf-8", "ignore")

    if "gsc_a_tr" not in html:
        raise ValueError("robot-check / unexpected page (no publication rows found)")

    # Each publication row exposes citation_for_view=<scholarid>:<pubid>, a title, a year,
    # and a citation-count cell (empty when zero).
    rows = re.findall(
        r'citation_for_view=[\w-]+:([\w-]+)".*?class="gsc_a_at">([^<]*)<'
        r'.*?class="gsc_a_ac[^"]*"[^>]*>(\d*)<'
        r'.*?class="gsc_a_y".*?>(\d{4})?<',
        html,
        re.DOTALL,
    )
    if not rows:
        raise ValueError("robot-check / unexpected page (rows not parseable)")

    pubs = {}
    for pub_id, title, count, year in rows:
        pubs[pub_id] = (int(count) if count else 0, title.strip(), year or "Unknown Year")
    return pubs


def yaml_escape(text):
    """Minimal YAML double-quote escaping for titles."""
    return '"' + text.replace("\\", "\\\\").replace('"', '\\"') + '"'


def write_citations(pubs):
    """pubs: {pub_id: (count, title, year)}. Writes _data/citations.yml."""
    today = datetime.date.today().isoformat()
    lines = ["metadata:", f"  last_updated: '{today}'", "papers:"]
    for pub_id, (count, title, year) in sorted(pubs.items()):
        lines.append(f"  {SCHOLAR_ID}:{pub_id}:")
        lines.append(f"    citations: {count}")
        lines.append(f"    title: {yaml_escape(title)}")
        lines.append(f"    year: '{year}'")
    with open(OUT_FILE, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")
    total = sum(c for c, _, _ in pubs.values())
    print(f"Wrote {OUT_FILE}: {len(pubs)} paper(s), {total} total citation(s).")


def main():
    if "--manual" in sys.argv:
        print("Using MANUAL_PUBLICATIONS (--manual).")
        write_citations(MANUAL_PUBLICATIONS)
        return

    # --if-scraped: only rewrite the file when the live scrape succeeds. On a block we
    # leave _data/citations.yml untouched (never overwrite good data with the fallback).
    if_scraped_only = "--if-scraped" in sys.argv

    try:
        pubs = scrape_scholar()
        if not pubs:
            raise ValueError("no publications parsed")
        write_citations(pubs)
    except (urllib.error.HTTPError, urllib.error.URLError, ValueError, TimeoutError) as e:
        if if_scraped_only:
            print(f"Scholar scrape failed ({e}). Leaving _data/citations.yml unchanged.")
            return
        print(f"Scholar scrape failed ({e}). Falling back to MANUAL_PUBLICATIONS.")
        print("If the numbers are stale, edit MANUAL_PUBLICATIONS at the top of this "
              "script, or re-run later (Scholar rate-limits).")
        write_citations(MANUAL_PUBLICATIONS)


if __name__ == "__main__":
    main()
