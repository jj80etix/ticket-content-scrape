import pytest

from harvest.feeds import parse_feed, youtube_feed_url

RSS = """<?xml version="1.0"?>
<rss version="2.0"><channel><title>Show</title>
<item><title>Ep 1</title><link>https://ex.com/1</link><guid>g1</guid>
<pubDate>Mon, 06 Jul 2026 08:00:00 GMT</pubDate>
<enclosure url="https://ex.com/1.mp3" type="audio/mpeg" length="1000"/></item>
</channel></rss>"""

DEAD_FEED_HTML = ("<html><head><title>404 Not Found</title></head>"
                   "<body><p>The requested feed was not found.</body></html>")


def test_parse_feed_maps_fields():
    items = parse_feed(RSS)
    assert items == [{
        "id": "g1", "title": "Ep 1", "author": "Show",
        "url": "https://ex.com/1", "published": "2026-07-06",
        "enclosure": "https://ex.com/1.mp3",
    }]


def test_youtube_feed_url():
    assert youtube_feed_url("UC123") == (
        "https://www.youtube.com/feeds/videos.xml?channel_id=UC123")


def test_parse_feed_raises_on_dead_feed():
    """A 404/HTML response parses with bozo set and zero entries — this
    must raise instead of silently reading as an empty-but-healthy feed."""
    with pytest.raises(RuntimeError):
        parse_feed(DEAD_FEED_HTML)
