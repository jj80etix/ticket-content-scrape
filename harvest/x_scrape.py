import os
from datetime import date

from playwright.sync_api import sync_playwright

_session = None


def _login(page):
    page.goto("https://x.com/i/flow/login")
    page.fill('input[autocomplete="username"]', os.environ["X_USERNAME"])
    page.keyboard.press("Enter")
    page.fill('input[name="password"]', os.environ["X_PASSWORD"])
    page.keyboard.press("Enter")
    page.wait_for_url("**/home", timeout=30000)


class _Session:
    """One logged-in browser shared across every handle in a run; repeated
    logins per handle trip X's bot detection."""

    def __init__(self):
        self._pw = sync_playwright().start()
        try:
            self._browser = self._pw.chromium.launch(headless=True)
            self.page = self._browser.new_page()
            _login(self.page)
        except Exception:
            self.close()
            raise

    def close(self):
        try:
            if getattr(self, "_browser", None):
                self._browser.close()
        finally:
            self._pw.stop()


def _get_session():
    global _session
    if _session is None:
        _session = _Session()
    return _session


def close_session():
    global _session
    if _session is not None:
        try:
            _session.close()
        finally:
            _session = None


def _scrape_one(page, handle, max_posts):
    page.goto(f"https://x.com/{handle}")
    page.wait_for_selector("article", timeout=20000)
    items = []
    for a in page.query_selector_all("article")[:max_posts]:
        link = a.query_selector('a[href*="/status/"]')
        if not link:
            continue
        url = "https://x.com" + link.get_attribute("href")
        text = a.inner_text().strip()
        items.append({
            "id": url, "type": "x",
            "title": text.splitlines()[0][:70] if text else url,
            "author": handle, "source": handle, "url": url,
            "published": date.today().isoformat(), "content": text,
        })
    return items


def scrape_accounts(handles, max_posts=20):
    page = _get_session().page
    out = []
    for h in handles:
        out.extend(_scrape_one(page, h, max_posts))
    return out
