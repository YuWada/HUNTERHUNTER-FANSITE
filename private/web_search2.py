import urllib.request
import urllib.parse
import re
import ssl

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

def search(query):
    try:
        url = 'https://search.yahoo.co.jp/search?p=' + urllib.parse.quote(query + " ハンターハンター")
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        html = urllib.request.urlopen(req, context=ctx).read().decode('utf-8')
        # Just check if there are hits
        if "一致するウェブページは見つかりませんでした" in html: return False
        return True
    except:
        return False

names = ["ギャトーム", "クズコ", "クルト", "グエリモリ", "コウモリ", "コナリー", "コネルト", "コバーン", "コンタスティン", "コービヒ", "ゴーレム", "サキスケ=ンジジ", "サクエーレ"]
for n in names:
    print(f"{n}: {search(n)}")
