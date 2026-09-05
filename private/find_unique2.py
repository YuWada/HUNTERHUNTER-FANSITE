import urllib.request
import urllib.parse
import re
import ssl

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

def search_yahoo(query):
    url = 'https://search.yahoo.co.jp/search?p=' + urllib.parse.quote(query)
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    try:
        with urllib.request.urlopen(req, context=ctx) as res:
            html = res.read().decode('utf-8')
            links = re.findall(r'href=\"(https?://[^\"]+)\"', html)
            return [l for l in links if 'yahoo' not in l and 'google' not in l][:2]
    except Exception as e:
        return []

print(search_yahoo('アニメイトタイムズ ハンターハンター 念能力'))
print(search_yahoo('マンガペディア HUNTER×HUNTER'))
print(search_yahoo('リアル脱出ゲーム ハンターハンター'))
print(search_yahoo('ABEMA HUNTER×HUNTER'))
print(search_yahoo('少年ジャンプ＋ HUNTER×HUNTER'))
