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
