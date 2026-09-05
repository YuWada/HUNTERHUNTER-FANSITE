import urllib.request
import re
import ssl

urls = [
    "https://huntermix.web.fc2.com/hunter_c.html",
    "https://hunterworld.tokyo/category/hunterassociation/",
    "https://hunterxhunter.fandom.com/",
    "https://ja.wikipedia.org/wiki/HUNTER%C3%97HUNTER%E3%81%AE%E7%99%BB%E5%A0%B4%E4%BA%BA%E7%89%A9",
    "https://dic.pixiv.net/a/HUNTER%C3%97HUNTER",
    "https://dic.nicovideo.jp/a/hunter%C3%97hunter",
    "https://w.atwiki.jp/aniwotawiki/pages/3233.html",
    "https://dic.pixiv.net/a/%E5%BF%B5%E8%83%BD%E5%8A%9B",
    "https://dic.pixiv.net/a/%E3%82%B0%E3%83%AA%E3%83%BC%E3%83%89%E3%82%A2%E3%82%A4%E3%83%A9%E3%83%B3%E3%83%89",
    "https://dic.pixiv.net/a/%E5%A4%A9%E7%A9%BA%E9%97%98%E6%8A%80%E5%A0%B4",
    "https://dic.pixiv.net/a/%E7%8E%8B%E4%BD%8D%E7%B6%99%E6%89%BF%E7%B7%A8",
    "https://ja.wikipedia.org/wiki/%E5%B9%BB%E5%BD%B1%E6%97%85%E5%9B%A3",
    "https://ja.wikipedia.org/wiki/%E3%82%AD%E3%83%A1%E3%83%A9%EF%BC%9D%E3%82%A2%E3%83%B3%E3%83%88",
    "https://ranking.net/rankings/strongest-hunterhunter-characters",
    "https://renote.net/articles/11059",
    "https://dic.pixiv.net/a/%E5%86%A8%E6%A8%AB%E7%BE%A9%E5%8D%9A",
    "https://www.shonenjump.com/j/rensai/hunter.html",
    "https://www.ntv.co.jp/hunterhunter/",
    "https://www.reddit.com/r/HunterXHunter/",
    "https://hiatus-hiatus.github.io/"
]

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

for i, url in enumerate(urls, 1):
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)'})
        res = urllib.request.urlopen(req, timeout=10, context=ctx)
        html = res.read().decode('utf-8', errors='ignore')
        match = re.search(r'<title>(.*?)</title>', html, re.IGNORECASE | re.DOTALL)
        if match:
            print(f"{i}. {match.group(1).strip()}")
        else:
            print(f"{i}. [No Title] {url}")
    except Exception as e:
        print(f"{i}. [ERROR: {e}] {url}")
