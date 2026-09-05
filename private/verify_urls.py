import urllib.request
import urllib.error

urls = {
    "1. Hunterpedia": "https://hunterxhunter.fandom.com/ja/wiki/Hunterpedia",
    "2. Wikipedia": "https://ja.wikipedia.org/wiki/HUNTER%C3%97HUNTER%E3%81%AE%E7%99%BB%E5%A0%B4%E4%BA%BA%E7%89%A9",
    "3. Pixiv": "https://dic.pixiv.net/a/HUNTER%C3%97HUNTER",
    "4. NicoNico": "https://dic.nicovideo.jp/a/hunter%C3%97hunter",
    "5. Aniwota": "https://w.atwiki.jp/aniwotawiki/pages/3233.html",
    "6. Nen Ability": "https://dic.pixiv.net/a/%E5%BF%B5%E8%83%BD%E5%8A%9B",
    "7. GI Cards": "https://dic.pixiv.net/a/%E6%8C%87%E5%AE%9A%E3%83%9D%E3%82%B1%E3%83%83%E3%83%88%E3%82%AB%E3%83%BC%E3%83%89",
    "8. Heavens Arena": "https://dic.pixiv.net/a/%E5%A4%A9%E7%A9%BA%E9%97%98%E6%8A%80%E5%A0%B4",
    "9. Succession War": "https://dic.pixiv.net/a/%E7%8E%8B%E4%BD%8D%E7%B6%99%E6%89%BF%E6%88%A6",
    "10. Quotes 1": "https://meigenkakugen.net/hunterhunter/",
    "10. Quotes 2": "https://ranking.net/rankings/best-hunterxhunter-quotes",
    "11. Strength Ranking 1": "https://ranking.net/rankings/strongest-hunterxhunter-characters",
    "11. Strength Ranking 2": "https://macaron.club/hunter-hunter-strength-ranking/",
    "12. Author": "https://dic.pixiv.net/a/%E5%86%A8%E6%A8%AB%E7%BE%A9%E5%8D%9A",
    "13. Mysteries": "https://renote.net/articles/11059",
    "14. Shonen Jump": "https://www.shonenjump.com/j/rensai/hunter.html",
    "15. NTV Anime": "https://www.ntv.co.jp/hunterhunter/",
    "16. Reddit": "https://www.reddit.com/r/HunterXHunter/",
    "17. Hiatus List": "https://hiatus-hiatus.github.io/",
    "18. Stage Play": "https://hunter-stage.jp/",
    "19. GameWiki": "https://kamigame.jp/hunter-arena/",
    "20. Chara-zokusei": "https://chara-zokusei.jp/anime/204"
}

for name, url in urls.items():
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'})
        res = urllib.request.urlopen(req, timeout=5)
        print(f"[OK] {name}: {url}")
    except urllib.error.HTTPError as e:
        if e.code in [403, 401]:
            print(f"[OK (Protected)] {name}: {url}")
        else:
            print(f"[FAIL {e.code}] {name}: {url}")
    except Exception as e:
        print(f"[FAIL {type(e)}] {name}: {url}")
