import re

with open('hg_characters.txt', 'r', encoding='utf-8') as f:
    hg_chars = [line.strip() for line in f if line.strip()]

with open('wiki_chars.txt', 'r', encoding='utf-8') as f:
    wiki_chars = [line.strip() for line in f if line.strip()]

all_chars = set()

def clean_name(name):
    # Remove roles or descriptors like "○○の母"
    name = re.sub(r'（.*?）|\(.*?\)', '', name)
    # Remove HTML remnants or extra spaces
    name = re.sub(r'<.*?>', '', name)
    name = name.strip()
    return name

for name in hg_chars + wiki_chars:
    cleaned = clean_name(name)
    # Filter out things that are obviously not character names
    if not cleaned: continue
    if "編" in cleaned and len(cleaned) < 10: continue
    if "一覧" in cleaned: continue
    if "について" in cleaned: continue
    if "の登場人物" in cleaned: continue
    
    # Simple heuristic to avoid long sentences
    if len(cleaned) > 20: continue
    
    all_chars.add(cleaned)

sorted_chars = sorted(list(all_chars))

with open('character_list.txt', 'w', encoding='utf-8') as f:
    for c in sorted_chars:
        f.write(c + '\n')

print(f"Total unique characters: {len(sorted_chars)}")
