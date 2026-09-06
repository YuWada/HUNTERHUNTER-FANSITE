import urllib.request
import re
import ssl

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

chars = []
pages = ['a', 'k', 's', 't', 'n', 'h', 'm', 'y', 'r', 'w']
for p in pages:
    url = f"https://huntermix.web.fc2.com/character_{p}.html"
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        html = urllib.request.urlopen(req, context=ctx).read().decode('shift_jis', errors='ignore')
        # names are like <h2><a name="xxx">Name</a></h2>
        matches = re.findall(r'<h2><a name=".*?">(.*?)</a></h2>', html)
        for m in matches:
            name = m.strip()
            name = re.sub(r'（.*?）', '', name) # remove aliases in parens
            if name:
                chars.append(name)
    except Exception as e:
        print(f"Error on {p}: {e}")

with open('mix_chars.txt', 'w', encoding='utf-8') as f:
    for c in list(set(chars)):
        f.write(c + '\n')
print(f"Extracted {len(set(chars))} from HUNTER MIX")
