import os
import yaml

base_dir = "build_src/docs"
order = ["ストーリー", "登場人物", "念能力", "グリードアイランド_カード", "用語集"]

nav = []
nav.append({"神眼DBホーム": "index.md"})

for section in order:
    section_dir = os.path.join(base_dir, section)
    if os.path.isdir(section_dir):
        # We need a list of dicts for the section
        section_files = []
        # Put index.md first if it exists
        if os.path.exists(os.path.join(section_dir, "index.md")):
            section_files.append({"ホーム": f"{section}/index.md"})
            
        # Get all other .md files
        for root, dirs, files in os.walk(section_dir):
            for file in sorted(files):
                if file.endswith(".md") and file != "index.md":
                    # Remove .md for title
                    title = file[:-3]
                    # Relative path from base_dir
                    rel_path = os.path.relpath(os.path.join(root, file), base_dir)
                    section_files.append({title: rel_path})
        
        # Determine the display name for the section
        display_name = section
        if display_name == "グリードアイランド_カード":
            display_name = "G.I.カード"
            
        nav.append({display_name: section_files})

# Load the existing mkdocs.yml and update the nav
with open("build_src/mkdocs.yml", "r", encoding="utf-8") as f:
    config = yaml.safe_load(f)

config["nav"] = nav

with open("build_src/mkdocs.yml", "w", encoding="utf-8") as f:
    yaml.dump(config, f, allow_unicode=True, sort_keys=False)
