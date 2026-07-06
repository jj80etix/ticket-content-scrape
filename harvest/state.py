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
