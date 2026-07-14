# Content Harvest Pipeline Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Daily automated harvest of YouTube/article/podcast/X content into per-item markdown notes under `brain/`, driven by a cloud-scheduled Claude agent.

**Architecture:** Python package `harvest/` does deterministic work (feed parsing, dedup state, caption/audio/article extraction, note rendering). Fetchers write raw items to `staging/*.json`. The scheduled agent (per `RUNBOOK.md`) summarizes each staged item and runs `harvest.finalize`, which writes the final note + daily index and only then marks the item seen. Per-source failures are isolated; failed items stay unstaged/unseen and retry next run.

**Tech Stack:** Python 3.11+, feedparser, PyYAML, requests, yt-dlp (CLI), ffmpeg (CLI), OpenAI Whisper API (`openai` lib), Playwright (Python), defuddle-cli via npx, pytest.

## Global Constraints

- Repo root: `/Users/jjchambers/Intellimark/ticket-content-scrape`; Obsidian vault root is `brain/` (spec: `brain/docs/specs/2026-07-06-content-harvest-pipeline-design.md`).
- Note frontmatter fields, exactly: `title`, `author`, `source`, `url`, `type`, `date`, `tags`.
- Note paths: `brain/{youtube,articles,podcasts,x}/YYYY-MM-DD-slug.md`; daily index `brain/YYYY-MM-DD.md`.
- First sighting of a source: seed all current feed item IDs as seen, process none (spec "First-run seeding", default N=0).
- Whisper request limit: chunk audio above 24MB (spec says 25MB API limit; use 24MB threshold for headroom).
- Credentials (X login `X_USERNAME`/`X_PASSWORD`, `OPENAI_API_KEY`) come ONLY from environment/agent secrets. Never in repo, spec, code, or commits.
- `staging/` and `__pycache__/` are gitignored; `sources-state.json` IS committed (it is the dedup memory).
- An item is marked seen ONLY when its final note is written (finalize step), never at fetch time.

---

### Task 1: Scaffolding

**Files:**
- Create: `requirements.txt`, `sources.yaml`, `.gitignore`, `harvest/__init__.py`, `tests/__init__.py`

**Interfaces:**
- Produces: `sources.yaml` schema consumed by Task 6 orchestrator: top-level keys `youtube` (list of channel IDs), `articles` (list of RSS URLs), `podcasts` (list of RSS URLs), `x` (list of account handles).

- [ ] **Step 1: Write files**

`requirements.txt`:
```
feedparser>=6.0
PyYAML>=6.0
requests>=2.31
openai>=1.30
playwright>=1.44
pytest>=8.0
```

`sources.yaml` (starter, empty lists — user adds sources later):
```yaml
# Subscription list for the daily harvest. Add entries; first run of a new
# source seeds its history as "seen" and only future items are processed.
youtube: []      # channel IDs, e.g. UCXuqSBlHAE6Xw-yeJA0Tunw
articles: []     # RSS feed URLs
podcasts: []     # RSS feed URLs
x: []            # account handles, e.g. karpathy
```

`.gitignore`:
```
__pycache__/
*.pyc
staging/
.pytest_cache/
.venv/
.env
```

`harvest/__init__.py` and `tests/__init__.py`: empty files.

- [ ] **Step 2: Verify pytest runs**

Run: `cd /Users/jjchambers/Intellimark/ticket-content-scrape && python3 -m venv .venv && .venv/bin/pip install -r requirements.txt && .venv/bin/pytest`
Expected: `no tests ran` (exit code 5 is fine at this stage).

- [ ] **Step 3: Commit**

```bash
git add requirements.txt sources.yaml .gitignore harvest/__init__.py tests/__init__.py
git commit -m "feat: scaffold harvest package"
```

---

### Task 2: Dedup state module

**Files:**
- Create: `harvest/state.py`
- Test: `tests/test_state.py`

**Interfaces:**
- Produces: `load_state(path) -> dict`, `save_state(state, path)`, `new_items(state, source_key: str, current_ids: list[str]) -> list[str]` (mutates state on first sighting), `mark_seen(state, source_key, item_id)`. State shape: `{"sources": {"<source_key>": {"seen": ["id", ...]}}}`. `source_key` = feed URL / channel ID / handle verbatim.

- [ ] **Step 1: Write failing tests**

`tests/test_state.py`:
```python
from harvest.state import load_state, save_state, new_items, mark_seen


def test_load_missing_returns_empty(tmp_path):
    assert load_state(tmp_path / "nope.json") == {"sources": {}}


def test_first_sighting_seeds_all_as_seen_processes_none():
    state = {"sources": {}}
    fresh = new_items(state, "feedA", ["1", "2", "3"])
    assert fresh == []
    assert state["sources"]["feedA"]["seen"] == ["1", "2", "3"]


def test_known_source_returns_only_unseen():
    state = {"sources": {"feedA": {"seen": ["1"]}}}
    assert new_items(state, "feedA", ["1", "2"]) == ["2"]
    # not marked seen until finalize
    assert state["sources"]["feedA"]["seen"] == ["1"]


def test_mark_seen_idempotent(tmp_path):
    state = {"sources": {"feedA": {"seen": []}}}
    mark_seen(state, "feedA", "2")
    mark_seen(state, "feedA", "2")
    assert state["sources"]["feedA"]["seen"] == ["2"]
    p = tmp_path / "s.json"
    save_state(state, p)
    assert load_state(p) == state
```

- [ ] **Step 2: Run to verify failure**

Run: `.venv/bin/pytest tests/test_state.py -v`
Expected: FAIL — `ModuleNotFoundError: harvest.state`

- [ ] **Step 3: Implement**

`harvest/state.py`:
```python
import json
from pathlib import Path


def load_state(path):
    p = Path(path)
    if p.exists():
        return json.loads(p.read_text())
    return {"sources": {}}


def save_state(state, path):
    Path(path).write_text(json.dumps(state, indent=2, sort_keys=True) + "\n")


def new_items(state, source_key, current_ids):
    """IDs to process. First sighting seeds all as seen and returns []."""
    src = state["sources"].get(source_key)
    if src is None:
        state["sources"][source_key] = {"seen": list(current_ids)}
        return []
    seen = set(src["seen"])
    return [i for i in current_ids if i not in seen]


def mark_seen(state, source_key, item_id):
    src = state["sources"].setdefault(source_key, {"seen": []})
    if item_id not in src["seen"]:
        src["seen"].append(item_id)
```

- [ ] **Step 4: Run to verify pass**

Run: `.venv/bin/pytest tests/test_state.py -v` — Expected: 4 PASS

- [ ] **Step 5: Commit**

```bash
git add harvest/state.py tests/test_state.py
git commit -m "feat: dedup state with first-run seeding"
```

---

### Task 3: Note writer

**Files:**
- Create: `harvest/notes.py`
- Test: `tests/test_notes.py`

**Interfaces:**
- Consumes: nothing internal.
- Produces: `slugify(title: str) -> str`; `render_note(item: dict, summary_md: str) -> str`; `write_note(item, summary_md, vault_dir) -> Path` (also updates daily index). `item` dict keys: `id, type, title, author, source, url, published (YYYY-MM-DD), content`. `type` ∈ `youtube|article|podcast|x`; folder map: youtube→youtube, article→articles, podcast→podcasts, x→x.

- [ ] **Step 1: Write failing tests**

`tests/test_notes.py`:
```python
from harvest.notes import slugify, render_note, write_note

ITEM = {
    "id": "abc123", "type": "article", "title": "Big News: AI & Tickets!",
    "author": "Jane Doe", "source": "https://example.com/feed",
    "url": "https://example.com/post", "published": "2026-07-06",
    "content": "Full article text here.",
}


def test_slugify():
    assert slugify("Big News: AI & Tickets!") == "big-news-ai-tickets"


def test_render_note_frontmatter_and_sections():
    md = render_note(ITEM, "One-line summary.\n\n- point")
    assert md.startswith("---\n")
    for line in ['title: "Big News: AI & Tickets!"', 'author: "Jane Doe"',
                 "type: article", "date: 2026-07-06", "tags: []"]:
        assert line in md
    assert "## Summary" in md and "## Transcript" in md
    assert "Full article text here." in md


def test_write_note_path_and_daily_index(tmp_path):
    p = write_note(ITEM, "Summary.", tmp_path)
    assert p == tmp_path / "articles" / "2026-07-06-big-news-ai-tickets.md"
    assert p.exists()
    index = (tmp_path / "2026-07-06.md").read_text()
    assert "[[articles/2026-07-06-big-news-ai-tickets|Big News: AI & Tickets!]]" in index
    # second write must not duplicate the index line
    write_note(ITEM, "Summary.", tmp_path)
    assert (tmp_path / "2026-07-06.md").read_text().count("big-news-ai-tickets") == 1
```

- [ ] **Step 2: Run to verify failure**

Run: `.venv/bin/pytest tests/test_notes.py -v` — Expected: FAIL, module not found

- [ ] **Step 3: Implement**

`harvest/notes.py`:
```python
import re
from pathlib import Path

FOLDERS = {"youtube": "youtube", "article": "articles",
           "podcast": "podcasts", "x": "x"}


def slugify(title):
    s = re.sub(r"[^a-z0-9]+", "-", title.lower()).strip("-")
    return s[:80]


def render_note(item, summary_md):
    def q(v):
        return '"' + str(v).replace('"', "'") + '"'
    return (
        "---\n"
        f"title: {q(item['title'])}\n"
        f"author: {q(item['author'])}\n"
        f"source: {q(item['source'])}\n"
        f"url: {q(item['url'])}\n"
        f"type: {item['type']}\n"
        f"date: {item['published']}\n"
        "tags: []\n"
        "---\n\n"
        f"# {item['title']}\n\n"
        f"## Summary\n\n{summary_md}\n\n"
        f"## Transcript\n\n{item['content']}\n"
    )


def write_note(item, summary_md, vault_dir):
    folder = Path(vault_dir) / FOLDERS[item["type"]]
    folder.mkdir(parents=True, exist_ok=True)
    stem = f"{item['published']}-{slugify(item['title'])}"
    path = folder / f"{stem}.md"
    path.write_text(render_note(item, summary_md))
    index = Path(vault_dir) / f"{item['published']}.md"
    line = f"- [[{FOLDERS[item['type']]}/{stem}|{item['title']}]]\n"
    existing = index.read_text() if index.exists() else f"# Harvest {item['published']}\n\n"
    if line not in existing:
        index.write_text(existing + line)
    return path
```

- [ ] **Step 4: Run to verify pass**

Run: `.venv/bin/pytest tests/test_notes.py -v` — Expected: 3 PASS

- [ ] **Step 5: Commit**

```bash
git add harvest/notes.py tests/test_notes.py
git commit -m "feat: note renderer with frontmatter and daily index"
```

---

### Task 4: Feed parsing + YouTube/article/podcast extractors

**Files:**
- Create: `harvest/feeds.py`, `harvest/extract.py`
- Test: `tests/test_feeds.py`, `tests/test_extract.py`

**Interfaces:**
- Produces:
  - `feeds.parse_feed(url_or_xml: str) -> list[dict]` — dicts with `id, title, author, url, published (YYYY-MM-DD), enclosure (str|None)`.
  - `feeds.youtube_feed_url(channel_id) -> str`.
  - `extract.youtube_captions(video_url, workdir) -> str` (yt-dlp auto-subs → cleaned text).
  - `extract.clean_vtt(vtt_text) -> str`.
  - `extract.article_markdown(url) -> str` (defuddle-cli via npx).
  - `extract.podcast_transcript(enclosure_url, workdir) -> str` (download → chunk if needed → Whisper).
  - `extract.needs_chunking(size_bytes) -> bool` (threshold 24MB).

- [ ] **Step 1: Write failing tests** (pure logic only — network wrappers are thin and exercised in Task 7's live smoke)

`tests/test_feeds.py`:
```python
from harvest.feeds import parse_feed, youtube_feed_url

RSS = """<?xml version="1.0"?>
<rss version="2.0"><channel><title>Show</title>
<item><title>Ep 1</title><link>https://ex.com/1</link><guid>g1</guid>
<pubDate>Mon, 06 Jul 2026 08:00:00 GMT</pubDate>
<enclosure url="https://ex.com/1.mp3" type="audio/mpeg" length="1000"/></item>
</channel></rss>"""


def test_parse_feed_maps_fields():
    items = parse_feed(RSS)
    assert items == [{
        "id": "g1", "title": "Ep 1", "author": "Show",
        "url": "https://ex.com/1", "published": "2026-07-06",
        "enclosure": "https://ex.com/1.mp3",
    }]


def test_youtube_feed_url():
    assert youtube_feed_url("UC123") == (
        "https://www.youtube.com/feeds/videos.xml?channel_id=UC123")
```

`tests/test_extract.py`:
```python
from harvest.extract import clean_vtt, needs_chunking

VTT = """WEBVTT

00:00:00.000 --> 00:00:02.000
hello world

00:00:02.000 --> 00:00:04.000
hello world
next line
"""


def test_clean_vtt_strips_cues_and_dedups():
    assert clean_vtt(VTT) == "hello world\nnext line"


def test_needs_chunking_threshold():
    assert not needs_chunking(24 * 1024 * 1024)
    assert needs_chunking(24 * 1024 * 1024 + 1)
```

- [ ] **Step 2: Run to verify failure**

Run: `.venv/bin/pytest tests/test_feeds.py tests/test_extract.py -v` — Expected: FAIL, modules not found

- [ ] **Step 3: Implement**

`harvest/feeds.py`:
```python
import time
from datetime import date

import feedparser


def youtube_feed_url(channel_id):
    return f"https://www.youtube.com/feeds/videos.xml?channel_id={channel_id}"


def parse_feed(url_or_xml):
    parsed = feedparser.parse(url_or_xml)
    feed_title = parsed.feed.get("title", "")
    items = []
    for e in parsed.entries:
        published = (
            time.strftime("%Y-%m-%d", e.published_parsed)
            if e.get("published_parsed") else date.today().isoformat()
        )
        items.append({
            "id": e.get("id") or e.get("link"),
            "title": e.get("title", "Untitled"),
            "author": e.get("author") or feed_title,
            "url": e.get("link", ""),
            "published": published,
            "enclosure": next((l["href"] for l in e.get("links", [])
                               if l.get("rel") == "enclosure"), None),
        })
    return items
```

`harvest/extract.py`:
```python
import subprocess
from pathlib import Path

import requests

WHISPER_CHUNK_BYTES = 24 * 1024 * 1024


def clean_vtt(vtt_text):
    out = []
    for ln in vtt_text.splitlines():
        ln = ln.strip()
        if not ln or ln == "WEBVTT" or "-->" in ln or ln.isdigit():
            continue
        if not out or out[-1] != ln:
            out.append(ln)
    return "\n".join(out)


def youtube_captions(video_url, workdir):
    subprocess.run(
        ["yt-dlp", "--skip-download", "--write-auto-subs", "--write-subs",
         "--sub-langs", "en.*", "--sub-format", "vtt",
         "-o", f"{workdir}/%(id)s", video_url],
        check=True, capture_output=True, text=True)
    vtts = sorted(Path(workdir).glob("*.vtt"))
    if not vtts:
        raise RuntimeError(f"no captions for {video_url}")
    return clean_vtt(vtts[0].read_text())


def article_markdown(url):
    r = subprocess.run(["npx", "--yes", "defuddle-cli", "parse", url, "--markdown"],
                       check=True, capture_output=True, text=True, timeout=120)
    return r.stdout.strip()


def needs_chunking(size_bytes):
    return size_bytes > WHISPER_CHUNK_BYTES


def podcast_transcript(enclosure_url, workdir):
    from openai import OpenAI  # deferred so tests don't need the key
    audio = Path(workdir) / "episode.mp3"
    with requests.get(enclosure_url, stream=True, timeout=300) as r:
        r.raise_for_status()
        with open(audio, "wb") as f:
            for chunk in r.iter_content(1 << 20):
                f.write(chunk)
    if needs_chunking(audio.stat().st_size):
        subprocess.run(
            ["ffmpeg", "-i", str(audio), "-f", "segment", "-segment_time",
             "1200", "-c", "copy", f"{workdir}/part%03d.mp3"],
            check=True, capture_output=True)
        parts = sorted(Path(workdir).glob("part*.mp3"))
    else:
        parts = [audio]
    client = OpenAI()
    texts = []
    for p in parts:
        with open(p, "rb") as f:
            texts.append(client.audio.transcriptions.create(
                model="whisper-1", file=f).text)
    return "\n".join(texts)
```

- [ ] **Step 4: Run to verify pass**

Run: `.venv/bin/pytest tests/test_feeds.py tests/test_extract.py -v` — Expected: 4 PASS.
Also verify defuddle CLI syntax once: `npx --yes defuddle-cli --help` — if the subcommand differs from `parse <url> --markdown`, fix `article_markdown` to match the actual CLI before committing.

- [ ] **Step 5: Commit**

```bash
git add harvest/feeds.py harvest/extract.py tests/test_feeds.py tests/test_extract.py
git commit -m "feat: feed parsing and content extractors"
```

---

### Task 5: X scraper (Playwright)

**Files:**
- Create: `harvest/x_scrape.py`
- Test: none automated (requires live login); verified in Task 7 smoke run.

**Interfaces:**
- Consumes: env `X_USERNAME`, `X_PASSWORD`.
- Produces: `scrape_accounts(handles: list[str], max_posts=20) -> list[dict]` — item dicts matching Task 3 shape with `type="x"`, `id` = status URL, `content` = post text.

- [ ] **Step 1: Implement**

`harvest/x_scrape.py`:
```python
import os
from datetime import date

from playwright.sync_api import sync_playwright


def _login(page):
    page.goto("https://x.com/i/flow/login")
    page.fill('input[autocomplete="username"]', os.environ["X_USERNAME"])
    page.keyboard.press("Enter")
    page.fill('input[name="password"]', os.environ["X_PASSWORD"])
    page.keyboard.press("Enter")
    page.wait_for_url("**/home", timeout=30000)


def _scrape_one(page, handle, max_posts):
    page.goto(f"https://x.com/{handle}")
    page.wait_for_selector("article", timeout=20000)
    items = []
    for a in page.query_selector_all("article")[:max_posts]:
        link = a.query_selector('a[href*="/status/"]')
        if not link:
            continue
        url = "https://x.com" + link.get_attribute("href")
        text = a.inner_text().strip()
        items.append({
            "id": url, "type": "x",
            "title": text.splitlines()[0][:70] if text else url,
            "author": handle, "source": handle, "url": url,
            "published": date.today().isoformat(), "content": text,
        })
    return items


def scrape_accounts(handles, max_posts=20):
    out = []
    with sync_playwright() as pw:
        browser = pw.chromium.launch(headless=True)
        page = browser.new_page()
        _login(page)
        for h in handles:
            out.extend(_scrape_one(page, h, max_posts))
        browser.close()
    return out
```

- [ ] **Step 2: Install browser + syntax check**

Run: `.venv/bin/playwright install chromium && .venv/bin/python -c "import harvest.x_scrape"`
Expected: no error. (Live login exercised when X sources exist; X challenges/lockouts are expected transients per spec — surfaced as per-source errors, retried next run.)

- [ ] **Step 3: Commit**

```bash
git add harvest/x_scrape.py
git commit -m "feat: X timeline scraper via Playwright"
```

---

### Task 6: Orchestrator → staging

**Files:**
- Create: `harvest/run.py`
- Test: `tests/test_run.py`

**Interfaces:**
- Consumes: `state.new_items`, `feeds.*`, `extract.*`, `x_scrape.scrape_accounts`, `sources.yaml`.
- Produces: CLI `python -m harvest.run` — writes `staging/<type>-<sha1(id)[:12]>.json` per new item (full item dict of Task 3 shape). Core function `harvest_all(config: dict, state: dict, staging_dir, fetchers: dict) -> list[str]` returns error strings; `fetchers` maps type_key (`youtube|article|podcast|x`) → callable so tests inject fakes. Fetcher signature: `fetcher(source_key) -> list[item]` (items WITH content already extracted).
- Note: adding a source is expected to go through `harvest.seed` (Task 7) BEFORE the next run, so expensive extraction is never wasted on a first sighting. If a source appears unseeded, `harvest_all` still seeds it safely (stages nothing) — the only cost is that run's extraction work.

- [ ] **Step 1: Write failing tests**

`tests/test_run.py`:
```python
import json
from harvest.run import harvest_all

ITEM = {"id": "i1", "type": "article", "title": "T", "author": "A",
        "source": "feedA", "url": "u", "published": "2026-07-06", "content": "c"}


def _ok_fetcher(source_key):
    return [ITEM]


def _boom(source_key):
    raise RuntimeError("feed down")


def test_one_failing_source_does_not_block_others(tmp_path):
    config = {"articles": ["feedA"], "podcasts": ["feedB"]}
    state = {"sources": {"feedA": {"seen": []}, "feedB": {"seen": []}}}
    errors = harvest_all(config, state, tmp_path,
                         {"article": _ok_fetcher, "podcast": _boom})
    staged = list(tmp_path.glob("*.json"))
    assert len(staged) == 1
    assert json.loads(staged[0].read_text()) == ITEM
    assert len(errors) == 1 and "feedB" in errors[0]
    # failed source's items NOT marked seen
    assert state["sources"]["feedB"]["seen"] == []


def test_first_sighting_stages_nothing(tmp_path):
    config = {"articles": ["newFeed"]}
    state = {"sources": {}}
    harvest_all(config, state, tmp_path, {"article": _ok_fetcher})
    assert list(tmp_path.glob("*.json")) == []
    assert state["sources"]["newFeed"]["seen"] == ["i1"]
```

- [ ] **Step 2: Run to verify failure**

Run: `.venv/bin/pytest tests/test_run.py -v` — Expected: FAIL, module not found

- [ ] **Step 3: Implement**

`harvest/run.py`:
```python
import hashlib
import json
import sys
import tempfile
from pathlib import Path

import yaml

from harvest import extract, feeds, state as state_mod

ROOT = Path(__file__).resolve().parents[1]
TYPE_KEYS = {"youtube": "youtube", "articles": "article",
             "podcasts": "podcast", "x": "x"}


def harvest_all(config, state, staging_dir, fetchers):
    staging_dir = Path(staging_dir)
    staging_dir.mkdir(parents=True, exist_ok=True)
    errors = []
    for cfg_key, type_key in TYPE_KEYS.items():
        fetcher = fetchers.get(type_key)
        if fetcher is None:
            continue
        for source_key in config.get(cfg_key, []):
            try:
                items = fetcher(source_key)
                fresh = set(state_mod.new_items(
                    state, source_key, [i["id"] for i in items]))
                for item in items:
                    if item["id"] not in fresh:
                        continue
                    h = hashlib.sha1(item["id"].encode()).hexdigest()[:12]
                    (staging_dir / f"{type_key}-{h}.json").write_text(
                        json.dumps(item, indent=2))
            except Exception as e:  # isolate per-source failures
                errors.append(f"{source_key}: {e}")
    return errors


def _youtube_fetcher(channel_id):
    out = []
    for i in feeds.parse_feed(feeds.youtube_feed_url(channel_id)):
        with tempfile.TemporaryDirectory() as wd:
            content = extract.youtube_captions(i["url"], wd)
        out.append({**i, "type": "youtube", "source": channel_id,
                    "content": content})
    return out


def _article_fetcher(feed_url):
    return [{**i, "type": "article", "source": feed_url,
             "content": extract.article_markdown(i["url"])}
            for i in feeds.parse_feed(feed_url)]


def _podcast_fetcher(feed_url):
    out = []
    for i in feeds.parse_feed(feed_url):
        with tempfile.TemporaryDirectory() as wd:
            content = extract.podcast_transcript(i["enclosure"], wd)
        out.append({**i, "type": "podcast", "source": feed_url,
                    "content": content})
    return out


def _x_fetcher(handle):
    from harvest.x_scrape import scrape_accounts
    return scrape_accounts([handle])


def main():
    config = yaml.safe_load((ROOT / "sources.yaml").read_text()) or {}
    state = state_mod.load_state(ROOT / "sources-state.json")
    errors = harvest_all(config, state, ROOT / "staging", {
        "youtube": _youtube_fetcher, "article": _article_fetcher,
        "podcast": _podcast_fetcher, "x": _x_fetcher,
    })
    state_mod.save_state(state, ROOT / "sources-state.json")
    for e in errors:
        print(f"ERROR {e}", file=sys.stderr)
    staged = len(list((ROOT / "staging").glob("*.json")))
    print(f"staged={staged} errors={len(errors)}")


if __name__ == "__main__":
    main()
```

- [ ] **Step 4: Run to verify pass**

Run: `.venv/bin/pytest tests/test_run.py -v` — Expected: 2 PASS

- [ ] **Step 5: Commit**

```bash
git add harvest/run.py tests/test_run.py
git commit -m "feat: orchestrator with per-source error isolation"
```

---

### Task 7: Seed helper + finalize CLI

**Files:**
- Create: `harvest/seed.py`, `harvest/finalize.py`
- Test: `tests/test_finalize.py`

**Interfaces:**
- Consumes: `state.*`, `notes.write_note`, staged JSON files from Task 6.
- Produces:
  - CLI `python -m harvest.seed <type> <source_key>` — fetches current feed IDs WITHOUT content extraction and seeds them seen (cheap; run when adding a source).
  - CLI `python -m harvest.finalize <staged.json> <summary.md>` — writes note via `write_note(item, summary, ROOT/"brain")`, marks seen, deletes staged file. Core: `finalize(staged_path, summary_md, vault_dir, state_path) -> Path`.

- [ ] **Step 1: Write failing test**

`tests/test_finalize.py`:
```python
import json
from harvest.finalize import finalize
from harvest.state import load_state, save_state

ITEM = {"id": "i1", "type": "article", "title": "T", "author": "A",
        "source": "feedA", "url": "u", "published": "2026-07-06", "content": "c"}


def test_finalize_writes_note_marks_seen_removes_staging(tmp_path):
    staged = tmp_path / "article-abc.json"
    staged.write_text(json.dumps(ITEM))
    state_path = tmp_path / "state.json"
    save_state({"sources": {"feedA": {"seen": []}}}, state_path)
    vault = tmp_path / "brain"

    note = finalize(staged, "Summary.", vault, state_path)

    assert note.exists() and "Summary." in note.read_text()
    assert load_state(state_path)["sources"]["feedA"]["seen"] == ["i1"]
    assert not staged.exists()
```

- [ ] **Step 2: Run to verify failure**

Run: `.venv/bin/pytest tests/test_finalize.py -v` — Expected: FAIL, module not found

- [ ] **Step 3: Implement**

`harvest/finalize.py`:
```python
import json
import sys
from pathlib import Path

from harvest.notes import write_note
from harvest.state import load_state, mark_seen, save_state

ROOT = Path(__file__).resolve().parents[1]


def finalize(staged_path, summary_md, vault_dir, state_path):
    staged_path = Path(staged_path)
    item = json.loads(staged_path.read_text())
    note = write_note(item, summary_md, vault_dir)
    state = load_state(state_path)
    mark_seen(state, item["source"], item["id"])
    save_state(state, state_path)
    staged_path.unlink()
    return note


def main():
    staged, summary_file = sys.argv[1], sys.argv[2]
    note = finalize(staged, Path(summary_file).read_text().strip(),
                    ROOT / "brain", ROOT / "sources-state.json")
    print(note)


if __name__ == "__main__":
    main()
```

`harvest/seed.py`:
```python
import sys
from pathlib import Path

from harvest import feeds
from harvest.state import load_state, new_items, save_state

ROOT = Path(__file__).resolve().parents[1]


def main():
    type_key, source_key = sys.argv[1], sys.argv[2]
    if type_key == "youtube":
        ids = [i["id"] for i in feeds.parse_feed(feeds.youtube_feed_url(source_key))]
    elif type_key in ("article", "podcast"):
        ids = [i["id"] for i in feeds.parse_feed(source_key)]
    else:  # x — no cheap feed; scraper only sees recent posts anyway
        ids = []
    state_path = ROOT / "sources-state.json"
    state = load_state(state_path)
    new_items(state, source_key, ids)  # first sighting seeds all as seen
    save_state(state, state_path)
    print(f"seeded {source_key} with {len(ids)} ids")


if __name__ == "__main__":
    main()
```

- [ ] **Step 4: Run full suite**

Run: `.venv/bin/pytest -v` — Expected: all PASS (state 4, notes 3, feeds 2, extract 2, run 2, finalize 1 = 14)

- [ ] **Step 5: Live smoke test (one real source)**

Add one real YouTube channel ID to `sources.yaml`, then:
```bash
.venv/bin/python -m harvest.seed youtube <CHANNEL_ID>   # seed history
.venv/bin/python -m harvest.run                         # should stage 0 (all seen)
```
Expected: `staged=0 errors=0`; `sources-state.json` contains the channel's video IDs. Proves feed fetch + seeding end-to-end without burning extraction.

- [ ] **Step 6: Commit**

```bash
git add harvest/seed.py harvest/finalize.py tests/test_finalize.py sources.yaml sources-state.json
git commit -m "feat: seed and finalize CLIs"
```

---

### Task 8: Agent runbook + README + schedule

**Files:**
- Create: `RUNBOOK.md`, `README.md`

**Interfaces:**
- Consumes: every CLI above.
- Produces: the prompt/checklist the scheduled cloud agent follows daily.

- [ ] **Step 1: Write RUNBOOK.md**

```markdown
# Daily Harvest Runbook (scheduled agent)

Secrets required in the agent environment: `OPENAI_API_KEY`, `X_USERNAME`,
`X_PASSWORD`, plus GitHub push access to this repo. Never echo or commit them.

1. `git pull --rebase origin main` (pick up local edits; abort run on
   conflict and report).
2. Install deps if needed: `pip install -r requirements.txt`,
   `playwright install chromium`; ensure `yt-dlp`, `ffmpeg`, `node` on PATH.
3. Run `python -m harvest.run`. Note the `staged=N errors=M` line. Errors are
   expected transients (X challenges, yt-dlp bot blocks, dead feeds) — report
   them in the run summary, do not retry within the run.
4. For EACH file in `staging/`:
   a. Read the JSON; read its `content`.
   b. Write a summary to a temp file: 2-4 sentence overview, then a
      `### Key Points` list of 3-7 bullets.
   c. `python -m harvest.finalize staging/<file>.json <summary-file>`
5. `git add brain/ sources-state.json && git commit -m "harvest: $(date +%F)"`
   (skip commit if nothing changed).
6. `git push origin main`.
7. Report: items harvested per type, errors, note links.

Adding a source later: append to `sources.yaml`, then run
`python -m harvest.seed <type> <source_key>` so history isn't backfilled.
```

- [ ] **Step 2: Write README.md**

```markdown
# ticket-content-scrape

Daily content harvest (YouTube / articles / podcasts / X) into an Obsidian
vault at `brain/`.

- Design spec: `brain/docs/specs/2026-07-06-content-harvest-pipeline-design.md`
- Implementation plan: `brain/docs/plans/2026-07-06-content-harvest-pipeline.md`
- Daily automation: `RUNBOOK.md` (cloud-scheduled Claude agent)

Usage:
- `sources.yaml` — subscriptions. After adding a source, seed it:
  `python -m harvest.seed <type> <source_key>`
- `sources-state.json` — dedup memory (committed).
- `python -m harvest.run` — stage new items to `staging/`.
- `python -m harvest.finalize <staged.json> <summary.md>` — write final note.
- Tests: `pytest`
```

- [ ] **Step 3: Commit**

```bash
git add RUNBOOK.md README.md
git commit -m "docs: agent runbook and README"
```

- [ ] **Step 4: Create the schedule (user action)**

Cannot be scripted: user runs `/schedule` in Claude Code to create a daily routine with prompt "Follow RUNBOOK.md in jj80etix/ticket-content-scrape and execute the daily harvest." Configure repo access plus the three secrets (`OPENAI_API_KEY`, `X_USERNAME`, `X_PASSWORD`) in the routine's environment. Verify the first scheduled run's report.

---

## Self-Review (done)

- **Spec coverage:** subscription config (T1), first-run seeding (T2 + T7 seed CLI), per-item notes w/ exact frontmatter + daily index (T3), all four source types (T4/T5/T6), Whisper 24MB chunking (T4), error isolation + not-seen-until-success (T6/T7), pull-before-run + push cycle + secrets handling (T8 runbook). Spec's out-of-scope items remain out.
- **Placeholder scan:** clean — every code step has full code; defuddle CLI syntax flagged for one-time verification in T4 step 4 with the exact command.
- **Type consistency:** item dict shape (`id,type,title,author,source,url,published,content`) identical across notes/run/finalize/x_scrape; folder map defined once in notes.py; state shape consistent between state.py and all tests.
