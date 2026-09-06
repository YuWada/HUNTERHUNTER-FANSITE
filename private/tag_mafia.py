import os
import re

db_dir = "/Users/yu/Antigravity_workspace/HUNTERHUNTER-FANSITE/private/HUNTER_DATA/登場人物"
families = ["エイ＝イ一家", "シュウ＝ウ一家", "シャ＝ア一家"]

for filename in os.listdir(db_dir):
    if not filename.endswith(".md") or filename == "index.md":
        continue
    filepath = os.path.join(db_dir, filename)
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()
    
    # Check if any family name is heavily implied or mentioned in the text
    # We will look at the text below the frontmatter
    parts = content.split("---")
    if len(parts) < 3:
        continue
    
    frontmatter = parts[1]
    body = "---".join(parts[2:])
    
    updated_tags = False
    
    for family in families:
        if family in body:
            # Check if family is already in tags
            tags_match = re.search(r"tags:\s*\[(.*?)\]", frontmatter)
            if tags_match:
                tags_str = tags_match.group(1)
                tags = [t.strip().strip("'").strip('"') for t in tags_str.split(",") if t.strip()]
                if family not in tags:
                    # Also we should only add the tag if they are actually a member, 
                    # but typically if their file mentions it prominently, they might be.
                    # Let's do a stricter check: "マフィア「エイ＝イ一家」の構成員" or similar.
                    # Or we can just add it if they belong to it.
                    pass

