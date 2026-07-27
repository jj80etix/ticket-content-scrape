from unittest.mock import MagicMock, patch

import harvest.x_scrape as xs


def _fake_playwright():
    sp = MagicMock()  # stands in for sync_playwright
    runtime = sp.return_value.start.return_value
    page = runtime.chromium.launch.return_value.new_page.return_value
    page.query_selector_all.return_value = []
    return sp, runtime, page


def test_session_reused_across_calls(monkeypatch):
    monkeypatch.setenv("X_USERNAME", "u")
    monkeypatch.setenv("X_PASSWORD", "p")
    sp, runtime, page = _fake_playwright()
    with patch.object(xs, "sync_playwright", sp):
        xs.close_session()
        xs.scrape_accounts(["a"])
        xs.scrape_accounts(["b"])
        assert sp.call_count == 1  # one browser/login for whole run
        xs.close_session()
        runtime.stop.assert_called_once()
    assert xs._session is None


def test_login_failure_cleans_up(monkeypatch):
    monkeypatch.setenv("X_USERNAME", "u")
    monkeypatch.setenv("X_PASSWORD", "p")
    sp, runtime, page = _fake_playwright()
    page.wait_for_url.side_effect = RuntimeError("login failed")
    with patch.object(xs, "sync_playwright", sp):
        xs.close_session()
        try:
            xs.scrape_accounts(["a"])
        except RuntimeError:
            pass
        else:
            raise AssertionError("expected login failure to raise")
        assert xs._session is None
        runtime.stop.assert_called_once()
