# Naming Conventions

## Directory Naming
- **Event Directory**: `YYYY-MM-DD_slug`
  - Example: `2025-12-17_claude-code-meetup`
  - Location: 
    - `events/YYYY/YYYY-MM-DD_slug/`
    - `raw/YYYY/YYYY-MM-DD_slug/`

## File Naming (`events/` folder)
Inside `events/YYYY/YYYY-MM-DD_slug/`:
- `meta.yaml`: Metadata for the event
- `01_overview.md`: General overview and motivation
- `02_session-notes.md`: Detailed session notes
- `03_reflection.md`: Personal reflections and key takeaways
- `04_actions.md`: Follow-up action items

## File Naming (`raw/` folder)
Inside `raw/YYYY/YYYY-MM-DD_slug/`:
- `agenda.txt`: Copy-pasted agenda or schedule
- `my_notes.md`: Rough notes taken during the event
- `etc/`: Folder for images, PDFs, or other raw materials
