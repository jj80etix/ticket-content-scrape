import os
from datetime import date

from playwright.sync_api import sync_playwright


def _login(page):
    page.goto("https://x.com/i/flow/login")
    page.fill('input[autocomplete="username"]', os.environ["X_USERNAME"])
    page.keyboard.press("Enter")
    page.fill('input[name="password"]', os.environ["X_PASSWORD"])
    page.keyboard.press("Enter")
    page.wait_for_url("**/home", timeout=30000)


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
    out = []
    with sync_playwright() as pw:
        browser = pw.chromium.launch(headless=True)
        page = browser.new_page()
        _login(page)
        for h in handles:
            out.extend(_scrape_one(page, h, max_posts))
        browser.close()
    return out
