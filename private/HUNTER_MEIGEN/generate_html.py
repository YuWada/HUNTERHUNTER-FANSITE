import re
import os

md_path = "/Users/yu/Antigravity_workspace/HUNTERHUNTER-FANSITE/private/HUNTER_MEIGEN/俺でなきゃ見逃しちゃう名台詞集.md"
html_path = "/Users/yu/Antigravity_workspace/HUNTERHUNTER-FANSITE/public/huntermeigen/index.html"

with open(md_path, "r", encoding="utf-8") as f:
    content = f.read()

# Extract table rows
# Format: | セリフ | 登場巻・話数 | 発言者 | 意味 |
quotes = []
in_table = False
for line in content.split('\n'):
    line = line.strip()
    if line.startswith('| セリフ') or line.startswith('| ---'):
        in_table = True
        continue
    if in_table and line.startswith('|'):
        cols = [c.strip() for c in line.split('|')[1:-1]]
        if len(cols) >= 4:
            quotes.append({
                'quote': cols[0],
                'volume': cols[1],
                'character': cols[2],
                'meaning': cols[3]
            })
    elif in_table and not line:
        pass

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
      --panel: #10120f;
      --text: #f3f0e4;
      --muted: #a7aa9f;
      --subtle: #6f746b;
      --acid: #b9e52d;
      --gold: #d7ad4a;
      --red: #e54335;
      --line: rgba(231, 232, 216, .14);
      --line-strong: rgba(231, 232, 216, .28);
      --shadow: 0 28px 80px rgba(0, 0, 0, .42);
    }

    * { box-sizing: border-box; }
    body {
      margin: 0;
      min-height: 100vh;
      color: var(--text);
      background: var(--bg);
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
      background: rgba(5, 6, 5, .85);
      backdrop-filter: blur(12px);
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
      width: 30px;
      height: 30px;
      border: 1px solid rgba(185, 229, 45, .7);
      border-radius: 50%;
      color: var(--acid);
      font: 900 10px/1 Arial, sans-serif;
    }
    .brand-copy { font-size: 11px; font-weight: 900; letter-spacing: .1em; }
    
    .hero {
      padding: 100px 0 60px;
      text-align: center;
      background: radial-gradient(circle at 50% 0%, rgba(185, 229, 45, .05), transparent 40rem);
      border-bottom: 1px solid var(--line);
    }
    .hero h1 {
      font-size: clamp(32px, 5vw, 56px);
      letter-spacing: -.03em;
      margin: 0 0 16px;
    }
    .hero p {
      color: var(--muted);
      font-size: 16px;
      max-width: 600px;
      margin: 0 auto;
      line-height: 1.8;
    }
    
    .container {
      width: min(1280px, calc(100% - 48px));
      margin: 60px auto;
    }
    
    .grid {
      display: grid;
      grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
      gap: 24px;
    }
    
    .card {
      background: var(--panel);
      border: 1px solid var(--line);
      border-radius: 6px;
      padding: 32px 28px;
      transition: transform 0.3s ease, border-color 0.3s ease, box-shadow 0.3s ease;
      display: flex;
      flex-direction: column;
      position: relative;
      overflow: hidden;
    }
    
    .card::before {
      content: "";
      position: absolute;
      top: 0; left: 0; right: 0; height: 3px;
      background: linear-gradient(90deg, var(--acid), transparent);
      opacity: 0;
      transition: opacity 0.3s ease;
    }
    
    .card:hover {
      transform: translateY(-5px);
      border-color: rgba(185, 229, 45, .4);
      box-shadow: 0 12px 40px rgba(0,0,0, .5);
    }
    
    .card:hover::before {
      opacity: 1;
    }
    
    .card-quote {
      font-size: 20px;
      font-weight: 800;
      line-height: 1.6;
      margin: 0 0 20px;
      color: var(--text);
      letter-spacing: 0.02em;
    }
    
    .card-meta {
      display: flex;
      align-items: center;
      gap: 12px;
      margin-bottom: 20px;
      font-size: 12px;
      font-weight: 700;
    }
    
    .card-character {
      color: var(--acid);
      padding: 4px 10px;
      background: rgba(185, 229, 45, 0.1);
      border-radius: 20px;
      letter-spacing: 0.1em;
    }
    
    .card-volume {
      color: var(--subtle);
      font-family: ui-monospace, SFMono-Regular, Menlo, monospace;
    }
    
    .card-meaning {
      color: var(--muted);
      font-size: 13px;
      line-height: 1.8;
      margin-top: auto;
      padding-top: 20px;
      border-top: 1px solid var(--line);
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
    <div class="grid">
"""

html_tail = """
    </div>
  </main>
</body>
</html>
"""

cards_html = ""
for q in quotes:
    # Basic escaping
    quote_text = q['quote'].replace('<', '&lt;').replace('>', '&gt;')
    char_text = q['character'].replace('<', '&lt;').replace('>', '&gt;')
    vol_text = q['volume'].replace('<', '&lt;').replace('>', '&gt;')
    mean_text = q['meaning'].replace('<', '&lt;').replace('>', '&gt;')
    
    cards_html += f'''
      <div class="card">
        <div class="card-meta">
          <span class="card-character">{char_text}</span>
          <span class="card-volume">{vol_text}</span>
        </div>
        <h2 class="card-quote">{quote_text}</h2>
        <div class="card-meaning">{mean_text}</div>
      </div>
'''

final_html = html_head + cards_html + html_tail

os.makedirs(os.path.dirname(html_path), exist_ok=True)
with open(html_path, "w", encoding="utf-8") as f:
    f.write(final_html)

print(f"Generated HTML with {len(quotes)} quotes.")
