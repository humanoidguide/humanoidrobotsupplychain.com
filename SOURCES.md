# The Briefing — Trusted Sources (allowlist)

This list controls which sources the scheduled news publisher may cite. **If the original
source of a story is not on this list, the story is not published.** Edit this file to add
or remove sources — the publisher reads it on every run.

## Publishing rules (enforced by the publisher)

1. Only publish stories whose original source is on this list. Link the original, never an aggregator rewrite.
2. The cited article must actually be fetched and read before writing — never write from a headline alone.
3. Big claims (funding amounts, IPOs, valuations, "first ever") require **two independent listed sources
   OR confirmation in the company's own press release**.
4. Capability claims are always attributed: "according to [company]".
5. Summaries in our own words, 1–2 sentences. No copied text.
6. Images — every item should have one when a rights-safe candidate exists, in this order:
   (a) the company's own press/newsroom images — credit "Image © [Company]";
   (b) humanoid.guide's own images for humanoid.guide stories — credit "Image © Humanoid Guide";
   (c) openly licensed images (CC BY / CC0, e.g. Wikimedia Commons) — credit with author and
       license, e.g. "Image: [Author] / Wikimedia Commons, CC BY 4.0";
   (d) otherwise the branded color card (art + artTitle).
   The credit is stored in the "credit" field and rendered automatically at the start of the
   summary. NEVER use other publications' article photos — credit does not equal a license.
7. No suitable story = skip the run. Never publish filler.
8. Deduplicate against the existing news.json archive before publishing.

## Tier 1 — business & tech press (one source sufficient for routine news)

- Reuters
- Bloomberg
- Financial Times
- The Wall Street Journal
- CNBC
- TechCrunch
- The Verge
- Ars Technica
- Axios
- Nikkei Asia
- IEEE Spectrum

## Tier 1 — robotics trade press

- The Robot Report
- Robotics 24/7

## Primary sources (always acceptable, preferred for big claims)

- Official company newsrooms / press pages (e.g. limxdynamics.com, agilityrobotics.com, figure.ai, 1x.tech, unitree.com)
- Official investor-relations pages and regulatory filings

## Own coverage

- humanoid.guide

## Never publish from

- SEO content farms and anonymous aggregator blogs
- AI-generated "news" sites
- Social media posts as the sole source (may be used as a tip, must be confirmed by a listed source)
- Press-release wire dumps without a named company newsroom behind them
