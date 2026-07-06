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
