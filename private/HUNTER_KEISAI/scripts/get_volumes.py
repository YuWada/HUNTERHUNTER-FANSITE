import urllib.request
import re
from html.parser import HTMLParser

url = "https://ja.wikipedia.org/wiki/HUNTER%C3%97HUNTER%E3%81%AE%E3%82%A8%E3%83%94%E3%82%BD%E3%83%BC%E3%83%89%E4%B8%80%E8%A6%A7"
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
try:
    with urllib.request.urlopen(req) as response:
        html = response.read().decode('utf-8')
    print("Success")
except urllib.error.HTTPError as e:
    print(f"HTTPError: {e.code}")
except Exception as e:
    print(f"Error: {e}")

