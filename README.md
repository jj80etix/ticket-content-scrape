# ticket-content-scrape

Daily content harvest (YouTube / articles / podcasts / X) into an Obsidian
vault at `brain/`.

- Design spec: `brain/docs/specs/2026-07-06-content-harvest-pipeline-design.md`
- Implementation plan: `brain/docs/plans/2026-07-06-content-harvest-pipeline.md`
- Daily automation: `RUNBOOK.md` (cloud-scheduled Claude agent)

Usage:
- `sources.yaml` — subscriptions. After adding a source, seed it:
  `python -m harvest.seed <type> <source_key>`
- `sources-state.json` — dedup memory (committed).
- `python -m harvest.run` — stage new items to `staging/`.
- `python -m harvest.finalize <staged.json> <summary.md>` — write final note.
- Tests: `pytest`
