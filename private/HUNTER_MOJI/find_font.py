import urllib.request
from bs4 import BeautifulSoup
import re

url = "https://intwosick.com/hunter-moji/"
req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
html = urllib.request.urlopen(req).read()
soup = BeautifulSoup(html, "html.parser")

for style in soup.find_all("style"):
    if "font-face" in style.text or "hunter" in style.text.lower():
        urls = re.findall(r"url\((.*?)\)", style.text)
        for u in urls:
            u_clean = u.strip("\"'")
            if "hunter" in u_clean.lower() or "woff" in u_clean.lower() or "ttf" in u_clean.lower():
                print(u_clean)
