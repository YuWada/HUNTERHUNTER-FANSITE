import urllib.request
import urllib.error

urls = {
    "1. Hunterpedia (EN)": "https://hunterxhunter.fandom.com/",
    "7. GI": "https://dic.pixiv.net/a/%E3%82%B0%E3%83%AA%E3%83%BC%E3%83%89%E3%82%A2%E3%82%A4%E3%83%A9%E3%83%B3%E3%83%89",
    "9. Succession": "https://dic.pixiv.net/a/%E7%8E%8B%E4%BD%8D%E7%B6%99%E6%89%BF%E7%B7%A8",
    "10. Quotes": "https://renote.net/articles/27885",
    "11. Strength": "https://renote.net/articles/12204",
    "19. Alibato": "https://gamewith.jp/hunterhunter-arena/"
}

for name, url in urls.items():
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        res = urllib.request.urlopen(req, timeout=5)
        print(f"[OK] {name}: {url}")
    except urllib.error.HTTPError as e:
        print(f"[FAIL {e.code}] {name}: {url}")
    except Exception as e:
        print(f"[FAIL {type(e)}] {name}: {url}")
