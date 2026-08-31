import os
import re

tag_map = {
    'backlog': '要確認',
    'beyond_faction': 'ビヨンド一派',
    'calamity': '五大厄災',
    'cha_r': 'シャア＝ア一家',
    'character': '登場人物',
    'chimera_ant': 'キメラ＝アント',
    'dark_continent': '暗黒大陸',
    'deep_scraped': '深堀り設定', 
    'gi_card': 'G.I.カード',
    'glossary': '用語',
    'greed_island': 'グリードアイランド',
    'heavens_arena': '天空闘技場',
    'hunter': 'ハンター',
    'hunter x hunter': 'HUNTER×HUNTER',
    'hunter_exam': 'ハンター試験',
    'hunter_rank': 'ハンター階級',
    'index': '目次',
    'injyu': '陰獣',
    'kakin': 'カキン帝国',
    'kakin_mafia': 'カキンマフィア',
    'kurta': 'クルタ族',
    'list': '一覧',
    'mafia': 'マフィア',
    'magical_beast': '魔獣',
    'main': 'メインキャラクター',
    'nen': '念',
    'nen_ability': '念能力',
    'nenability': '念能力',
    'nostrade': 'ノストラード組',
    'organization': '組織・勢力',
    'phantom_troupe': '幻影旅団',
    'story': 'ストーリー',
    'term': '用語',
    'terms': '用語',
    'world_setting': '世界観',
    'world_tree': '世界樹',
    'zodiac': '十二支ん',
    'zoldyck': 'ゾルディック家'
}

def translate_tags(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    def replace_tags(match):
        tags_str = match.group(1)
        # Parse tags
        tags = [t.strip(" '\"") for t in tags_str.split(',')]
        new_tags = []
        for t in tags:
            if not t:
                continue
            if t in tag_map:
                new_tags.append(tag_map[t])
            else:
                new_tags.append(t)
        
        # Format tags back (deduplicate, preserve order roughly)
        seen = set()
        unique_tags = []
        for t in new_tags:
            if t not in seen:
                seen.add(t)
                unique_tags.append(t)
        
        # Build replacement string
        tags_list_str = ", ".join(f"'{t}'" for t in unique_tags)
        return f"tags: [{tags_list_str}]"

    new_content = re.sub(r'tags:\s*\[(.*?)\]', replace_tags, content)

    if new_content != content:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        return True
    return False

changed = 0
for root, _, files in os.walk('.'):
    for file in files:
        if file.endswith('.md'):
            if translate_tags(os.path.join(root, file)):
                changed += 1

print(f"Updated tags in {changed} files.")
