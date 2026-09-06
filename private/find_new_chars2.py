import os
import re

db_dir = "/Users/yu/Antigravity_workspace/HUNTERHUNTER-FANSITE/public/hunterdata2/登場人物"
existing_items = [f for f in os.listdir(db_dir) if os.path.isdir(os.path.join(db_dir, f))]

nen_dir = "/Users/yu/Antigravity_workspace/HUNTERHUNTER-FANSITE/public/hunterdata2/念能力"
nen_items = [f for f in os.listdir(nen_dir) if os.path.isdir(os.path.join(nen_dir, f))]

with open('/Users/yu/Antigravity_workspace/HUNTERHUNTER-FANSITE/private/db_character_candidates.txt', 'r', encoding='utf-8') as f:
    candidates = [line.strip() for line in f if line.strip()]

def normalize(name):
    return name.replace('=', '').replace('＝', '').replace(' ', '').replace('　', '')

existing_normalized = {normalize(name): name for name in existing_items}
nen_normalized = {normalize(name): name for name in nen_items}

new_chars = []
for c in candidates:
    norm_c = normalize(c)
    
    # Check if exists in chars
    if norm_c in existing_normalized:
        continue
    # Check if exists in nen
    if norm_c in nen_normalized:
        continue
        
    # Check subsets for chars
    is_subset = False
    for ex in existing_normalized:
        if norm_c in ex and len(norm_c) >= 2: # prevent single letter matches
            is_subset = True
            break
    if is_subset: continue
    
    # Check subsets for nen
    is_nen_subset = False
    for ex in nen_normalized:
        if norm_c in ex and len(norm_c) > 3:
            is_nen_subset = True
            break
    if is_nen_subset: continue

    new_chars.append(c)

with open('/Users/yu/Antigravity_workspace/HUNTERHUNTER-FANSITE/private/new_characters_to_add.txt', 'w', encoding='utf-8') as f:
    for c in sorted(new_chars):
        f.write(c + '\n')

print(f"Total candidates: {len(candidates)}")
print(f"Existing chars in DB: {len(existing_items)}")
print(f"Existing nen in DB: {len(nen_items)}")
print(f"New characters to add: {len(new_chars)}")
