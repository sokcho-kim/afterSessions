import os
import argparse
import datetime
import hashlib
import json
import shutil

def get_file_content(path):
    if os.path.exists(path):
        with open(path, 'r', encoding='utf-8') as f:
            return f.read()
    return ""

def write_file(path, content):
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Created/Updated: {path}")

def calculate_checksum(directory):
    """Calculates a simple checksum of all files in the directory to detect changes."""
    sha256_hash = hashlib.sha256()
    if not os.path.exists(directory):
        return ""
    
    for root, _, files in sorted(os.walk(directory)):
        for names in sorted(files):
            filepath = os.path.join(root, names)
            try:
                with open(filepath, "rb") as f:
                    # Read and update hash string value in blocks of 4K
                    for byte_block in iter(lambda: f.read(4096), b""):
                        sha256_hash.update(byte_block)
            except OSError:
                pass
    return sha256_hash.hexdigest()

def main():
    parser = argparse.ArgumentParser(description="Summarize raw event data into structured event notes.")
    parser.add_argument("--date", required=True, help="Event date (YYYY-MM-DD)")
    parser.add_argument("--slug", required=True, help="Event slug")
    parser.add_argument("--force", action="store_true", help="Overwrite existing files and ignore cache")
    
    args = parser.parse_args()
    
    try:
        event_date = datetime.datetime.strptime(args.date, "%Y-%m-%d")
    except ValueError:
        print("Error: Date must be in YYYY-MM-DD format")
        return

    year = str(event_date.year)
    folder_name = f"{args.date}_{args.slug}"
    
    root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    raw_dir = os.path.join(root_dir, "raw", year, folder_name)
    events_dir = os.path.join(root_dir, "events", year, folder_name)

    if not os.path.exists(raw_dir):
        print(f"Error: Raw directory not found: {raw_dir}")
        return

    # Checksum logic
    current_checksum = calculate_checksum(raw_dir)
    meta_path = os.path.join(events_dir, "meta.yaml")
    
    if os.path.exists(events_dir) and not args.force:
        # Try to read existing checksum from meta (if we were storing it there, 
        # but YAML parsing with regex/simple read is safer to avoid pyyaml dependency)
        existing_content = get_file_content(meta_path)
        if f"raw_checksum: {current_checksum}" in existing_content:
            print(f"Skipping {folder_name}: No changes in raw data (Checksum match). Use --force to overwrite.")
            return

    if not os.path.exists(events_dir):
        os.makedirs(events_dir)
        print(f"Created events directory: {events_dir}")

    # Gather content
    agenda_content = get_file_content(os.path.join(raw_dir, "agenda.txt"))
    if not agenda_content:
        agenda_content = get_file_content(os.path.join(raw_dir, "agenda.md")) # Fallback
    
    my_notes_content = get_file_content(os.path.join(raw_dir, "my_notes.md"))
    links_content = get_file_content(os.path.join(raw_dir, "links.md"))
    
    sources_content = ""
    sources_dir = os.path.join(raw_dir, "sources")
    if os.path.exists(sources_dir):
        for filename in sorted(os.listdir(sources_dir)):
            if filename.endswith(".txt"):
                sources_content += f"\n\n### Source: {filename}\n"
                sources_content += get_file_content(os.path.join(sources_dir, filename))

    # Generate Files
    
    # meta.yaml
    meta_yaml = f"""slug: {args.slug}
date: {args.date}
raw_checksum: {current_checksum}
generated_at: {datetime.datetime.now().isoformat()}
"""
    write_file(meta_path, meta_yaml)

    # 01_overview.md
    overview_md = f"""# Overview
## Agenda
{agenda_content}

## My Initial Notes
{my_notes_content}
"""
    write_file(os.path.join(events_dir, "01_overview.md"), overview_md)

    # 02_session-notes.md
    session_notes_md = f"""# Session Notes
{sources_content}
"""
    write_file(os.path.join(events_dir, "02_session-notes.md"), session_notes_md)

    # 03_reflection.md (Append only if exists? No, overwrite based on pipeline logic, but keep safe)
    # Strategy: If file exists and not forcing, we already returned. So here we just write.
    reflection_md = f"""# Reflections
## References
{links_content}
"""
    write_file(os.path.join(events_dir, "03_reflection.md"), reflection_md)

    # 04_actions.md
    actions_md = """# Action Items
- [ ] Review session notes
- [ ] Organize key takeaways
"""
    write_file(os.path.join(events_dir, "04_actions.md"), actions_md)

    print(f"Successfully summarized event to: {events_dir}")

if __name__ == "__main__":
    main()
