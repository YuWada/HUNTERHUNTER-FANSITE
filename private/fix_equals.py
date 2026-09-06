with open('character_list_resolved.txt', 'r', encoding='utf-8') as f:
    chars = [line.strip() for line in f if line.strip()]

fixed = set()
for c in chars:
    if c.endswith('='):
        c = c[:-1]
    fixed.add(c)

with open('character_list_resolved.txt', 'w', encoding='utf-8') as f:
    for c in sorted(list(fixed)):
        f.write(c + '\n')
