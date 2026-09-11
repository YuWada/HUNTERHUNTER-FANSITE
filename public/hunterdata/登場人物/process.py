import os
import glob
import re
import sys

files = [
    "200階クラスの案内係.md", "503号室の住人、ミハエル、店員.md", "アイザック＝ネテロ.md", "アゴン.md", 
    "アスタ.md", "アッサム.md", "アニタ.md", "アネスト.md", "アベンガネ.md", "アマナ.md", 
    "アマネ.md", "アモリ.md", "アモリ、ウモリ、イモリ.md", "アルカ＝ゾルディック.md", "アーカ.md", 
    "イカルゴ.md", "イサク.md", "イズナビ.md", "イックションペ＝カットゥーヂャ.md", "イットク.md", 
    "イベンコフ.md", "イモリ.md", "イラルディア.md", "イルミ＝ゾルディック.md", "イワレンコフ.md", 
    "イータ.md", "ウイング.md", "ウェルゲー.md", "ウェルフィン.md", "ウサメーン.md", 
    "ウショウヒ.md", "ウッディー、変死した4人.md", "ウボォーギン.md", "ウマンマ.md", "ウモリ.md", 
    "ウンマ.md", "ウンマ王妃所属兵11名.md"
]

base_dir = "/Users/yu/Antigravity_workspace/HUNTERHUNTER-FANSITE/private/HUNTER_DATA/登場人物/"

for f in files:
    path = os.path.join(base_dir, f)
    if os.path.exists(path):
        with open(path, "r") as file:
            content = file.read()
        
        # print title and tags and a bit of content
        print(f"FILE: {f}")
        match = re.search(r'tags:\s*\[(.*?)\]', content)
        if match:
            print(f"TAGS: {match.group(1)}")
        else:
            print("TAGS: NOT FOUND")
        print(f"CONTENT: {content[:200].replace(chr(10), ' ')}")
        print("-" * 40)
