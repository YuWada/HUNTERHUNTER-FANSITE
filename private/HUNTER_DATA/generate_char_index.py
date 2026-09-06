import os
import re
import yaml
from datetime import datetime, timezone

def main():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    char_dir = os.path.join(base_dir, "登場人物")
    
    char_files = []
    for f in os.listdir(char_dir):
        if f.endswith(".md") and f != "index.md":
            char_files.append(f)
            
    char_files.sort()
    
    # タイムスタンプを取得してフロントマターに入れる
    now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    
    lines = [
        "---",
        "title: 登場人物一覧",
        f"timestamp: {now}",
        "---",
        "# 登場人物一覧",
        ""
    ]
    
    for f in char_files:
        path = os.path.join(char_dir, f)
        name = f[:-3]
        
        with open(path, "r", encoding="utf-8") as file:
            content = file.read()
            
        tags = []
        match = re.search(r'^---\n(.*?)\n---', content, re.DOTALL)
        if match:
            yaml_content = match.group(1)
            try:
                data = yaml.safe_load(yaml_content)
                if data and "tags" in data:
                    tags = data["tags"]
            except Exception as e:
                print(f"Error parsing YAML in {f}: {e}")
                
        # タグの表記
        tag_str = ""
        if tags:
            # 「登場人物」タグは一覧では自明なので除外する
            display_tags = [t for t in tags if t != "登場人物"]
            if display_tags:
                # バッジ風にするために spanタグ とクラスを付与
                # <span class="tag-badge">タグ</span> のような形式
                badges = [f'<span class="tag-badge" style="display:inline-block; margin-left:8px; padding:2px 6px; font-size:0.8em; background-color:#f0f0f0; color:#666; border-radius:4px; border:1px solid #ddd;">{t}</span>' for t in display_tags]
                tag_str = "".join(badges)
                
        lines.append(f"* [{name}](./{f}){tag_str}")
        
    with open(os.path.join(char_dir, "index.md"), "w", encoding="utf-8") as file:
        file.write("\n".join(lines) + "\n")
        
    print(f"登場人物一覧 (index.md) を生成しました。 (計 {len(char_files)} 人)")

if __name__ == "__main__":
    main()
