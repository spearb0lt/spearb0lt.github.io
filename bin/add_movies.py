#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Add movies to _data/movies.yml automatically.

You only supply a movie name (and the genre bucket it should go in). The script
looks the movie up on IMDb, downloads its poster into assets/img/movies/, and
appends an entry (title, poster, imdb) to _data/movies.yml. Re-running is safe:
movies already present (matched by IMDb id) are skipped.

USAGE
-----
1) Batch mode (recommended): create a file `movies_to_add.txt` in the repo root
   with one movie per line, in the form:

       Title | Genre
       Goodfellas | Crime
       Back to the Future | Sci-Fi
       The Apartment (1960) | Romance      # add a year to disambiguate

   Lines that are blank or start with '#' are ignored. Then run:

       python bin/add_movies.py

2) One-off mode:

       python bin/add_movies.py "Goodfellas" "Crime"

No API key is required. Posters come from IMDb's public suggestion endpoint.
"""
import io
import json
import os
import re
import sys
import time
import urllib.parse
import urllib.request

try:
    from PIL import Image
    HAVE_PIL = True
except Exception:
    HAVE_PIL = False

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MOVIES_YML = os.path.join(ROOT, "_data", "movies.yml")
POSTER_DIR = os.path.join(ROOT, "assets", "img", "movies")
INPUT_TXT = os.path.join(ROOT, "movies_to_add.txt")
UA = "Mozilla/5.0 (movies-adder; contact shubhro2004@gmail.com)"
POSTER_WIDTH = 420  # downscale posters to this width to keep the repo lean

HEADER = """# Movies and shows I have watched and liked, grouped by genre.
#
# You can edit this by hand, but the easy way to add movies is:
#   1. Add lines to movies_to_add.txt in the repo root:  Title | Genre
#   2. Run:  python bin/add_movies.py
# That looks up the IMDb link, downloads the poster, and appends it here.
#
# Hovering a poster shows the title; clicking opens its IMDb page.
"""

MOVIE_TYPES = {"feature", "tv series", "tv mini-series", "tvSeries",
               "tvMiniSeries", "tvMovie", "video", "short"}


def slugify(title):
    s = re.sub(r"[^a-z0-9]+", "_", title.lower()).strip("_")
    return s or "movie"


def yq(s):
    """Quote a scalar for YAML safely (double-quoted)."""
    return '"' + str(s).replace("\\", "\\\\").replace('"', '\\"') + '"'


# ---- minimal movies.yml parser (title/poster/imdb per genre) ----
def load_movies():
    genres = []  # list of {name, movies:[{title,poster,imdb}]}
    if not os.path.exists(MOVIES_YML):
        return genres
    cur = None
    m = None
    for raw in open(MOVIES_YML, encoding="utf-8"):
        line = raw.rstrip("\n")
        s = line.strip()
        if not s or s.startswith("#"):
            continue
        mn = re.match(r"^\s*-\s*name:\s*(.*)$", line)
        if mn:
            name = mn.group(1).strip().strip('"').strip("'")
            cur = {"name": name, "movies": []}
            genres.append(cur)
            m = None
            continue
        mt = re.match(r"^\s*-\s*title:\s*(.*)$", line)
        if mt and cur is not None:
            m = {"title": mt.group(1).strip().strip('"').strip("'")}
            cur["movies"].append(m)
            continue
        mp = re.match(r"^\s*poster:\s*(.*)$", line)
        if mp and m is not None:
            m["poster"] = mp.group(1).strip().strip('"').strip("'")
            continue
        mi = re.match(r"^\s*imdb:\s*(.*)$", line)
        if mi and m is not None:
            m["imdb"] = mi.group(1).strip().strip('"').strip("'")
            continue
    return genres


def write_movies(genres):
    out = [HEADER, "", "genres:"]
    for g in genres:
        out.append(f"  - name: {yq(g['name'])}")
        out.append("    movies:")
        if not g["movies"]:
            out.append("      []")
        for mv in g["movies"]:
            out.append(f"      - title: {yq(mv['title'])}")
            out.append(f"        poster: {mv['poster']}")
            out.append(f"        imdb: {mv['imdb']}")
        out.append("")
    with open(MOVIES_YML, "w", encoding="utf-8", newline="\n") as f:
        f.write("\n".join(out).rstrip() + "\n")


def imdb_lookup(query, want_year=None):
    q = urllib.parse.quote(query)
    url = f"https://v3.sg.media-imdb.com/suggestion/x/{q}.json?includeVideos=0"
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "application/json"})
    with urllib.request.urlopen(req, timeout=25) as r:
        data = json.load(r)
    cands = [x for x in data.get("d", []) if str(x.get("id", "")).startswith("tt") and x.get("i")]
    if not cands:
        return None
    if want_year:
        for x in cands:
            if str(x.get("y")) == str(want_year):
                return x
    for x in cands:
        if (x.get("q") or "").lower() in {"feature", "tv series", "tv mini-series", "tvmovie"}:
            return x
    return cands[0]


def download_poster(image_url, slug):
    req = urllib.request.Request(image_url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=40) as r:
        raw = r.read()
    path = os.path.join(POSTER_DIR, slug + ".jpg")
    os.makedirs(POSTER_DIR, exist_ok=True)
    if HAVE_PIL:
        im = Image.open(io.BytesIO(raw)).convert("RGB")
        w, h = im.size
        if w > POSTER_WIDTH:
            im = im.resize((POSTER_WIDTH, int(h * POSTER_WIDTH / w)), Image.LANCZOS)
        im.save(path, "JPEG", quality=85)
    else:
        with open(path, "wb") as f:
            f.write(raw)
    return "assets/img/movies/" + slug + ".jpg"


def parse_input_lines():
    items = []
    if os.path.exists(INPUT_TXT):
        for raw in open(INPUT_TXT, encoding="utf-8"):
            s = raw.strip()
            if not s or s.startswith("#"):
                continue
            if "|" in s:
                title, genre = s.split("|", 1)
                items.append((title.strip(), genre.strip()))
            else:
                items.append((s, "Uncategorised"))
    return items


def main():
    if len(sys.argv) >= 3:
        items = [(sys.argv[1], sys.argv[2])]
    elif len(sys.argv) == 2:
        items = [(sys.argv[1], "Uncategorised")]
    else:
        items = parse_input_lines()

    if not items:
        print("Nothing to add. Pass a title/genre, or fill movies_to_add.txt.")
        return

    genres = load_movies()
    have_ids = {re.search(r"tt\d+", mv.get("imdb", "")).group(0)
                for g in genres for mv in g["movies"]
                if mv.get("imdb") and re.search(r"tt\d+", mv["imdb"])}
    by_name = {g["name"].lower(): g for g in genres}

    added = skipped = failed = 0
    for title, genre in items:
        ym = re.search(r"\((\d{4})\)\s*$", title)
        year = ym.group(1) if ym else None
        clean_title = re.sub(r"\s*\(\d{4}\)\s*$", "", title).strip()
        try:
            hit = imdb_lookup(clean_title, year)
        except Exception as e:
            print(f"  FAIL  {title}: lookup error {e}"); failed += 1; continue
        if not hit:
            print(f"  FAIL  {title}: no IMDb match"); failed += 1; continue
        ttid = hit["id"]
        if ttid in have_ids:
            print(f"  skip  {hit.get('l')} ({ttid}) already present"); skipped += 1; continue
        try:
            poster = download_poster(hit["i"]["imageUrl"], slugify(hit.get("l", clean_title)))
        except Exception as e:
            print(f"  FAIL  {title}: poster download {e}"); failed += 1; continue
        entry = {"title": hit.get("l", clean_title),
                 "poster": poster,
                 "imdb": f"https://www.imdb.com/title/{ttid}/"}
        g = by_name.get(genre.lower())
        if g is None:
            g = {"name": genre, "movies": []}
            genres.append(g); by_name[genre.lower()] = g
        g["movies"].append(entry)
        have_ids.add(ttid)
        print(f"  OK    {entry['title']} ({hit.get('y')}) -> {genre}")
        added += 1
        time.sleep(0.3)

    write_movies(genres)
    print(f"\nDone. added={added} skipped={skipped} failed={failed}. Wrote {MOVIES_YML}")


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    main()
