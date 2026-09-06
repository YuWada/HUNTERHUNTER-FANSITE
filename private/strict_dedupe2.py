import os
import difflib

db_dir = "/Users/yu/Antigravity_workspace/HUNTERHUNTER-FANSITE/public/hunterdata2/登場人物"
existing = [f for f in os.listdir(db_dir)]

with open('/Users/yu/Antigravity_workspace/HUNTERHUNTER-FANSITE/private/new_characters_to_add.txt', 'r', encoding='utf-8') as f:
    candidates = [line.strip() for line in f if line.strip()]

def clean(name):
    return name.replace('=', '').replace('＝', '').replace('・', '').replace(' ', '').replace('　', '')

existing_clean = {clean(name): name for name in existing}

duplicates = []
truly_new = []

for cand in candidates:
    c = clean(cand)
    if c in existing_clean:
        duplicates.append((cand, existing_clean[c], "exact"))
        continue
        
    matched = False
    for ex, orig in existing_clean.items():
        # Substring but only if it's a full word match when split by =
        cand_parts = cand.replace('＝','=').replace('・','=').split('=')
        orig_parts = orig.replace('＝','=').replace('・','=').split('=')
        
        # If any part matches exactly
        if any(p in orig_parts for p in cand_parts):
            # Verify they are actually the same person by looking at length or other context
            # A good heuristic: if the first part matches exactly, they are the same person
            if cand_parts[0] == orig_parts[0]:
                duplicates.append((cand, orig, "First name match"))
                matched = True
                break

        # Fuzzy match for typos (Levenshtein distance)
        ratio = difflib.SequenceMatcher(None, c, ex).ratio()
        if ratio >= 0.80:
            if c[:2] == ex[:2]: # Must start with same 2 letters
                duplicates.append((cand, orig, f"fuzzy ({ratio:.2f})"))
                matched = True
                break
                
    if not matched:
        truly_new.append(cand)

with open('/Users/yu/Antigravity_workspace/HUNTERHUNTER-FANSITE/private/truly_new_characters.txt', 'w', encoding='utf-8') as f:
    for c in sorted(truly_new):
        f.write(c + '\n')

with open('/Users/yu/Antigravity_workspace/HUNTERHUNTER-FANSITE/private/dedupe_log.txt', 'w', encoding='utf-8') as f:
    for cand, orig, reason in duplicates:
        f.write(f"REMOVED: {cand} == {orig} (Reason: {reason})\n")
