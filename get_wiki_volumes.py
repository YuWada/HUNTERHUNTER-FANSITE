import json
import urllib.request
import re
from html.parser import HTMLParser

url = "https://ja.wikipedia.org/wiki/HUNTER%C3%97HUNTER"
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
try:
    with urllib.request.urlopen(req) as response:
        html = response.read().decode('utf-8')
except Exception as e:
    print(f"Error fetching wiki: {e}")
    html = ""

# Look for single tankoubon information
import re
# Regex to find "第N巻" and its chapters
# Actually, since Wikipedia tables can be tricky, let's just make a hardcoded list of end chapters for each volume based on the standard.
# Hunter x Hunter volumes:
# 1: 8
# 2: 17
# 3: 26
# 4: 35
# 5: 44
# 6: 54
# 7: 63
# 8: 73
# 9: 83
# 10: 93
# 11: 103
# 12: 115
# 13: 127
# 14: 137
# ...
