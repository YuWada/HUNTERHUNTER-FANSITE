import os
import re

db_dir = "/Users/yu/Documents/Daiv_Antigravity/Antigravity20/HUNTER_DATA/登場人物"
existing_files = [f.replace('.md', '') for f in os.listdir(db_dir) if f.endswith('.md')]

with open('/Users/yu/Antigravity_workspace/HUNTERHUNTER-FANSITE/private/db_character_candidates.txt', 'r', encoding='utf-8') as f:
    candidates = [line.strip() for line in f if line.strip()]

# Normalize for comparison (remove =, spaces, etc)
def normalize(name):
    return name.replace('=', '').replace('＝', '').replace(' ', '').replace('　', '')

existing_normalized = {normalize(name): name for name in existing_files}
existing_names_set = set(existing_files)

new_chars = []
for c in candidates:
    norm_c = normalize(c)
    
    # Check exact match
    if c in existing_names_set:
        continue
        
    # Check normalized match
    if norm_c in existing_normalized:
        continue
        
    # Check if this candidate is a subset of an existing character
    # e.g. "ゴン" is a subset of "ゴン=フリークス"
    is_subset = False
    for ex in existing_normalized:
        if norm_c in ex:
            is_subset = True
            break
    if is_subset:
        continue
        
    # Check if an existing character is a subset of this candidate
    # (Maybe the DB has "ゴン" and we found "ゴン=フリークス", then it's technically a new full name but refers to the same person)
    has_subset_in_db = False
    for ex in existing_normalized:
        if ex in norm_c:
            has_subset_in_db = True
            # We might want to flag this as "DB update needed" but the user asked for "newly registered"
            break
            
    if has_subset_in_db:
        continue
        
    new_chars.append(c)

with open('/Users/yu/Antigravity_workspace/HUNTERHUNTER-FANSITE/private/new_characters_to_add.txt', 'w', encoding='utf-8') as f:
    for c in sorted(new_chars):
        f.write(c + '\n')

print(f"Total candidates: {len(candidates)}")
print(f"Existing in DB: {len(existing_files)}")
print(f"New characters to add: {len(new_chars)}")
