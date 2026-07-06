# Content Harvest Pipeline — Design Spec

Date: 2026-07-06
Status: approved (pending final sign-off before implementation plan)

## Purpose

Daily automated harvesting of content from YouTube, articles, podcasts, and X (Twitter) into a searchable, organized personal knowledge base. Subscription-based — new sources can always be added without re-architecting the pipeline.

## Repo

`/Users/jjchambers/Intellimark/ticket-content-scrape` (github.com/jj80etix/ticket-content-scrape, `main` branch). Fully separate from the etix codebase — avoids bloating that repo as this vault grows over time.

## Architecture

### Trigger

Cloud-scheduled agent (via `/schedule`), runs once daily. Not dependent on local machine being on.

### Configuration

- `sources.yaml` (repo root) — subscription list, one section per source type:
  - `youtube`: channel IDs
  - `articles`: RSS feed URLs
  - `podcasts`: RSS feed URLs
  - `x`: account handles / list URLs
- `sources-state.json` (repo root) — dedup state: seen item IDs/URLs per source, so re-runs only process new items.

**First-run seeding:** when a source appears in `sources.yaml` for the first time, its current feed items are seeded into `sources-state.json` as "seen" WITHOUT processing (optionally processing the N most recent, default 0). Prevents backfill floods — e.g. transcribing a podcast's entire archive on day one.

### Per-source-type fetch & processing

| Type | Fetch | Extract | Cost |
|---|---|---|---|
| YouTube | channel RSS feed → new video IDs | yt-dlp captions (reuse existing youtube-transcript skill logic) | free |
| Article | RSS feed → new entries | defuddle skill → clean markdown | free |
| Podcast | RSS enclosure → new episodes | download audio → OpenAI Whisper API transcription | ~$0.006/min |
| X | headless browser (Playwright) login → account/list timeline | scrape recent posts/threads | free (browser-based) |

Each new item gets: full transcript/text stored, plus a generated summary + key-points section on top.

Notes per type:
- **X:** login uses a dedicated scrape account; credentials supplied via the scheduled agent's secret/env config — never committed to this repo or the spec. Automated logins from cloud IPs may trigger X challenges/lockouts; treat X failures as expected transients (retry next run). If lockouts become chronic, fall back to a local run for X only or the paid X API.
- **Podcast:** OpenAI Whisper API has a 25MB/request limit — episodes above it are chunked (e.g. ffmpeg segment) and transcripts concatenated.
- **YouTube:** yt-dlp from datacenter IPs is intermittently bot-blocked; expected transient, covered by retry-next-run.

### Storage layout

Content lives under `brain/` at repo root (mirrors the existing etix `brain/` vault convention):

```
ticket-content-scrape/
├── sources.yaml
├── sources-state.json
└── brain/                     # Obsidian vault root
    ├── docs/specs/            # design specs (this doc)
    ├── youtube/YYYY-MM-DD-slug.md
    ├── articles/YYYY-MM-DD-slug.md
    ├── podcasts/YYYY-MM-DD-slug.md
    ├── x/YYYY-MM-DD-slug.md
    └── YYYY-MM-DD.md          # daily index note, links to that day's items
```

Each per-item note has frontmatter: `title`, `author` (channel/show/handle/byline), `source`, `url`, `type`, `date`, `tags` — title+author make the daily index readable.

### Error handling

- Per-source fetch failures are isolated — one broken feed doesn't block other sources that day.
- If transcription/extraction fails for an item, it is NOT marked "seen" in `sources-state.json` — retried on next run.

### Persistence

The cloud job clones the repo from GitHub (push credentials via the scheduled agent's GitHub access), pulls latest `main` before processing (picks up local edits, avoids conflicts), then commits new notes/state and pushes to `origin/main` each run — fully hands-off, vault stays backed up daily. The local path `/Users/jjchambers/Intellimark/ticket-content-scrape` is the user's working clone, not the job's runtime.

## Out of scope (for this iteration)

- No digest/summary rollup beyond the daily index note (no weekly/monthly rollups yet).
- No search/query tooling over the vault (Obsidian itself, or a future skill, handles retrieval).
- No credential/auth setup instructions for X login or Whisper API key — those are implementation-plan concerns, not design concerns.
