import urllib.request
import urllib.parse
import re
import ssl

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

def search_yahoo(query):
    url = 'https://search.yahoo.co.jp/search?p=' + urllib.parse.quote(query + " ハンターハンター")
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    try:
        html = urllib.request.urlopen(req, context=ctx).read().decode('utf-8')
        links = re.findall(r'<div class="sw-Card__title".*?>(.*?)</div>', html, re.IGNORECASE)
        # Just grab text snippets
        snippets = re.findall(r'<div class="sw-Card__summary".*?>(.*?)</div>', html, re.IGNORECASE)
        return links[:2], snippets[:2]
    except Exception as e:
        return str(e)

print("ウォン=ポー:", search_yahoo("ウォン=ポー"))
print("ウォン=リー:", search_yahoo("ウォン=リー"))
print("ウォーリオ=ベイ:", search_yahoo("ウォーリオ=ベイ"))
