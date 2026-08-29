import os
import time
import requests
import urllib.parse
from bs4 import BeautifulSoup

CHARS = list("あいうえおかきくけこさしすせそたちつてとなにぬねのはひふへほまみむめもやゆよらりるれろわをん")
BASE_DIR = "/Users/yu/Antigravity_workspace/HUNTERHUNTER-FANSITE/private/HUNTER_MOJI"
HEADERS = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}

def search_and_download(char):
    char_dir = os.path.join(BASE_DIR, char)
    os.makedirs(char_dir, exist_ok=True)
    
    query = f"ハンター文字 {char}"
    url = f"https://html.duckduckgo.com/html/?q={urllib.parse.quote(query)}"
    
    try:
        res = requests.get(url, headers=HEADERS)
        soup = BeautifulSoup(res.text, 'html.parser')
        
        images = [img.get('src') for img in soup.find_all('img') if img.get('src')]
        
        count = 0
        for src in images:
            if src.startswith('//'):
                src = 'https:' + src
            elif src.startswith('/'):
                src = 'https://duckduckgo.com' + src
            
            if count >= 3: break
            try:
                img_data = requests.get(src, headers=HEADERS, timeout=5).content
                if len(img_data) > 500:
                    ext = 'jpg'
                    with open(os.path.join(char_dir, f"sample_{count+1}.{ext}"), 'wb') as f:
                        f.write(img_data)
                    count += 1
            except:
                pass
                
        if count == 0:
            with open(os.path.join(char_dir, "info.txt"), "w") as f:
                f.write(f"Could not fetch images automatically for {char}. Please download manually.\n")
                
    except Exception as e:
         print(f"Failed to search for {char}: {e}")
         
for c in CHARS:
    search_and_download(c)
    print(f"Processed {c}")
