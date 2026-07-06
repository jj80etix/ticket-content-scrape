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
