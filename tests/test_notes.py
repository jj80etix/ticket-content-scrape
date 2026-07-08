import hashlib

from harvest.notes import extract_tags, slugify, render_note, write_note

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


def test_extract_tags():
    assert extract_tags("Summary.\n\n- point\n\n#q12 #build #ticketmaster") == [
        "q12", "build", "ticketmaster"]
    assert extract_tags("Summary with no tag line.\n\n- point") == []
    # hashtags mid-text don't count — only a trailing tags-only line
    assert extract_tags("Talks about #q12 in prose.\n\n- point") == []
    assert extract_tags("") == []


def test_render_note_mirrors_tags_into_frontmatter():
    md = render_note(ITEM, "Summary.\n\n- point\n\n#q8 #evolve #build")
    assert "tags: [q8, evolve, build]" in md
    assert "#q8 #evolve #build" in md  # inline tag line preserved


def test_write_note_path_and_daily_index(tmp_path):
    p = write_note(ITEM, "Summary.", tmp_path)
    assert p == tmp_path / "articles" / "2026-07-06-big-news-ai-tickets.md"
    assert p.exists()
    index = (tmp_path / "2026-07-06.md").read_text()
    assert "[[articles/2026-07-06-big-news-ai-tickets|Big News: AI & Tickets!]]" in index
    # second write must not duplicate the index line
    write_note(ITEM, "Summary.", tmp_path)
    assert (tmp_path / "2026-07-06.md").read_text().count("big-news-ai-tickets") == 1


def test_write_note_empty_slug_falls_back_to_id_hash(tmp_path):
    """A fully non-ASCII title slugifies to '' — without a fallback, every
    such note on a given day collapses onto the same YYYY-MM-DD-.md file,
    silently overwriting prior notes."""
    item1 = {**ITEM, "id": "note-one", "title": "日本語のタイトル"}
    item2 = {**ITEM, "id": "note-two", "title": "日本語のタイトル"}

    p1 = write_note(item1, "Summary.", tmp_path)
    p2 = write_note(item2, "Summary.", tmp_path)

    assert p1.name != "2026-07-06-.md"
    assert p2.name != "2026-07-06-.md"
    assert p1 != p2

    h1 = hashlib.sha1(item1["id"].encode()).hexdigest()[:12]
    h2 = hashlib.sha1(item2["id"].encode()).hexdigest()[:12]
    assert p1.name == f"2026-07-06-{h1}.md"
    assert p2.name == f"2026-07-06-{h2}.md"
