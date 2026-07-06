import time
from datetime import date

import feedparser


def youtube_feed_url(channel_id):
    return f"https://www.youtube.com/feeds/videos.xml?channel_id={channel_id}"


def parse_feed(url_or_xml):
    parsed = feedparser.parse(url_or_xml)
    feed_title = parsed.feed.get("title", "")
    items = []
    for e in parsed.entries:
        published = (
            time.strftime("%Y-%m-%d", e.published_parsed)
            if e.get("published_parsed") else date.today().isoformat()
        )
        items.append({
            "id": e.get("id") or e.get("link"),
            "title": e.get("title", "Untitled"),
            "author": e.get("author") or feed_title,
            "url": e.get("link", ""),
            "published": published,
            "enclosure": next((l["href"] for l in e.get("links", [])
                               if l.get("rel") == "enclosure"), None),
        })
    return items
