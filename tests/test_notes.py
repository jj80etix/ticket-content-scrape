from harvest.notes import slugify, render_note, write_note

ITEM = {
    "id": "abc123", "type": "article", "title": "Big News: AI & Tickets!",
    "author": "Jane Doe", "source": "https://example.com/feed",
    "url": "https://example.com/post", "published": "2026-07-06",
    "content": "Full article text here.",
}


def test_slugify():
    assert slugify("Big News: AI & Tickets!") == "big-news-ai-tickets"


def test_render_note_frontmatter_and_sections():
    md = render_note(ITEM, "One-line summary.\n\n- point")
    assert md.startswith("---\n")
    for line in ['title: "Big News: AI & Tickets!"', 'author: "Jane Doe"',
                 "type: article", "date: 2026-07-06", "tags: []"]:
        assert line in md
    assert "## Summary" in md and "## Transcript" in md
    assert "Full article text here." in md


def test_write_note_path_and_daily_index(tmp_path):
    p = write_note(ITEM, "Summary.", tmp_path)
    assert p == tmp_path / "articles" / "2026-07-06-big-news-ai-tickets.md"
    assert p.exists()
    index = (tmp_path / "2026-07-06.md").read_text()
    assert "[[articles/2026-07-06-big-news-ai-tickets|Big News: AI & Tickets!]]" in index
    # second write must not duplicate the index line
    write_note(ITEM, "Summary.", tmp_path)
    assert (tmp_path / "2026-07-06.md").read_text().count("big-news-ai-tickets") == 1
