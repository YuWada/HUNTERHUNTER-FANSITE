import urllib.request
import urllib.parse
import re
import ssl
import json

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

def get_summary(query):
    url = 'https://search.yahoo.co.jp/search?p=' + urllib.parse.quote(query + " ハンターハンター")
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    try:
        html = urllib.request.urlopen(req, context=ctx).read().decode('utf-8')
        snippets = re.findall(r'<div class="sw-Card__summary".*?>(.*?)</div>', html, re.IGNORECASE)
        clean = [re.sub('<[^<]+?>', '', s) for s in snippets]
        return clean[:3]
    except Exception as e:
        return str(e)

results = {}
for name in ["バルダー", "ヒシタ", "ヒマンセ", "ビレ", "ピサク", "ファムール", "フミ", "フリチョセフ", "ベンニー=ドロン"]:
    results[name] = get_summary(name)

with open('search_results6.json', 'w') as f:
    json.dump(results, f, ensure_ascii=False, indent=2)
