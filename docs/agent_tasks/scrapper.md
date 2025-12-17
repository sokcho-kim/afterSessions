[Mode]
Planning mode. Show plan + file changes before applying.

[Mission]
Create the "raw → events" summarization pipeline for afterSessions.

[Context]
- Scraping/ingest is already set up.
- Raw artifacts exist under raw/YYYY/YYYY-MM-DD_slug/ with:
  - sources/source_*.txt
  - sources/source_*.meta.json
  - agenda.md, links.md, scrape_log.md (may exist)
- Events output should be created under events/YYYY/YYYY-MM-DD_slug/.

[Goal]
Implement scripts/after_sessions_summarize.py that:
- Reads raw folder for a given event
- Produces events folder files:
  - meta.yaml
  - 01_overview.md
  - 02_session-notes.md
  - 03_reflection.md
  - 04_actions.md

[Constraints]
- Standard library only (no new packages).
- Do not modify scrape/ingest logic.
- Do not delete any files.
- If output files already exist, do not overwrite by default; add --force to overwrite.
- Add caching: if source meta has content_hash and a previous run stored the same hash, skip re-summarization unless --force.

[CLI]
python scripts/after_sessions_summarize.py --date YYYY-MM-DD --slug SLUG
Optional:
  --year YY
