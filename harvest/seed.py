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
