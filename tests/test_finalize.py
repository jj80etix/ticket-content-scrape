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
