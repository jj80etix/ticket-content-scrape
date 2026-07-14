# brain/ticket-content-scrape/ — generated Obsidian vault

Everything under this directory is pipeline output written by `harvest/finalize.py` and the daily cloud agent (see `../RUNBOOK.md`). Treat it as data, not source.

- Do not hand-edit, reorganize, dedupe, or "clean up" notes here — fix the pipeline (`harvest/notes.py`, `RUNBOOK.md`, `docs/research-questions.md`) instead, or the next run reintroduces the problem.
- Layout: `YYYY-MM-DD.md` daily summary reports; `articles/`, `youtube/`, `podcasts/`, `x/` per-item notes; `digests/` weekly/monthly rollups; `docs/` design specs and plans (the one hand-written area).
- Note format contract: YAML frontmatter with mirrored `tags:`, body ends with the tag line as the last line. Editing a note's tail can break tag mirroring assumptions.
- Deleting a note does NOT cause re-harvest (dedup lives in `../sources-state.json`), but the daily note's links to it break.

## Obsidian CLI

- Pipeline and cloud agent write notes as plain files via `harvest/notes.py` — never through Obsidian CLI (cloud agent has no Obsidian app).
- Obsidian CLI is for local inspection/verification only: searching notes, querying tags/properties, checking that frontmatter tag mirroring rendered correctly.
- Never create harvest notes via Obsidian CLI — that bypasses `harvest/finalize.py`, so `sources-state.json` never marks the item seen and the next run re-stages it as a duplicate.
