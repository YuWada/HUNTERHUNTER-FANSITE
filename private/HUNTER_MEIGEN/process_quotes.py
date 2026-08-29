import re
import os

md_path = "/Users/yu/Antigravity_workspace/HUNTERHUNTER-FANSITE/private/HUNTER_MEIGEN/俺でなきゃ見逃しちゃう名台詞集.md"
html_path = "/Users/yu/Antigravity_workspace/HUNTERHUNTER-FANSITE/public/huntermeigen/index.html"

with open(md_path, "r", encoding="utf-8") as f:
    content = f.read()

quotes = []
pre_table = []
in_table = False
for line in content.split('\n'):
    line_s = line.strip()
    if line_s.startswith('| セリフ'):
        in_table = True
        continue
    if line_s.startswith('| ---'):
        continue
    
    if in_table and line_s.startswith('|'):
        cols = [c.strip() for c in line_s.split('|')[1:-1]]
        if len(cols) >= 5:
            quotes.append({
                'quote': cols[0],
                'volume': cols[1],
                'character': cols[2],
                'rating': cols[3],
                'meaning': cols[4]
            })
    elif not in_table:
        pre_table.append(line)

# Deduplication logic
def normalize_quote(q):
    s = re.sub(r'[\s　…「」。！？、,\'"♥♠♣♦♡♤♧♢！]', '', q)
    return s

seen = {}
deduped_quotes = []
dup_count = 0
for q in quotes:
    norm = normalize_quote(q['quote'])
    if norm not in seen:
        seen[norm] = True
        deduped_quotes.append(q)
    else:
        print(f"Removed duplicate: {q['quote']}")
        dup_count += 1

quotes = deduped_quotes
if dup_count > 0:
    print(f"Total duplicates removed: {dup_count}")

# Sort by volume
def extract_vol(vol_str):
    m = re.search(r'\d+', vol_str)
    return int(m.group()) if m else 9999

quotes.sort(key=lambda x: extract_vol(x['volume']))

# Rewrite MD
md_out = "\n".join(pre_table) + "\n"
if not md_out.endswith('\n\n'):
    md_out += "\n"
md_out += "| セリフ | 登場巻・話数 | 発言者 | 電脳有名度 | 意味 |\n"
md_out += "| --- | --- | --- | --- | --- |\n"
for q in quotes:
    md_out += f"| {q['quote']} | {q['volume']} | {q['character']} | {q['rating']} | {q['meaning']} |\n"

with open(md_path, "w", encoding="utf-8") as f:
    f.write(md_out)

# Rewrite HTML
html_head = """<!DOCTYPE html>
<html lang="ja">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>俺でなきゃ見逃しちゃう名台詞集 | 電脳ハンター協会</title>
  <style>
    :root {
      color-scheme: dark;
      --bg: #080907;
      --bg-darker: #050605;
      --panel: rgba(16, 18, 15, 0.75);
      --text: #f3f0e4;
      --muted: #a7aa9f;
      --subtle: #6f746b;
      --acid: #b9e52d;
      --gold: #d7ad4a;
      --line: rgba(231, 232, 216, .12);
      --line-strong: rgba(185, 229, 45, .2);
    }

    * { box-sizing: border-box; }
    body {
      margin: 0;
      min-height: 100vh;
      color: var(--text);
      background-color: var(--bg-darker);
      background-image: 
        radial-gradient(circle at 10% 20%, rgba(185, 229, 45, 0.04), transparent 30%),
        radial-gradient(circle at 90% 80%, rgba(185, 229, 45, 0.03), transparent 35%),
        linear-gradient(rgba(255, 255, 255, 0.015) 1px, transparent 1px),
        linear-gradient(90deg, rgba(255, 255, 255, 0.015) 1px, transparent 1px);
      background-size: 100% 100%, 100% 100%, 40px 40px, 40px 40px;
      background-attachment: fixed;
      font-family: Inter, "Hiragino Kaku Gothic ProN", "Yu Gothic", Meiryo, sans-serif;
      -webkit-font-smoothing: antialiased;
    }

    a { color: inherit; text-decoration: none; }
    
    .site-header {
      position: sticky;
      top: 0;
      z-index: 100;
      width: 100%;
      border-bottom: 1px solid var(--line);
      background: rgba(5, 6, 5, .7);
      backdrop-filter: blur(16px);
      -webkit-backdrop-filter: blur(16px);
    }
    .nav {
      display: flex;
      align-items: center;
      justify-content: space-between;
      min-height: 70px;
      width: min(1180px, calc(100% - 48px));
      margin: 0 auto;
    }
    .brand { display: flex; align-items: center; gap: 13px; }
    .brand-mark {
      display: grid;
      place-items: center;
      width: 32px;
      height: 32px;
      border: 1px solid rgba(185, 229, 45, .6);
      border-radius: 50%;
      color: var(--acid);
      font: 900 11px/1 Arial, sans-serif;
      box-shadow: inset 0 0 8px rgba(185, 229, 45, .15);
    }
    .brand-copy { font-size: 12px; font-weight: 900; letter-spacing: .12em; }
    
    .hero {
      position: relative;
      padding: 100px 0 60px;
      text-align: center;
      overflow: hidden;
    }
    .hero h1 {
      position: relative;
      font-size: clamp(32px, 4vw, 56px);
      letter-spacing: -.02em;
      margin: 0 0 16px;
      text-shadow: 0 0 30px rgba(185, 229, 45, 0.15);
    }
    .hero p {
      color: var(--muted);
      font-size: 15px;
      max-width: 600px;
      margin: 0 auto;
      line-height: 1.8;
      letter-spacing: 0.05em;
    }
    
    .container {
      width: min(1380px, calc(100% - 32px));
      margin: 40px auto 80px;
    }
    
    .table-wrapper {
      background: var(--panel);
      border: 1px solid var(--line);
      border-radius: 8px;
      backdrop-filter: blur(10px);
      -webkit-backdrop-filter: blur(10px);
      box-shadow: 0 10px 40px rgba(0,0,0, 0.3);
      overflow-x: auto;
    }
    
    table {
      width: 100%;
      border-collapse: collapse;
      text-align: left;
    }
    
    th, td {
      padding: 16px 24px;
      border-bottom: 1px solid var(--line);
    }
    
    th {
      position: sticky;
      top: 0;
      background: rgba(5, 6, 5, 0.95);
      color: var(--acid);
      font-size: 12px;
      font-weight: 800;
      letter-spacing: 0.15em;
      white-space: nowrap;
      z-index: 10;
      border-bottom: 1px solid var(--line-strong);
    }
    
    tr:last-child td {
      border-bottom: none;
    }
    
    tr:hover td {
      background: rgba(185, 229, 45, 0.04);
    }
    
    .col-vol { 
      color: var(--subtle); 
      font-family: ui-monospace, SFMono-Regular, Menlo, monospace; 
      font-size: 12px;
      white-space: nowrap; 
    }
    
    .col-char { 
      color: #cacbc3; 
      font-weight: 700; 
      font-size: 13px;
      white-space: nowrap; 
      letter-spacing: 0.05em;
    }
    
    .col-quote { 
      font-weight: 800; 
      font-size: 16px; 
      color: var(--text); 
      min-width: 280px; 
      line-height: 1.6;
      letter-spacing: 0.03em;
    }
    
    .col-meaning { 
      color: var(--muted); 
      font-size: 13px; 
      line-height: 1.7; 
      min-width: 300px;
    }

    /* Rating specific styles */
    .col-rating { 
      white-space: nowrap; 
      letter-spacing: 2px;
    }
    .rating-5 {
      color: #ffeb82;
      text-shadow: 0 0 10px rgba(255, 235, 130, 0.8), 0 0 20px rgba(255, 235, 130, 0.5);
      font-size: 16px;
      font-weight: 900;
    }
    .rating-4 {
      color: #e6ca4a;
      text-shadow: 0 0 8px rgba(230, 202, 74, 0.4);
      font-size: 14px;
      font-weight: 800;
    }
    .rating-3 {
      color: #aeb0a2;
      font-size: 13px;
      font-weight: 700;
    }
    .rating-2 {
      color: #727467;
      opacity: 0.8;
      font-size: 12px;
    }
    .rating-1 {
      color: #4b4c44;
      opacity: 0.5;
      font-size: 12px;
    }
    .rating-unknown {
      color: var(--subtle);
      font-size: 12px;
    }

  </style>
</head>
<body>
  <header class="site-header">
    <div class="nav">
      <a href="../index.html" class="brand">
        <div class="brand-mark">HXH</div>
        <div class="brand-copy">電脳ハンター協会</div>
      </a>
    </div>
  </header>
  
  <section class="hero">
    <h1>俺でなきゃ見逃しちゃう名台詞集</h1>
    <p>心を撃ち抜く一言から、通だからこそ拾える一言まで。<br>ハンターハンターの世界を彩る名言アーカイブ。</p>
  </section>

  <main class="container">
    <div class="table-wrapper">
      <table>
        <thead>
          <tr>
            <th>登場巻</th>
            <th>発言者</th>
            <th>セリフ</th>
            <th>電脳有名度</th>
            <th>意味</th>
          </tr>
        </thead>
        <tbody>
"""

html_tail = """
        </tbody>
      </table>
    </div>
  </main>
</body>
</html>
"""

table_html = ""
for q in quotes:
    quote_text = q['quote'].replace('<', '&lt;').replace('>', '&gt;')
    char_text = q['character'].replace('<', '&lt;').replace('>', '&gt;')
    vol_text = q['volume'].replace('<', '&lt;').replace('>', '&gt;')
    rating_text = q['rating'].replace('<', '&lt;').replace('>', '&gt;')
    mean_text = q['meaning'].replace('<', '&lt;').replace('>', '&gt;')
    
    star_count = rating_text.count('★')
    if star_count == 5:
        r_class = "rating-5"
    elif star_count == 4:
        r_class = "rating-4"
    elif star_count == 3:
        r_class = "rating-3"
    elif star_count == 2:
        r_class = "rating-2"
    elif star_count == 1:
        r_class = "rating-1"
    else:
        r_class = "rating-unknown"
    
    table_html += f'''
          <tr>
            <td class="col-vol">{vol_text}</td>
            <td class="col-char">{char_text}</td>
            <td class="col-quote">{quote_text}</td>
            <td class="col-rating {r_class}">{rating_text}</td>
            <td class="col-meaning">{mean_text}</td>
          </tr>
'''

final_html = html_head + table_html + html_tail

with open(html_path, "w", encoding="utf-8") as f:
    f.write(final_html)

print(f"Updated HTML and MD with {len(quotes)} quotes (Kurapika bonus removed).")

# Inject shared header
import subprocess
inject_script = "/Users/yu/Antigravity_workspace/HUNTERHUNTER-FANSITE/inject_shared_header.py"
if os.path.exists(inject_script):
    try:
        subprocess.run(["python3", inject_script], check=True)
        print("Successfully injected shared header.")
    except Exception as e:
        print(f"Failed to inject shared header: {e}")
