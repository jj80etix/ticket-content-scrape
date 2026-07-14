# Ticketing Industry Intelligence — Research Questions

Editorial guide for the daily harvest. The scheduled agent reads this every run.
It drives three things:

1. **Source selection** — what belongs in `sources.yaml` (each question's
   "feeds reachable today" column is the subscribe list).
2. **Per-item tagging** — every note summary ends with an inline tag line
   (see Tagging). This is what turns a pile of notes into a queryable corpus.
3. **Synthesis digests** — weekly/monthly rollups per question (see Synthesis).
   The pipeline is subscription-pull: items arrive when published, so
   "refresh cadence" applies to synthesis, not fetching.

**Source weighting:** prioritize original sources (regulator sites, filings,
primary press releases) over aggregators. Treat consumer-sentiment sources
(Reddit, reviews) as signal for *pain points and unmet needs*, never as fact
for regulatory or market-structure questions.

---

## Tagging

At summarize time (RUNBOOK step 4b), end each summary with one tag line:

```
#q12 #build #improve #ticketmaster
```

- `#qN` — every question the item substantively informs (0, 1, or several).
- Decision tags — copy from the matched questions' Decision column:
  `#monitor #build #improve #evolve #ai-context`.
- Entity tags — lowercase-kebab: companies (`#ticketmaster`, `#seatgeek`),
  regulators (`#ftc`, `#doj`), bills/laws (`#bots-act`, `#ticket-act`,
  `#clarity-act`), cases (`#doj-v-livenation`).
- **Never force a match.** An item matching no question gets no tags — that is
  correct behavior, not a failure.

| Tag | Meaning | Downstream use |
|-----|---------|----------------|
| `#monitor` | Situational awareness; no immediate action | Weekly digest |
| `#build` | Signals new product/feature to create | Roadmap input |
| `#improve` | Signals refinement of existing product | Roadmap input |
| `#evolve` | Long-horizon strategic direction | Monthly digest |
| `#ai-context` | Grounding material for internal AI (Etix Assistant) | AI corpus |

`#ai-context` applies beyond Q14: client/patron pain-point content (Q1, Q2)
and win/loss reasoning (Q20) are prime grounding material — tag them.

## Per-item enrichment

When an item matches at least one question (i.e. it gets `#qN` tags), the
summary also carries three sections, each written *through the lens of the
matched questions*:

- `### Highlights` — 2-4 bullets: facts in this item that most directly
  inform the matched questions (numbers, dates, named parties, deadlines).
- `### Industry Problem` — 1-3 sentences: the underlying client/patron/
  industry pain point or structural issue this item evidences. Anchor to the
  question's framing (e.g. Q2 → patron pain, Q9 → compliance burden).
- `### Proposed Solution` — 1-3 sentences: the solution the item itself
  describes, if any, plus what an independent primary platform (Etix) could
  build or improve in response. Align with the matched questions' decision
  tags: `#build`/`#improve` → concrete product response; `#monitor`/`#evolve`
  → what to watch and the trigger that would change posture.

Unmatched items get none of these sections — summary + key points only.

## Synthesis

- **Daily (every run):** the daily note `brain/ticket-content-scrape/YYYY-MM-DD.md` is a summary
  report, not a bare link list. Format:
  1. `## Highlights` — regulatory/legal items (Q5, Q9–Q11) first, one line
     each: what changed, why it matters, effective dates/deadlines. Empty if
     none — omit the section, don't pad.
  2. `## By question` — one `### Qn — <short title>` block per question with
     matched items; each item is a `[[wikilink]]` + one-line takeaway.
  3. `## Other` — untagged items, bare `[[wikilinks]]`.
- **Weekly (Mondays):** digest of the week's `#monitor`-tagged notes, grouped
  by question, written to `brain/ticket-content-scrape/digests/YYYY-Www.md`. Flag anything
  regulatory/legal (Q9–Q11, Q5) that looks time-sensitive at the top.
- **Monthly (1st):** strategic rollup of `#build` / `#improve` / `#evolve`
  notes → `brain/ticket-content-scrape/digests/YYYY-MM.md`. This is where Q8, Q19, Q20 actually get
  answered — by cross-referencing a month of accumulated evidence, not by any
  single item.
- Digests cite notes as `[[wikilinks]]`; no new facts, only rollup.

## Source feasibility & phase status

The pipeline fetches RSS/Atom (articles, podcasts), YouTube channels, and X
handles. Subscribe what's reachable; the rest is marked **needs-new-fetcher**
and answered only via synthesis or manual feed-in.

**Phase 1 — SUBSCRIBED + seeded 2026-07-06** (live in `sources.yaml`):
- TheTicketingBusiness — `https://www.theticketingbusiness.com/feed/` (Q1, Q3, Q6, Q9–Q13)
- TicketNews — `https://www.ticketnews.com/feed/` (Q2, Q6, Q9, Q11; US focus)
- Pollstar — `https://news.pollstar.com/feed/` (Q1, Q3, Q8, Q13; main-site /feed is HTML — use news subdomain)
- IQ Magazine — `https://www.iqmagazine.com/feed/` (Q3, Q6, Q11; iq-mag.net redirects here)
- FTC press releases — `https://www.ftc.gov/feeds/press-release.xml` (Q9, Q10; requires browser UA — set in `harvest/feeds.py`)
- Regulatory Oversight (Troutman Pepper) — `https://www.regulatoryoversight.com/feed/` (Q9, Q11; state-AG / junk-fee alerts). Substituted for National Law Review: NLR exposes only an all-practice firehose (~40 items/poll, no topic feeds). JD Supra syndication page is JS-only — no static RSS found; unresolved.

**Phase 2 — hold until Phase 1 validated:**
- VenuesNow RSS (Q1, Q3)
- Subreddit `.rss` (r/Ticketmaster) — high noise, patron-sentiment only (Q2)
- Queue-it blog (Q18); fraud/security vendor blogs (Q7)
- GovTrack per-bill feeds — TICKET Act, CLARITY Act, BOTS enforcement (Q5, Q11)
- CourtListener docket RSS — *DOJ v. Live Nation* (Q10)
- Tier 1 competitor blogs/newsrooms with feeds (Q12, Q14)
- Stripe/Adyen/payments trade press RSS (Q15)

**Deferred — blocked, do not start:**
- X handles (competitor + reporter accounts) — pending X password rotation
- Needs-new-fetcher: G2/Capterra, Trustpilot, app-store reviews,
  Crunchbase/PitchBook, earnings-call transcripts, court trackers beyond
  CourtListener, internal CRM/win-loss data.

---

## 1. Pain points & unmet needs

| ID | Question | Decision | Sources |
|----|----------|----------|---------|
| Q1 | Biggest pain point for **clients** (venues, promoters, organizers)? | Improve, Build, AI-Context | Trade press; organizer forums/LinkedIn; INTIX coverage; *(needs-fetcher: G2/Capterra)* |
| Q2 | Biggest pain point for **patrons** (buyers) — fees, checkout, entry, resale, refunds? | Improve, Build, AI-Context | Reddit RSS; social; *(needs-fetcher: Trustpilot, app-store reviews, BBB/FTC complaint data)* |
| Q3 | Biggest pain point for **ticketing/event-management companies** (peers)? | Monitor, Evolve | Trade press; analyst notes; *(needs-fetcher: earnings calls)* |
| Q19 | What are clients asking for that **no vendor serves well** (whitespace)? | Build | Answered via monthly synthesis over Q1/Q12 notes; *(needs-fetcher: review sites, public RFPs)* |
| Q20 | **Why do clients churn / choose competitors** (win/loss)? | Build, Improve, AI-Context | Answered via monthly synthesis; competitor switch announcements; feed CRM/win-loss notes in manually if desired |

## 2. Competitive & market structure

| ID | Question | Decision | Sources |
|----|----------|----------|---------|
| Q12 | What are competitors **shipping** — feature launches, fee-model changes, redesigns? **Tier 1, direct primary-platform (highest build/improve signal):** Eventbrite, See Tickets, DICE, Tixr, AudienceView (incl. OvationTix/TheaterMania), Spektrix, PatronManager, Tessitura, Prekindle, TicketSpice, ThunderTix. **Tier 2, consumer majors (expectation-setters):** Ticketmaster, AXS, SeatGeek. **Tier 3, resale (Q6 context only):** StubHub, Vivid Seats, Gametime. | Build, Improve | Company blogs/newsrooms; product-launch coverage; job postings; X handles; app-store update notes |
| Q13 | What **M&A / consolidation** — who is entering or exiting? | Monitor, Evolve | Press releases; trade press; *(needs-fetcher: Crunchbase/PitchBook, earnings calls)* |

## 3. Regulatory & legal

| ID | Question | Decision | Sources |
|----|----------|----------|---------|
| Q9 | How is **all-in / junk-fee pricing regulation** evolving (FTC rule + state patchwork)? Most operationally consequential story for a primary platform. | Improve, Monitor | FTC.gov RSS; state AG sites; JD Supra / National Law Review topic feeds |
| Q10 | How is **Live Nation / Ticketmaster antitrust + deceptive-pricing litigation** progressing? Model competitive openings for independents. | Monitor, Evolve | CourtListener docket RSS; DOJ/FTC releases; trade & legal press |
| Q11 | Where are **resale/transferability, price caps, BOTS Act enforcement, speculative-ticketing bans** heading? | Monitor, Improve | GovTrack bill feeds; state legislatures; law-firm alerts; trade press |
| Q5 | Would the **CLARITY Act** change ticketing? Crypto market-structure law, not ticketing law — watch as enabler of Q4 (token clarity de-risks blockchain ticketing). Not yet law (cleared Senate Banking May 2026). | Monitor, Evolve | GovTrack; SEC/CFTC; crypto-policy trackers |

## 4. Technology & AI

| ID | Question | Decision | Sources |
|----|----------|----------|---------|
| Q7 | Latest tech to **combat fraud** — bot mitigation, identity verification, rotating/secure barcodes, ML detection? | Improve, Build | Fraud/security vendor blogs; competitor security announcements; trade press |
| Q14 | Beyond fraud, how are platforms **deploying AI** (support, forecasting, dynamic pricing, personalization)? Benchmark for Etix Assistant. | Build, Improve, AI-Context | Competitor blogs/docs/demos; conference talks; trade press |
| Q18 | How is the industry solving **high-demand onsale scalability + bot defense at scale** (queue-meltdown problem)? | Improve, Build | Queue-vendor blogs; onsale post-mortems; engineering talks |
| Q4 | How could ticketing **evolve using blockchain** — credible uses (provenance, verifiable transfer, resale royalties) vs hype? | Evolve, Monitor | Blockchain-ticketing vendor blogs; pilot/case-study coverage; trade press |

## 5. Patron experience & demand-side trends

| ID | Question | Decision | Sources |
|----|----------|----------|---------|
| Q15 | How are **payment methods shifting** (BNPL, tap-to-pay, wallets) and conversion impact? | Build, Improve | Payments trade press; PSP blogs (Stripe, Adyen); fintech reports |
| Q16 | Expectations around **digital-only entry, accessibility/ADA flows, refund/insurance flexibility**? | Improve, Build | Trade press; accessibility advocacy; competitor feature pages |
| Q17 | Is the industry moving toward **loyalty, membership, subscription** models? | Evolve, Build | Trade press; case studies; adjacent-industry models |

## 6. Forward bets

| ID | Question | Decision | Sources |
|----|----------|----------|---------|
| Q6 | Current state of the **secondary market** — volume, pricing, platform share, transferability? | Monitor | Trade press; analyst coverage; *(needs-fetcher: StubHub/Vivid/SeatGeek filings)* |
| Q8 | **Where is the next big opportunity?** Answered via monthly synthesis, cross-referenced against Q19/Q20 evidence. | Evolve, Build | VC/analyst reports; conference keynotes; adjacent-industry trends |

---

*Scope notes:* Q1–Q8 = original set (Q5 reframed). Q9–Q20 = additions. IDs are
stable forever — notes carry `#qN` tags, so never renumber; retire IDs instead.
The daily run only summarizes and tags subscribed feeds; it does no open web
research. If a question is starving, either add feeds for it or add an explicit
monthly research pass (WebSearch by the scheduled agent) — not yet enabled.
