import json
import base64
import os
import re

js_file = "hxh_sprites.js"
out_dir = "CLEAN_IMAGES_2"
os.makedirs(out_dir, exist_ok=True)

with open(js_file, "r", encoding="utf-8") as f:
    content = f.read()

match = re.search(r'const SPRITES\s*=\s*(\{.*?\});', content, re.DOTALL)
if match:
    json_str = match.group(1)
    
    # 最後の要素の後にあるカンマを削除
    json_str = re.sub(r',\s*\}', '}', json_str)
    
    try:
        data = json.loads(json_str)
        for char, b64_url in data.items():
            if b64_url.startswith("data:image/png;base64,"):
                b64_data = b64_url.split(",", 1)[1]
                img_data = base64.b64decode(b64_data)
                
                safe_char = char.replace('/', '_')
                with open(os.path.join(out_dir, f"{safe_char}.png"), "wb") as out_f:
                    out_f.write(img_data)
        print("Successfully generated all PNG files from Base64 data.")
    except Exception as e:
        print(f"Error parsing JSON or decoding: {e}")
else:
    print("Could not find SPRITES data in JS.")
