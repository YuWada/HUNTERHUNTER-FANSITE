import re

with open('character_list.txt', 'r', encoding='utf-8') as f:
    chars = [line.strip() for line in f if line.strip()]

# Find formal names (longest names)
# First, group by first names if they contain "="
formal_dict = {}
for c in chars:
    if '=' in c:
        parts = c.split('=')
        first = parts[0]
        last = parts[-1]
        formal_dict[first] = c
        formal_dict[last] = c

resolved_chars = set()
merges = []

for c in chars:
    # Try to find if this character is a part of a formal name
    merged = False
    
    if '=' not in c:
        # Check if it matches any first name or last name exactly
        if c in formal_dict:
            formal_name = formal_dict[c]
            if c != formal_name:
                merges.append(f"{c} -> {formal_name}")
                resolved_chars.add(formal_name)
                merged = True
        else:
            # Maybe it's a prefix of a formal name
            # Example: "ネテロ" -> "アイザック=ネテロ"
            for first, formal in formal_dict.items():
                if c == formal.split('=')[-1]: # Last name match
                    merges.append(f"{c} -> {formal}")
                    resolved_chars.add(formal)
                    merged = True
                    break
    if not merged:
        resolved_chars.add(c)

# Remove substrings (e.g. if 'キルア' and 'キルア=ゾルディック' are both in resolved_chars somehow)
final_chars = list(resolved_chars)
to_remove = set()
for i, c1 in enumerate(final_chars):
    for j, c2 in enumerate(final_chars):
        if i != j:
            # If c1 is exactly the first part of c2 when split by =
            if '=' in c2:
                parts = c2.split('=')
                if c1 == parts[0] or c1 == parts[-1]:
                    to_remove.add(c1)
                    merges.append(f"{c1} -> {c2}")

final_chars = sorted(list(set(final_chars) - to_remove))

with open('character_list_resolved.txt', 'w', encoding='utf-8') as f:
    for c in final_chars:
        f.write(c + '\n')

with open('nayose_log.txt', 'w', encoding='utf-8') as f:
    for m in sorted(list(set(merges))):
        f.write(m + '\n')

print(f"Original: {len(chars)}, Resolved: {len(final_chars)}")
print(f"Merges recorded in nayose_log.txt")
