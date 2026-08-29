import os
import cv2
import numpy as np
from PIL import Image

chart_path = "CLEAN_IMAGES_3/hunter_alphabet_chart.gif"
out_dir = "CLEAN_IMAGES_3"

# GIFを読み込んでPIL経由で変換
gif = Image.open(chart_path)
gif = gif.convert("RGB")
img = np.array(gif)

# グレースケールに変換
gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
# 2値化
_, thresh = cv2.threshold(gray, 200, 255, cv2.THRESH_BINARY_INV)

# 文字の輪郭を見つける
contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

count = 1
for cnt in contours:
    x, y, w, h = cv2.boundingRect(cnt)
    
    # 小さすぎるノイズなどは無視
    if w > 15 and h > 15:
        # 少し余裕を持たせてクロップ
        pad = 5
        x1 = max(0, x - pad)
        y1 = max(0, y - pad)
        x2 = min(img.shape[1], x + w + pad)
        y2 = min(img.shape[0], y + h + pad)
        
        char_img = img[y1:y2, x1:x2]
        cv2.imwrite(os.path.join(out_dir, f"char_{count:03d}.png"), cv2.cvtColor(char_img, cv2.COLOR_RGB2BGR))
        count += 1

print(f"Extracted {count-1} character images.")
