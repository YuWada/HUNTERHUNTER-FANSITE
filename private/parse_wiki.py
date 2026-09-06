from bs4 import BeautifulSoup
import urllib.request
import re

url = "https://ja.wikipedia.org/wiki/HUNTER%C3%97HUNTER%E3%81%AE%E7%99%BB%E5%A0%B4%E4%BA%BA%E7%89%A9"
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
html = urllib.request.urlopen(req).read()

soup = BeautifulSoup(html, 'html.parser')
chars = []

# Characters are often in dt
for dt in soup.find_all('dt'):
    name = dt.get_text(strip=True)
    # Remove references like [1], (CV: xxx)
    name = re.sub(r'\[\d+\]', '', name)
    name = re.sub(r'（.*?）', '', name)
    name = re.sub(r'\(.*?\)', '', name)
    name = name.split(' / ')[0] # Handle alias like Name / Alias
    if name and len(name) < 30: # reasonable length
        chars.append(name)

# Sometimes in h3/h4
for hx in soup.find_all(['h3', 'h4']):
    headline = hx.find('span', class_='mw-headline')
    if headline:
        name = headline.get_text(strip=True)
        name = re.sub(r'\[\d+\]', '', name)
        name = re.sub(r'（.*?）', '', name)
        name = re.sub(r'\(.*?\)', '', name)
        if name and len(name) < 20:
            chars.append(name)

with open('wiki_chars.txt', 'w', encoding='utf-8') as f:
    for c in list(set(chars)):
        f.write(c + '\n')

print(f"Found {len(set(chars))} characters on Wikipedia.")
