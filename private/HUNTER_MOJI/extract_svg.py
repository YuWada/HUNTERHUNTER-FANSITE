import re
import json
import os

html_file = "hunter_moji_source.html"
out_dir = "CLEAN_IMAGES"
os.makedirs(out_dir, exist_ok=True)

with open(html_file, "r") as f:
    content = f.read()

# var G={ ... }; の部分を抽出
match = re.search(r'var G=(\{.*?\});', content, re.DOTALL)
if match:
    json_str = match.group(1)
    # JSONとしてパースできるようにキーやクォートを整形
    json_str = re.sub(r'([a-zA-Z0-9_]+):', r'"\1":', json_str)
    # 最後のカンマを削除
    json_str = re.sub(r',\s*\}', '}', json_str)
    # 文字列がシングルクォートで囲まれている場合に対応（このサイトはダブルクォートだった）
    try:
        data = json.loads(json_str)
        for char, info in data.items():
            path_d = info.get("t", "")
            if path_d:
                # SVGファイル生成
                svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100" width="100" height="100">
  <path d="{path_d}" fill="#000000" />
</svg>'''
                # Mac/Linuxファイル名に使えない文字のスラッシュなどはエスケープ（ハンター文字には基本ないが）
                safe_char = char.replace('/', '_')
                with open(os.path.join(out_dir, f"{safe_char}.svg"), "w") as out_f:
                    out_f.write(svg)
        print("Successfully generated all SVG files from path data.")
    except Exception as e:
        print(f"Error parsing JSON: {e}")
else:
    print("Could not find the path data in HTML.")
