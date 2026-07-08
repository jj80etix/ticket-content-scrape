import hashlib
import re
from pathlib import Path

FOLDERS = {"youtube": "youtube", "article": "articles",
           "podcast": "podcasts", "x": "x"}


def slugify(title):
    s = re.sub(r"[^a-z0-9]+", "-", title.lower()).strip("-")
    return s[:80]


TAG_LINE = re.compile(r"^(#[a-z0-9][a-z0-9-]*)(\s+#[a-z0-9][a-z0-9-]*)*$")


def extract_tags(summary_md):
    for line in reversed(summary_md.strip().splitlines()):
        line = line.strip()
        if not line:
            continue
        if TAG_LINE.match(line):
            return [t.lstrip("#") for t in line.split()]
        return []
    return []


def render_note(item, summary_md):
    def q(v):
        return '"' + str(v).replace('"', "'") + '"'
    tags_yaml = "[" + ", ".join(extract_tags(summary_md)) + "]"
    return (
        "---\n"
        f"title: {q(item['title'])}\n"
        f"author: {q(item['author'])}\n"
        f"source: {q(item['source'])}\n"
        f"url: {q(item['url'])}\n"
        f"type: {item['type']}\n"
        f"date: {item['published']}\n"
        f"tags: {tags_yaml}\n"
        "---\n\n"
        f"# {item['title']}\n\n"
        f"## Summary\n\n{summary_md}\n\n"
        f"## Transcript\n\n{item['content']}\n"
    )


def write_note(item, summary_md, vault_dir):
    folder = Path(vault_dir) / FOLDERS[item["type"]]
    folder.mkdir(parents=True, exist_ok=True)
    slug = slugify(item["title"]) or hashlib.sha1(item["id"].encode()).hexdigest()[:12]
    stem = f"{item['published']}-{slug}"
    path = folder / f"{stem}.md"
    path.write_text(render_note(item, summary_md))
    index = Path(vault_dir) / f"{item['published']}.md"
    line = f"- [[{FOLDERS[item['type']]}/{stem}|{item['title']}]]\n"
    existing = index.read_text() if index.exists() else f"# Harvest {item['published']}\n\n"
    if line not in existing:
        index.write_text(existing + line)
    return path
