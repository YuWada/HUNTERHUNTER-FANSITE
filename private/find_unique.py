import urllib.request
import urllib.parse
import re
import ssl

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

urls_to_check = [
    "https://w.atwiki.jp/aniwotawiki/pages/32230.html", # Aniwota HxH? Let's check
    "https://w.atwiki.jp/aniwotawiki/pages/13554.html", # Try another
    "https://vap.co.jp/hunterhunter/",
    "https://togashi-ten.com/",
    "https://chara-zokusei.jp/anime/204",
    "https://hunter-stage.jp/",
    "https://j-books.shueisha.co.jp/books/hunter_hunter_phantom.html",
    "https://j-books.shueisha.co.jp/books/hunter_hunter_last.html"
]

for url in urls_to_check:
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        res = urllib.request.urlopen(req, timeout=5, context=ctx)
        html = res.read().decode('utf-8', errors='ignore')
        match = re.search(r'<title>(.*?)</title>', html, re.IGNORECASE)
        print(f"[OK] {match.group(1).strip() if match else 'No Title'} - {url}")
    except Exception as e:
        print(f"[FAIL {e}] - {url}")

def search_yahoo(query):
    url = 'https://search.yahoo.co.jp/search?p=' + urllib.parse.quote(query)
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    try:
        with urllib.request.urlopen(req, context=ctx) as res:
            html = res.read().decode('utf-8')
            links = re.findall(r'href=\"(https?://[^\"]+)\"', html)
            return [l for l in links if 'yahoo' not in l and 'google' not in l][:5]
    except Exception as e:
        return []

print("\nSearch: アニヲタWiki ハンターハンター")
for l in search_yahoo('アニヲタWiki HUNTER×HUNTER'): print(l)

print("\nSearch: HUNTER×HUNTER 考察 ブログ")
for l in search_yahoo('HUNTER×HUNTER 考察 ブログ'): print(l)
