# ticket-content-scrape

Daily content harvest (articles / YouTube / podcasts / X) into an Obsidian vault at `brain/`. A cloud-scheduled Claude agent runs the pipeline daily at 10:00 UTC following `RUNBOOK.md`; a local launchd job pulls the resulting commits at 7 AM ET.

## Commands

```bash
pytest                                          # run all tests
python -m harvest.run                           # stage new items to staging/
python -m harvest.finalize <staged.json> <summary.md>   # write final note + mark seen
python -m harvest.seed <type> <source_key>      # seed a NEW source (see gotcha below)
```

## Architecture

- `harvest/run.py` — orchestrator: lists new items per source, extracts content, writes JSON to `staging/`. Per-item isolation: one failing item logs an error, doesn't kill the run.
- `harvest/extract.py` — content extraction (yt-dlp captions, `npx defuddle-cli` for articles, podcast transcripts).
- `harvest/feeds.py` — RSS/Atom parsing.
- `harvest/state.py` — dedup memory backed by `sources-state.json` (committed to git on purpose).
- `harvest/notes.py` — renders Obsidian notes; mirrors the summary's final tag line into YAML frontmatter `tags:`.
- `harvest/finalize.py` — staged JSON + summary → note in vault, then marks item seen.
- `sources.yaml` — subscription list, annotated with research-question mappings.
- `docs/research-questions.md` — editorial layer: the research questions used to tag/enrich harvested items, plus §Per-item enrichment and §Synthesis specs. Read it before changing summary/tagging behavior.
- `RUNBOOK.md` — the cloud agent's step-by-step daily procedure. Changing pipeline behavior usually means updating RUNBOOK.md too.

Pipeline flow: `run.py` → `staging/*.json` → (agent writes summary per RUNBOOK step 4) → `finalize.py` → `brain/` note + state update.

## Gotchas

- **Always seed new sources.** After adding to `sources.yaml`, run `python -m harvest.seed <type> <key>` or the next run backfills the source's entire history. Exception: `x` handles self-seed on first run.
- **`sources-state.json` is the dedup memory and is committed.** Deleting or reverting it causes mass re-harvesting.
- **Tag line contract:** the summary's final line holds tags (`#q12 #build ...`). `notes.py::extract_tags` reads only the last line — anything appended after it breaks frontmatter tag mirroring. No forced tags: unmatched items get no tag line and no enrichment sections.
- **Run errors are expected transients** (X challenges, yt-dlp bot blocks, dead feeds). Report them; don't retry within a run.
- **`npx defuddle-cli` is deprecated** (merged into `defuddle`) but still works; if it disappears, switch `harvest/extract.py` to the `defuddle` package.
- **Commit timing:** the cloud agent runs at 10:00 UTC. Local pipeline changes must be pushed before then to take effect same-day.
- X harvesting is deferred (`sources.yaml` `x: []`) pending password rotation.

## Environment (cloud agent)

Secrets: `OPENAI_API_KEY`, `X_USERNAME`, `X_PASSWORD` — never echo or commit. Deps: `requirements.txt`, `playwright install chromium`, plus `yt-dlp`, `ffmpeg`, `node` on PATH. Cloud env needs Network access = Full (egress proxy under Trusted mode blocks the feeds).
