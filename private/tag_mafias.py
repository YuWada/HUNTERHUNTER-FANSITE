import os
import re

db_dir = "/Users/yu/Antigravity_workspace/HUNTERHUNTER-FANSITE/private/HUNTER_DATA/登場人物"

mafia_members = {
    "エイ＝イ一家": [
        "ヨコタニ", "モレナ＝プルード", "ルイーニー", "トレベルム", "ボコンテ", "ドッグマン", 
        "ジェラート", "カシュー", "ギャトーム", "ペリゴル", "デモン", "デヴェラレス", "クオロール", 
        "パドイユ", "バドイユ", "シフォン＝トト", "モンブラン＝トト", "スフレ", "ノートル", "ビレ", "マトベール", "ソドム"
    ],
    "シュウ＝ウ一家": [
        "オニオール＝ロンポウ", "ヒンリギ＝ビガンダフノ", "ザクロ＝カスタード", "リンチ＝フルボッコ", "タッシ", "ミーシャ＝ハオ"
    ],
    "シャ＝ア一家": [
        "ブロッコ＝リー", "オウ＝ケンイ", "イットク", "ソンビン", "ツンジ", "ツドンケ", "オラルジ"
    ]
}

def update_tags(filepath, family):
    if not os.path.exists(filepath):
        return
        
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()
        
    parts = content.split("---")
    if len(parts) < 3:
        return
        
    frontmatter = parts[1]
    body = "---".join(parts[2:])
    
    # Parse tags
    tags_match = re.search(r"tags:\s*\[(.*?)\]", frontmatter)
    if not tags_match:
        return
        
    tags_str = tags_match.group(1)
    tags = [t.strip().strip("'").strip('"') for t in tags_str.split(",") if t.strip()]
    
    if family not in tags:
        tags.append(family)
        
    if "登場人物" not in tags:
        tags.insert(0, "登場人物")
        
    # Format tags back
    new_tags_str = "['" + "', '".join(tags) + "']"
    new_frontmatter = re.sub(r"tags:\s*\[.*?\]", f"tags: {new_tags_str}", frontmatter)
    
    new_content = f"---{new_frontmatter}---{body}"
    
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(new_content)
    print(f"Updated {filepath} with tag {family}")

for family, members in mafia_members.items():
    for member in members:
        update_tags(os.path.join(db_dir, f"{member}.md"), family)

