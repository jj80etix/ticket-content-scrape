import sys
from pathlib import Path

from harvest import feeds
from harvest.state import load_state, new_items, save_state

ROOT = Path(__file__).resolve().parents[1]


def main():
    type_key, source_key = sys.argv[1], sys.argv[2]
    allow_empty = "--allow-empty" in sys.argv[3:]
    if type_key == "x":
        # x has no cheap feed to pre-seed from, but that's fine: not seeding
        # an x handle gives correct first-sighting behavior on its own.
        print("x needs no seeding — first run seeds itself")
        return
    if type_key == "youtube":
        ids = [i["id"] for i in feeds.parse_feed(feeds.youtube_feed_url(source_key))]
    else:  # article, podcast
        ids = [i["id"] for i in feeds.parse_feed(source_key)]
    if not ids and not allow_empty:
        print(f"ERROR: refusing to seed {source_key!r} with 0 ids "
              "(feed unreachable or genuinely empty?) — pass --allow-empty "
              "to seed anyway", file=sys.stderr)
        sys.exit(1)
    state_path = ROOT / "sources-state.json"
    state = load_state(state_path)
    new_items(state, source_key, ids)  # first sighting seeds all as seen
    save_state(state, state_path)
    print(f"seeded {source_key} with {len(ids)} ids")


if __name__ == "__main__":
    main()
