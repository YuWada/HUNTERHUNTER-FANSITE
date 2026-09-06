import os
import re

directory = "/Users/yu/Antigravity_workspace/HUNTERHUNTER-FANSITE/private/HUNTER_DATA/登場人物/"
files_to_process = [
    "モズベ.md", "モタリケ.md", "モモゼ＝ホイコーロ.md", "モラウ＝マッカーナーシ.md", 
    "モレナ＝プルード.md", "モンタ＝ユーラス.md", "モントゥトゥユピー.md", "モントール.md", 
    "ヤビビ.md", "ユウリ.md", "ユヒライ.md", "ユンジュ.md", "ヨコタニ.md", "ライス.md", 
    "ライト＝ノストラード.md", "ラジオラス.md", "ラターザ.md", "ラモット.md", "ラロック.md", 
    "リサムセッタ.md", "リスト.md", "リスノース.md", "リゾル神父.md", "リッポー.md", 
    "リハン.md", "リュウ.md", "リョウジ.md", "リンセン.md", "リンチ＝フルボッコ.md", 
    "リンネ＝オードブル.md", "リン＝コウシ.md", "リールベルト.md", "ルイーニー.md", 
    "ルズールス＝ホイコーロ.md", "ルーペ＝ハイランド.md", "レイザー.md", 
    "レオリオ＝パラディナイト.md", "レオル.md"
]

tags_map = {
    "モズベ.md": ["暗黒大陸・王位継承編"],
    "モタリケ.md": ["グリードアイランド編"],
    "モモゼ＝ホイコーロ.md": ["暗黒大陸・王位継承編"],
    "モラウ＝マッカーナーシ.md": ["プロハンター", "キメラ＝アント編", "会長選挙・アルカ編", "暗黒大陸・王位継承編"],
    "モレナ＝プルード.md": ["暗黒大陸・王位継承編"],
    "モンタ＝ユーラス.md": ["キメラ＝アント編"],
    "モントゥトゥユピー.md": ["キメラ＝アント", "キメラ＝アント編"],
    "モントール.md": ["暗黒大陸・王位継承編"],
    "ヤビビ.md": ["暗黒大陸・王位継承編"],
    "ユウリ.md": ["暗黒大陸・王位継承編"],
    "ユヒライ.md": ["暗黒大陸・王位継承編"],
    "ユンジュ.md": ["キメラ＝アント", "キメラ＝アント編"],
    "ヨコタニ.md": ["暗黒大陸・王位継承編"],
    "ライス.md": ["暗黒大陸・王位継承編"],
    "ライト＝ノストラード.md": ["ヨークシンシティ編"],
    "ラジオラス.md": ["グリードアイランド編"],
    "ラターザ.md": ["グリードアイランド編"],
    "ラモット.md": ["キメラ＝アント", "キメラ＝アント編"],
    "ラロック.md": ["暗黒大陸・王位継承編"],
    "リサムセッタ.md": ["暗黒大陸・王位継承編"],
    "リスト.md": ["グリードアイランド編"],
    "リスノース.md": ["暗黒大陸・王位継承編"],
    "リゾル神父.md": ["クラピカ追憶編"],
    "リッポー.md": ["プロハンター", "ハンター試験編"],
    "リハン.md": ["暗黒大陸・王位継承編"],
    "リュウ.md": ["暗黒大陸・王位継承編"],
    "リョウジ.md": ["暗黒大陸・王位継承編"],
    "リンセン.md": ["プロハンター", "会長選挙・アルカ編"],
    "リンチ＝フルボッコ.md": ["暗黒大陸・王位継承編"],
    "リンネ＝オードブル.md": ["プロハンター", "会長選挙・アルカ編"],
    "リン＝コウシ.md": ["暗黒大陸・王位継承編"],
    "リールベルト.md": ["天空闘技場編"],
    "ルイーニー.md": ["暗黒大陸・王位継承編"],
    "ルズールス＝ホイコーロ.md": ["暗黒大陸・王位継承編"],
    "ルーペ＝ハイランド.md": ["プロハンター", "会長選挙・アルカ編"],
    "レイザー.md": ["グリードアイランド編"],
    "レオリオ＝パラディナイト.md": ["プロハンター", "ハンター試験編", "ゾルディック家編", "ヨークシンシティ編", "会長選挙・アルカ編", "暗黒大陸・王位継承編"],
    "レオル.md": ["キメラ＝アント", "キメラ＝アント編"],
}

for filename in files_to_process:
    filepath = os.path.join(directory, filename)
    if not os.path.exists(filepath):
        print(f"File not found: {filename}")
        continue
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()
    
    # Read old tags
    old_tags = []
    match = re.search(r'^tags:\s*\[(.*?)\]', content, re.MULTILINE)
    if match:
        old_tags_str = match.group(1)
        old_tags = [t.strip().strip("'").strip('"') for t in old_tags_str.split(",") if t.strip()]
        
    allowed_groups = {"幻影旅団", "ゾルディック家", "キメラ＝アント", "十二支ん", "プロハンター"}
    new_groups = [t for t in old_tags if t in allowed_groups]
    
    target_tags = tags_map.get(filename, [])
    
    final_tags = set(new_groups + target_tags)
    # Ensure they are uniquely represented and formatted as list
    final_tags_list = sorted(list(final_tags))
    
    tags_str = "[" + ", ".join(final_tags_list) + "]"
    
    if match:
        new_content = content[:match.start(0)] + f"tags: {tags_str}" + content[match.end(0):]
    else:
        new_content = content
        print(f"Warning: No tags field found in {filename}")
        
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(new_content)
        
print("Finished processing files.")
