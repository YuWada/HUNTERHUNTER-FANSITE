import os
import json
import re

html_file = "hunter_moji_source.html"
out_dir = "MY_CLEAN_IMAGES"
os.makedirs(out_dir, exist_ok=True)

DAKU = {"が":"か","ぎ":"き","ぐ":"く","げ":"け","ご":"こ","ざ":"さ","じ":"し","ず":"す","ぜ":"せ","ぞ":"そ","だ":"た","ぢ":"ち","づ":"つ","で":"て","ど":"と","ば":"は","び":"ひ","ぶ":"ふ","べ":"へ","ぼ":"ほ","ゔ":"う"}
HAND = {"ぱ":"は","ぴ":"ひ","ぷ":"ふ","ぺ":"へ","ぽ":"ほ"}

def generate_svg(char, info, mark=None):
    gold_grad = """<linearGradient id="goldGrad" x1="0" y1="0" x2="136" y2="136" gradientUnits="userSpaceOnUse">
      <stop offset="0%" stop-color="#ffd700" />
      <stop offset="50%" stop-color="#f5deb3" />
      <stop offset="100%" stop-color="#daa520" />
    </linearGradient>"""
    
    def draw_path(d_str):
        if not d_str: return ""
        return f'''
    <path d="{d_str}" fill="none" stroke="#222222" stroke-width="3" stroke-linejoin="miter" stroke-linecap="butt" />
    <path d="{d_str}" fill="url(#goldGrad)" fill-rule="evenodd" />'''

    def draw_stroke_path(d_str):
        return f'''
    <path d="{d_str}" fill="none" stroke="#222222" stroke-width="10" stroke-linecap="square" stroke-linejoin="miter" />
    <path d="{d_str}" fill="none" stroke="url(#goldGrad)" stroke-width="7" stroke-linecap="square" stroke-linejoin="miter" />'''
        
    def draw_fill_circle(cx, cy, r):
        return f'''
    <circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="#222222" stroke-width="3" />
    <circle cx="{cx}" cy="{cy}" r="{r}" fill="url(#goldGrad)" />'''
        
    def draw_stroke_circle(cx, cy, r):
        return f'''
    <circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="#222222" stroke-width="8" />
    <circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="url(#goldGrad)" stroke-width="5" />'''

    elements = []
    
    if "t" in info and info["t"]:
        elements.append(draw_path(info["t"]))
    if "p" in info:
        for p in info["p"]:
            elements.append(draw_stroke_path(p))
    if "c" in info:
        for c in info["c"]:
            elements.append(draw_stroke_circle(c[0], c[1], c[2]))
    if "f" in info:
        for f in info["f"]:
            elements.append(draw_fill_circle(f[0], f[1], f[2]))
            
    if mark == 'd':
        elements.append(draw_fill_circle(87, 87, 8))
    elif mark == 'h':
        elements.append(draw_stroke_circle(87, 87, 8))

    g_content = "\n".join(elements)

    # 以前は width/height=200, translate(40,40) で余白が上下左右に約40pxずつあった
    # その余白の8割(約32px)を削るため、width/height=136, translate(8,8) に変更
    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 136 136" width="136" height="136">
  <defs>
    {gold_grad}
  </defs>
  <g transform="translate(8, 8) scale(1.2)">
    {g_content}
  </g>
</svg>"""

    safe_char = char.replace('/', '_')
    with open(os.path.join(out_dir, f"{safe_char}.svg"), "w") as out_f:
        out_f.write(svg)

with open(html_file, "r") as f:
    content = f.read()

match = re.search(r'var G=(\{.*?\});', content, re.DOTALL)
if match:
    json_str = match.group(1)
    json_str = re.sub(r'([a-zA-Z_]+):', r'"\1":', json_str)
    json_str = re.sub(r',\s*\}', '}', json_str)
    
    try:
        G = json.loads(json_str)
        for char, info in G.items():
            generate_svg(char, info)
        for d_char, base_char in DAKU.items():
            if base_char in G:
                generate_svg(d_char, G[base_char], mark='d')
        for h_char, base_char in HAND.items():
            if base_char in G:
                generate_svg(h_char, G[base_char], mark='h')
        print("Successfully generated SVGs with cropped margins.")
    except Exception as e:
        print(f"Error: {e}")
else:
    print("Could not find G.")
