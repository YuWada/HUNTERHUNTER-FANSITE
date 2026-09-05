import urllib.request
import urllib.parse
import re

def search(query):
    url = f"https://html.duckduckgo.com/html/?q={urllib.parse.quote(query)}"
    req = urllib.request.Request(
        url, 
        headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
    )
    try:
        with urllib.request.urlopen(req) as response:
            html = response.read().decode('utf-8')
            # Extract links with class result__url or result__a
            links = re.findall(r'class="result__url" href="([^"]+)"', html)
            if not links:
                links = re.findall(r'class="result__a" href="([^"]+)"', html)
            
            # Unescape DDG redirect URLs
            real_links = []
            for l in links:
                if l.startswith('//duckduckgo.com/l/?uddg='):
                    real_link = urllib.parse.unquote(l.split('uddg=')[1].split('&')[0])
                    real_links.append(real_link)
                else:
                    real_links.append(l)
            return real_links[:3]
    except Exception as e:
        return [str(e)]

queries = [
    "Hunterpedia Fandom",
    "HUNTER×HUNTER 念能力 まとめ サイト",
    "HUNTER×HUNTER ピクシブ百科事典",
    "HUNTER×HUNTER アニヲタWiki"
]

for q in queries:
    print(f"--- {q} ---")
    for link in search(q):
        print(link)
