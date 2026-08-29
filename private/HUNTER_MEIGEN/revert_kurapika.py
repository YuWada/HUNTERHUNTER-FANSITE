import re

md_path = "/Users/yu/Antigravity_workspace/HUNTERHUNTER-FANSITE/private/HUNTER_MEIGEN/俺でなきゃ見逃しちゃう名台詞集.md"

with open(md_path, "r", encoding="utf-8") as f:
    content = f.read()

quotes = []
pre_table = []
in_table = False
for line in content.split('\n'):
    line_s = line.strip()
    if line_s.startswith('| セリフ'):
        in_table = True
        continue
    if line_s.startswith('| ---'):
        continue
    
    if in_table and line_s.startswith('|'):
        cols = [c.strip() for c in line_s.split('|')[1:-1]]
        if len(cols) >= 5:
            # Filter out the specific quote
            if "円を解こう" in cols[0] and "バビマイナ" in cols[2]:
                continue
                
            character = cols[2]
            rating = cols[3]
            
            # Revert Kurapika +1 star
            if 'クラピカ' in character:
                star_count = rating.count('★')
                if star_count > 1:
                    star_count -= 1
                rating = ('★' * star_count) + ('☆' * (5 - star_count))
                
            quotes.append({
                'quote': cols[0],
                'volume': cols[1],
                'character': character,
                'rating': rating,
                'meaning': cols[4]
            })
    elif not in_table:
        pre_table.append(line)

# Sort by volume just in case
def extract_vol(vol_str):
    m = re.search(r'\d+', vol_str)
    return int(m.group()) if m else 9999

quotes.sort(key=lambda x: extract_vol(x['volume']))

md_out = "\n".join(pre_table) + "\n"
if not md_out.endswith('\n\n'):
    md_out += "\n"
md_out += "| セリフ | 登場巻・話数 | 発言者 | 電脳有名度 | 意味 |\n"
md_out += "| --- | --- | --- | --- | --- |\n"
for q in quotes:
    md_out += f"| {q['quote']} | {q['volume']} | {q['character']} | {q['rating']} | {q['meaning']} |\n"

with open(md_path, "w", encoding="utf-8") as f:
    f.write(md_out)
