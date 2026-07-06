import json

from harvest.run import harvest_all

META = {"id": "i1", "title": "T", "author": "A", "url": "u",
        "published": "2026-07-06"}
ITEM = {**META, "type": "article", "source": "feedA", "content": "c"}


def _ok_lister(source_key):
    return [META]


def _ok_extractor(source_key, meta):
    return {**meta, "type": "article", "source": source_key, "content": "c"}


def _boom_lister(source_key):
    raise RuntimeError("feed down")


def test_one_failing_source_does_not_block_others(tmp_path):
    config = {"articles": ["feedA"], "podcasts": ["feedB"]}
    state = {"sources": {"feedA": {"seen": []}, "feedB": {"seen": []}}}
    errors = harvest_all(config, state, tmp_path,
                         {"article": (_ok_lister, _ok_extractor),
                          "podcast": (_boom_lister, _ok_extractor)})
    staged = list(tmp_path.glob("*.json"))
    assert len(staged) == 1
    assert json.loads(staged[0].read_text()) == ITEM
    assert len(errors) == 1 and "feedB" in errors[0]
    # failed source's items NOT marked seen
    assert state["sources"]["feedB"]["seen"] == []


def test_first_sighting_stages_nothing(tmp_path):
    config = {"articles": ["newFeed"]}
    state = {"sources": {}}
    harvest_all(config, state, tmp_path, {"article": (_ok_lister, _ok_extractor)})
    assert list(tmp_path.glob("*.json")) == []
    assert state["sources"]["newFeed"]["seen"] == ["i1"]


def test_extraction_skips_already_seen_ids(tmp_path):
    """Known source, lister returns a mix of seen/unseen ids: extractor must
    run only for unseen ids, and only the unseen item gets staged."""
    config = {"articles": ["feedA"]}
    state = {"sources": {"feedA": {"seen": ["i1"]}}}
    calls = []

    def lister(source_key):
        return [{"id": "i1", "title": "Old"}, {"id": "i2", "title": "New"}]

    def extractor(source_key, meta):
        calls.append(meta["id"])
        return {**meta, "type": "article", "source": source_key, "content": "c2"}

    errors = harvest_all(config, state, tmp_path, {"article": (lister, extractor)})
    staged = list(tmp_path.glob("*.json"))

    assert errors == []
    assert calls == ["i2"]
    assert len(staged) == 1
    assert json.loads(staged[0].read_text())["id"] == "i2"
