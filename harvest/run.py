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
        lister, extractor = fetcher
        for source_key in config.get(cfg_key, []):
            try:
                metas = lister(source_key)
                fresh = set(state_mod.new_items(
                    state, source_key, [m["id"] for m in metas]))
                for meta in metas:
                    if meta["id"] not in fresh:
                        continue
                    item = extractor(source_key, meta)
                    h = hashlib.sha1(item["id"].encode()).hexdigest()[:12]
                    (staging_dir / f"{type_key}-{h}.json").write_text(
                        json.dumps(item, indent=2))
            except Exception as e:  # isolate per-source failures
                errors.append(f"{source_key}: {e}")
    return errors


def _youtube_lister(channel_id):
    return feeds.parse_feed(feeds.youtube_feed_url(channel_id))


def _youtube_extractor(channel_id, meta):
    with tempfile.TemporaryDirectory() as wd:
        content = extract.youtube_captions(meta["url"], wd)
    return {**meta, "type": "youtube", "source": channel_id,
            "content": content}


def _article_lister(feed_url):
    return feeds.parse_feed(feed_url)


def _article_extractor(feed_url, meta):
    return {**meta, "type": "article", "source": feed_url,
            "content": extract.article_markdown(meta["url"])}


def _podcast_lister(feed_url):
    return feeds.parse_feed(feed_url)


def _podcast_extractor(feed_url, meta):
    with tempfile.TemporaryDirectory() as wd:
        content = extract.podcast_transcript(meta["enclosure"], wd)
    return {**meta, "type": "podcast", "source": feed_url,
            "content": content}


def _x_lister(handle):
    from harvest.x_scrape import scrape_accounts
    return scrape_accounts([handle])


def _x_extractor(handle, meta):
    return meta


def main():
    config = yaml.safe_load((ROOT / "sources.yaml").read_text()) or {}
    state = state_mod.load_state(ROOT / "sources-state.json")
    errors = harvest_all(config, state, ROOT / "staging", {
        "youtube": (_youtube_lister, _youtube_extractor),
        "article": (_article_lister, _article_extractor),
        "podcast": (_podcast_lister, _podcast_extractor),
        "x": (_x_lister, _x_extractor),
    })
    state_mod.save_state(state, ROOT / "sources-state.json")
    for e in errors:
        print(f"ERROR {e}", file=sys.stderr)
    staged = len(list((ROOT / "staging").glob("*.json")))
    print(f"staged={staged} errors={len(errors)}")


if __name__ == "__main__":
    main()
