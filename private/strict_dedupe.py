import os
import difflib

db_dir = "/Users/yu/Antigravity_workspace/HUNTERHUNTER-FANSITE/public/hunterdata2/登場人物"
existing = [f for f in os.listdir(db_dir)]

with open('/Users/yu/Antigravity_workspace/HUNTERHUNTER-FANSITE/private/new_characters_to_add.txt', 'r', encoding='utf-8') as f:
    candidates = [line.strip() for line in f if line.strip()]

def clean(name):
    # Remove =, ＝, spaces, mid-dots, etc.
    return name.replace('=', '').replace('＝', '').replace('・', '').replace(' ', '').replace('　', '')

existing_clean = {clean(name): name for name in existing}
existing_names = list(existing_clean.keys())

def is_duplicate(cand):
    c = clean(cand)
    if c in existing_names: return True, existing_clean[c], "exact"
    
    for ex, orig in existing_clean.items():
        # Check if one is a substring of the other
        if c in ex and len(c) > 2: return True, orig, "substring"
        if ex in c and len(ex) > 2: return True, orig, "substring"
        
        # Check similarity
        ratio = difflib.SequenceMatcher(None, c, ex).ratio()
        if ratio > 0.7:
            # High similarity (e.g. トゥノフメイル vs タノフメール)
            # Make sure they share the same starting characters to avoid false positives (like ゴン and ジン)
            if c[:2] == ex[:2] and len(c) > 3 and len(ex) > 3:
                return True, orig, f"fuzzy ({ratio:.2f})"
        
        # Check first names
        # if they start with the same 4+ letters
        if len(c) >= 4 and len(ex) >= 4 and c[:4] == ex[:4]:
            return True, orig, "prefix"

    return False, None, None

truly_new = []
duplicates = []

for cand in candidates:
    dup, orig, reason = is_duplicate(cand)
    if dup:
        duplicates.append((cand, orig, reason))
    else:
        truly_new.append(cand)

with open('/Users/yu/Antigravity_workspace/HUNTERHUNTER-FANSITE/private/truly_new_characters.txt', 'w', encoding='utf-8') as f:
    for c in sorted(truly_new):
        f.write(c + '\n')

with open('/Users/yu/Antigravity_workspace/HUNTERHUNTER-FANSITE/private/dedupe_log.txt', 'w', encoding='utf-8') as f:
    for cand, orig, reason in duplicates:
        f.write(f"REMOVED: {cand} == {orig} (Reason: {reason})\n")

print(f"Candidates before strict dedupe: {len(candidates)}")
print(f"Removed as duplicates: {len(duplicates)}")
print(f"Truly new characters: {len(truly_new)}")
