from bs4 import BeautifulSoup
import re

with open('hg.html', 'r', encoding='utf-8') as f:
    soup = BeautifulSoup(f, 'html.parser')

characters = []
for tr in soup.find_all('tr'):
    tds = tr.find_all('td')
    if len(tds) >= 2:
        name_td = tds[1]
        a_tag = name_td.find('a')
        if a_tag:
            # If there's an A tag, the name is mostly inside it or mixed.
            # E.g. <a href="...">アイザック=<br>ネテロ</a>
            name = a_tag.get_text(strip=True)
            if not name: continue
            characters.append(name)
        else:
            # Maybe text directly? E.g. アベンガネ
            name = name_td.contents[0]
            if isinstance(name, str):
                name = name.strip()
                if name: characters.append(name)

# Remove things that are not characters or duplicates
res = []
for c in characters:
    c = c.replace('\n', '').replace('\r', '')
    if c and c not in res:
        res.append(c)

with open('hg_characters.txt', 'w', encoding='utf-8') as f:
    for c in res:
        f.write(c + '\n')

print(f"Extracted {len(res)} characters from HG.")
