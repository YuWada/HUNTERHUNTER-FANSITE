import re

terms = ["ゴン＝フリークス", "キルア＝ゾルディック", "ビスケット＝クルーガー（ビスケ）", "カイト", "ジン＝フリークス"]
aliases = {}

for term in terms:
    aliases[term] = term
    
    m = re.match(r'^(.+)（(.+)）$', term)
    if m:
        base = m.group(1).strip()
        sub = m.group(2).strip()
        if len(base) >= 2 and base not in aliases: aliases[base] = term
        if len(sub) >= 2 and sub not in aliases: aliases[sub] = term
    else:
        base = term
        
    if '＝' in base:
        first = base.split('＝')[0]
        if len(first) >= 2 and first not in aliases:
            aliases[first] = term

for k, v in aliases.items():
    print(f"{k} -> {v}")
