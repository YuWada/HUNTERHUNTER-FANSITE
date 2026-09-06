import re

with open('hg_characters.txt', 'r', encoding='utf-8') as f:
    hg_chars = set(line.strip() for line in f if line.strip())

with open('wiki_chars.txt', 'r', encoding='utf-8') as f:
    wiki_chars = set(line.strip() for line in f if line.strip())

# Words that indicate it's probably not a character name
invalid_words = ['の', '能力', '世界', '空間', '時計', '窓', 'その他', '男', '女', '一覧', '人物', '編', '仕事', '状態', '人', '者', '達', '室', '親子', '係']

valid_wiki = set()
for c in wiki_chars:
    c = re.sub(r'（.*?）|\(.*?\)', '', c).strip()
    if not c: continue
    
    # If it's already in HG, it's valid
    if c in hg_chars:
        valid_wiki.add(c)
        continue
    
    # Check invalid words
    if any(w in c for w in invalid_words):
        continue
        
    # Check if it contains mostly hiragana/kanji forming a sentence (rough check)
    if len(c) > 15:
        continue
        
    valid_wiki.add(c)

all_chars = sorted(list(hg_chars | valid_wiki))

with open('character_list.txt', 'w', encoding='utf-8') as f:
    for c in all_chars:
        f.write(c + '\n')

print(f"Total cleaned characters: {len(all_chars)}")
