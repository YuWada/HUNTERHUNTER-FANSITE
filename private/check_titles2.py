import urllib.request
import re

urls = [
    "https://w.atwiki.jp/aniwotawiki/pages/10395.html",
    "https://hunterhunter-kousatsu.hatenablog.com/"
]

for url in urls:
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        res = urllib.request.urlopen(req, timeout=5)
        html = res.read().decode('utf-8', errors='ignore')
        match = re.search(r'<title>(.*?)</title>', html, re.IGNORECASE)
        print(f"[OK] {match.group(1).strip() if match else 'No Title'} - {url}")
    except Exception as e:
        print(f"[FAIL {e}] - {url}")
