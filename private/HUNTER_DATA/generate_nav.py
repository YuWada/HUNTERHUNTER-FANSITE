import os
import yaml

base_dir = "build_src/docs"
order = ["ストーリー", "登場人物", "念能力", "グリードアイランド_カード", "用語集"]

story_order = [
    "ハンター試験編.md",
    "ゾルディック家編.md",
    "天空闘技場編.md",
    "ヨークシンシティ編.md",
    "グリードアイランド編.md",
    "キメラ＝アント編.md",
    "会長選挙・アルカ編.md",
    "暗黒大陸・王位継承編.md"
]

nav = []
nav.append({"神眼DBホーム": "index.md"})

for section in order:
    section_dir = os.path.join(base_dir, section)
    if os.path.isdir(section_dir):
        section_files = []
        if os.path.exists(os.path.join(section_dir, "index.md")):
            section_files.append({"ホーム": f"{section}/index.md"})
            
        if section == "ストーリー":
            for file in story_order:
                if os.path.exists(os.path.join(section_dir, file)):
                    title = file[:-3]
                    rel_path = f"{section}/{file}"
                    section_files.append({title: rel_path})
        else:
            for root, dirs, files in os.walk(section_dir):
                for file in sorted(files):
                    if file.endswith(".md") and file != "index.md":
                        title = file[:-3]
                        rel_path = os.path.relpath(os.path.join(root, file), base_dir)
                        section_files.append({title: rel_path})
        
        display_name = section
        if display_name == "グリードアイランド_カード":
            display_name = "G.I.カード"
            
        nav.append({display_name: section_files})

with open("build_src/mkdocs.yml", "r", encoding="utf-8") as f:
    config = yaml.safe_load(f)

config["nav"] = nav

with open("build_src/mkdocs.yml", "w", encoding="utf-8") as f:
    yaml.dump(config, f, allow_unicode=True, sort_keys=False)
