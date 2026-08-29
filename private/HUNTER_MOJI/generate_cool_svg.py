import os
import glob
import xml.etree.ElementTree as ET

source_dir = "CLEAN_IMAGES"
out_dir = "MY_CLEAN_IMAGES"

def create_cool_svg(char, in_path, out_path):
    if not os.path.exists(in_path):
        return
        
    tree = ET.parse(in_path)
    root = tree.getroot()
    
    path_d = ""
    for elem in root.iter():
        if 'path' in elem.tag:
            path_d = elem.get('d')
            break
            
    if not path_d:
        return

    # 透過背景、細くてシャープな縁取り、影なし
    cool_svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 200 200" width="200" height="200">
  <defs>
    <!-- Text Gold Gradient -->
    <linearGradient id="goldGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#ffd700" />
      <stop offset="50%" stop-color="#f5deb3" />
      <stop offset="100%" stop-color="#daa520" />
    </linearGradient>
  </defs>

  <!-- Scaled and centered Hunter Character Path -->
  <g transform="translate(40, 40) scale(1.2)">
    <!-- Sharp Outline (Stroke) -->
    <path d="{path_d}" fill="none" stroke="#222222" stroke-width="3" stroke-linejoin="miter" stroke-linecap="butt" />
    
    <!-- Inner Fill (Gold) -->
    <path d="{path_d}" fill="url(#goldGrad)" />
  </g>
</svg>"""

    with open(out_path, "w") as f:
        f.write(cool_svg)

# CLEAN_IMAGES フォルダ内のすべてのSVGファイルを処理
count = 0
for in_file in glob.glob(os.path.join(source_dir, "*.svg")):
    basename = os.path.basename(in_file)
    char = os.path.splitext(basename)[0]
    out_file = os.path.join(out_dir, basename)
    
    create_cool_svg(char, in_file, out_file)
    count += 1

print(f"Successfully generated all {count} sharp outline SVGs.")
