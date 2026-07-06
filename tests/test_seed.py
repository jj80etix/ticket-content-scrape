import pytest
import sys

from harvest.seed import main


def test_dead_feed_raises_runtime_error_exits_1(monkeypatch, tmp_path):
    """Dead feed raises RuntimeError before seeding; exit(1), no state created."""
    def mock_parse_feed(url):
        raise RuntimeError("feed error: boom")

    monkeypatch.setattr("harvest.seed.feeds.parse_feed", mock_parse_feed)
    monkeypatch.setattr("sys.argv", ["seed", "article", "http://dead.example/feed"])
    monkeypatch.setattr("harvest.seed.ROOT", tmp_path)

    with pytest.raises(SystemExit) as exc_info:
        main()

    assert exc_info.value.code == 1
    # Verify state file was not created
    assert not (tmp_path / "sources-state.json").exists()


def test_empty_feed_with_allow_empty_seeds_without_error(monkeypatch, tmp_path):
    """Empty feed with --allow-empty succeeds, creates state with empty ids."""
    def mock_parse_feed(url):
        return []

    monkeypatch.setattr("harvest.seed.feeds.parse_feed", mock_parse_feed)
    monkeypatch.setattr("sys.argv", ["seed", "article", "http://empty.example/feed", "--allow-empty"])
    monkeypatch.setattr("harvest.seed.ROOT", tmp_path)

    # Should return normally without raising
    main()

    # Verify state file was created with empty ids
    from harvest.state import load_state
    state = load_state(tmp_path / "sources-state.json")
    assert "http://empty.example/feed" in state["sources"]
    assert state["sources"]["http://empty.example/feed"]["seen"] == []
