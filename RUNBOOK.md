# Daily Harvest Runbook (scheduled agent)

Secrets required in the agent environment: `OPENAI_API_KEY`, `X_USERNAME`,
`X_PASSWORD`, plus GitHub push access to this repo. Never echo or commit them.

1. `git pull --rebase origin main` (pick up local edits; abort run on
   conflict and report).
2. Install deps if needed: `pip install -r requirements.txt`,
   `playwright install chromium`; ensure `yt-dlp`, `ffmpeg`, `node` on PATH.
   Note: article extraction shells out to `npx defuddle-cli` — the npm package is deprecated (merged into `defuddle`) but still works; if it disappears, switch `harvest/extract.py` to the `defuddle` package.
3. Run `python -m harvest.run`. Note the `staged=N errors=M` line. Errors are
   expected transients (X challenges, yt-dlp bot blocks, dead feeds) — report
   them in the run summary, do not retry within the run.
4. For EACH file in `staging/`:
   a. Read the JSON; read its `content`.
   b. Write a summary to a temp file: 2-4 sentence overview, then a
      `### Key Points` list of 3-7 bullets.
   c. `python -m harvest.finalize staging/<file>.json <summary-file>`
5. `git add brain/ sources-state.json && git commit -m "harvest: $(date +%F)"`
   (skip commit if nothing changed).
6. `git push origin main`.
7. Report: items harvested per type, errors, note links.

Adding a source later: append to `sources.yaml`, then run
`python -m harvest.seed <type> <source_key>` so history isn't backfilled.
