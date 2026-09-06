with open('character_list_resolved.txt', 'r', encoding='utf-8') as f:
    chars = [line.strip() for line in f if line.strip()]

invalid = ["七色弓箭", "不思議で便利な大風呂敷", "九十九乃掌", "予知夢", "二刀流", "体は全部知っている", "体毛針", "偽試験官", "能力", "分身", "手裏剣", "魔獣", "暗殺", "放出系", "強化系", "変化系", "操作系", "具現化系", "特質系", "武器", "必殺技", "技"]

new_chars = []
for c in chars:
    c = c.replace('　※', '').replace(' ※', '')
    if any(i in c for i in invalid): continue
    if "曹長" in c: c = c.replace("曹長", "")
    if "伍長" in c: c = c.replace("伍長", "")
    if "神父" in c: c = c.replace("神父", "")
    new_chars.append(c.strip())

with open('db_character_candidates.txt', 'w', encoding='utf-8') as f:
    for c in sorted(list(set(new_chars))):
        f.write(c + '\n')
