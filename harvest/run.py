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
