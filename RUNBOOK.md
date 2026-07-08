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
      `### Key Points` list of 3-7 bullets. If the item matches one or more
      research questions, add the three enrichment sections per
      `docs/research-questions.md` §Per-item enrichment: `### Highlights`,
      `### Industry Problem`, `### Proposed Solution`. End with a final tag
      line (e.g. `#q12 #build #ticketmaster`; no tags — and no enrichment
      sections — if nothing clearly applies; never force a match). The tag
      line must stay the last line of the file.
   c. `python -m harvest.finalize staging/<file>.json <summary-file>`
5. Rewrite the daily note `brain/YYYY-MM-DD.md` as a daily summary report
   per `docs/research-questions.md` §Synthesis (Daily): Highlights first
   (regulatory/legal Q5, Q9–Q11 — one-line why + any effective dates), then
   items grouped by question with a one-line takeaway each, then untagged
   items as bare links under "Other". Keep the `[[wikilinks]]` written in
   step 4c.
6. `git add brain/ sources-state.json && git commit -m "harvest: $(date +%F)"`
   (skip commit if nothing changed).
7. `git push origin main`.
8. Report: paste the daily summary report, then items harvested per type and
   errors.
9. Mondays: before step 6, write the weekly digest; 1st of month: the monthly
   rollup — both per `docs/research-questions.md` §Synthesis, into
   `brain/digests/`.

Adding a source later: append to `sources.yaml`, then run
`python -m harvest.seed <type> <source_key>` so history isn't backfilled
(x handles need no seeding — the first run seeds itself).
