import os
import argparse
import datetime
import shutil

def create_directory(path):
    if not os.path.exists(path):
        os.makedirs(path)
        print(f"Created directory: {path}")
    else:
        print(f"Directory already exists: {path}")

def read_template(template_path):
    try:
        with open(template_path, 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        print(f"Template not found: {template_path}")
        return ""

def write_file(path, content):
    if not os.path.exists(path):
        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Created file: {path}")
    else:
        print(f"File already exists: {path}")

def main():
    parser = argparse.ArgumentParser(description="Initialize a new event session.")
    parser.add_argument("--date", required=True, help="Event date in YYYY-MM-DD format")
    parser.add_argument("--slug", required=True, help="URL-friendly slug for the event name")
    parser.add_argument("--title", help="Title of the event", default="")
    parser.add_argument("--tags", help="Comma-separated tags", default="")

    args = parser.parse_args()

    try:
        event_date = datetime.datetime.strptime(args.date, "%Y-%m-%d")
    except ValueError:
        print("Error: Date must be in YYYY-MM-DD format")
        return

    year = str(event_date.year)
    folder_name = f"{args.date}_{args.slug}"

    # Base paths
    root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    events_dir = os.path.join(root_dir, "events", year, folder_name)
    raw_dir = os.path.join(root_dir, "raw", year, folder_name)

    # 1. Create Directories
    create_directory(events_dir)
    create_directory(raw_dir)
    create_directory(os.path.join(raw_dir, "etc"))

    # 2. Create Files in events/
    # Load template
    template_path = os.path.join(root_dir, "templates", "event-notes-template.md")
    template_content = read_template(template_path)

    # Fill template metadata
    filled_content = template_content
    if args.title:
        filled_content = filled_content.replace("title: ", f"title: {args.title}")
    if args.date:
        filled_content = filled_content.replace("date: ", f"date: {args.date}")
    
    # Handle tags
    if args.tags:
        tags_list = [t.strip() for t in args.tags.split(',')]
        tags_str = str(tags_list).replace("'", '"') # simple conversion to yaml list style
        filled_content = filled_content.replace("tags: []", f"tags: {tags_str}")

    # meta.yaml (simple placeholder)
    meta_content = f"slug: {args.slug}\ndate: {args.date}\ntitle: {args.title}\n"
    write_file(os.path.join(events_dir, "meta.yaml"), meta_content)
    
    # Markdown files
    # 02_session-notes.md gets the template content
    write_file(os.path.join(events_dir, "02_session-notes.md"), filled_content)
    
    # Others are empty or minimal
    write_file(os.path.join(events_dir, "01_overview.md"), f"# Overview: {args.title}\n")
    write_file(os.path.join(events_dir, "03_reflection.md"), "# Reflections\n")
    write_file(os.path.join(events_dir, "04_actions.md"), "# Action Items\n")

    # 3. Create Files in raw/
    write_file(os.path.join(raw_dir, "agenda.txt"), "Paste agenda here.\n")
    write_file(os.path.join(raw_dir, "my_notes.md"), "# Raw Notes\n")

    print(f"\nSuccessfully initialized session: {folder_name}")

if __name__ == "__main__":
    main()
