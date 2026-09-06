import re

with open('character_list.txt', 'r', encoding='utf-8') as f:
    chars = [line.strip() for line in f if line.strip()]

clean = set()
for c in chars:
    # Remove wiki references like [注 37]
    c = re.sub(r'\[.*?\]', '', c)
    # Remove HTML if any
    c = re.sub(r'<.*?>', '', c)
    c = c.strip()
    
    # Filter rules
    if not c: continue
    if 'マンション' in c: continue
    if '僕等' in c: continue
    if '兵' in c and len(c) > 5: continue # like カミーラ私設兵, ウンマ王妃所属兵11名
    if '兄弟' in c: continue
    if '、' in c: continue # アモリ、ウモリ、イモリ
    
    # standardize equal sign
    c = c.replace('＝', '=')
    
    clean.add(c)

with open('character_list.txt', 'w', encoding='utf-8') as f:
    for c in sorted(list(clean)):
        f.write(c + '\n')

print(f"Final cleaned count: {len(clean)}")
