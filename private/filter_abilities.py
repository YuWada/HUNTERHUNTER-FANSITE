import os

nen_dir = "/Users/yu/Documents/Daiv_Antigravity/Antigravity20/HUNTER_DATA/念能力"
nen_files = [f.replace('.md', '') for f in os.listdir(nen_dir) if f.endswith('.md')]

with open('/Users/yu/Antigravity_workspace/HUNTERHUNTER-FANSITE/private/new_characters_to_add.txt', 'r', encoding='utf-8') as f:
    new_chars = [line.strip() for line in f if line.strip()]

def normalize(name):
    return name.replace('=', '').replace('＝', '').replace(' ', '').replace('　', '')

nen_normalized = {normalize(name): name for name in nen_files}

filtered_chars = []
for c in new_chars:
    norm_c = normalize(c)
    if norm_c in nen_normalized:
        continue
    
    # Also check if it's a subset of an ability
    is_nen = False
    for n in nen_normalized:
        if norm_c in n or n in norm_c:
            # Let's be careful. If n is short, it might over-match.
            if len(n) > 3 and (n in norm_c or norm_c in n):
                is_nen = True
                break
    if is_nen:
        continue

    filtered_chars.append(c)

with open('/Users/yu/Antigravity_workspace/HUNTERHUNTER-FANSITE/private/new_characters_to_add.txt', 'w', encoding='utf-8') as f:
    for c in filtered_chars:
        f.write(c + '\n')

print(f"Filtered out {len(new_chars) - len(filtered_chars)} abilities. Remaining: {len(filtered_chars)}")
