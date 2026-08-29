import re
import os
import json
from datetime import datetime, timedelta
from html.parser import HTMLParser

class JajankenParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.in_tr = False
        self.in_td = False
        self.td_class = ""
        self.in_pill = False
        self.current_row = {}
        self.data = []
        self.current_href = ""
        self.current_title_text = ""
        self.current_remarks = []
        
    def handle_starttag(self, tag, attrs):
        attrs_dict = dict(attrs)
        if tag == "tr":
            self.in_tr = True
            self.current_row = {"issue_name": "", "issue_date": "", "title": "", "remarks": [], "order": ""}
            self.current_title_text = ""
            self.current_remarks = []
        elif tag == "td" and self.in_tr:
            self.in_td = True
            self.td_class = attrs_dict.get("class", "").strip()
            self.current_text = ""
        elif tag == "a" and self.in_td and "issue" in self.td_class:
            self.current_href = attrs_dict.get("href", "")
        elif tag == "span" and self.in_td and "title" in self.td_class:
            cls = attrs_dict.get("class", "")
            if "chapter-pill" in cls:
                self.in_pill = True
                
    def handle_endtag(self, tag):
        if tag == "tr":
            self.in_tr = False
            if self.current_row.get("issue_name"):
                self.current_row["title"] = self.current_title_text.strip()
                self.current_row["remarks"] = self.current_remarks
                self.data.append(self.current_row)
        elif tag == "td":
            self.in_td = False
            if "issue" in self.td_class:
                self.current_row["issue_name"] = self.current_text.strip()
                if self.current_href.startswith("/issues/"):
                    self.current_row["issue_date"] = self.current_href.split("/")[2]
            elif "order" in self.td_class:
                self.current_row["order"] = self.current_text.strip()
            self.current_text = ""
            self.td_class = ""
        elif tag == "span" and self.in_pill:
            self.in_pill = False

    def handle_data(self, data):
        if self.in_td:
            if "title" in self.td_class:
                if self.in_pill:
                    self.current_remarks.append(data.strip())
                else:
                    self.current_title_text += data
            else:
                self.current_text += data

with open('/Users/yu/.gemini/antigravity/brain/5e19d2a4-4e72-4120-9d34-f2217034f781/.system_generated/steps/3/content.md', 'r') as f:
    html = f.read()

parser = JajankenParser()
parser.feed(html)

def get_volume(chapter_num):
    if chapter_num <= 8: return 1
    elif chapter_num <= 17: return 2
    elif chapter_num <= 26: return 3
    elif chapter_num <= 35: return 4
    elif chapter_num <= 44: return 5
    elif chapter_num <= 54: return 6
    elif chapter_num <= 63: return 7
    elif chapter_num <= 73: return 8
    elif chapter_num <= 83: return 9
    elif chapter_num <= 93: return 10
    elif chapter_num <= 103: return 11
    elif chapter_num <= 115: return 12
    elif chapter_num <= 127: return 13
    elif chapter_num <= 137: return 14
    elif chapter_num <= 147: return 15
    elif chapter_num <= 157: return 16
    elif chapter_num <= 167: return 17
    elif chapter_num <= 177: return 18
    elif chapter_num <= 187: return 19
    elif chapter_num <= 199: return 20
    elif chapter_num <= 211: return 21
    elif chapter_num <= 223: return 22
    elif chapter_num <= 235: return 23
    elif chapter_num <= 247: return 24
    elif chapter_num <= 257: return 25
    elif chapter_num <= 267: return 26
    elif chapter_num <= 278: return 27
    elif chapter_num <= 290: return 28
    elif chapter_num <= 300: return 29
    elif chapter_num <= 310: return 30
    elif chapter_num <= 320: return 31
    elif chapter_num <= 330: return 32
    elif chapter_num <= 340: return 33
    elif chapter_num <= 350: return 34
    elif chapter_num <= 360: return 35
    elif chapter_num <= 370: return 36
    elif chapter_num <= 380: return 37
    elif chapter_num <= 390: return 38
    elif chapter_num <= 400: return 39
    elif chapter_num <= 410: return 39
    else: return None

output_data = []
published_dates = []

for row in parser.data:
    row["title"] = re.sub(r'\s+', ' ', row["title"]).strip()
    match = re.search(r'No\.(\d+)', row["title"])
    vol_str = ""
    is_published = 1
    
    # Check if this row is actually a publication
    if "休載" in row["remarks"] or "休載" in row["title"] or not match:
        is_published = 0
        
    if match:
        chap_num = int(match.group(1))
        if chap_num <= 380: vol = get_volume(chap_num)
        elif chap_num <= 390: vol = 37
        elif chap_num <= 400: vol = 38
        elif chap_num <= 410: vol = 39
        else: vol = None

        if vol:
            vol_str = f"{vol}巻"
        else:
            vol_str = "未収録"
    else:
        vol_str = "-"
    
    remarks_str = ", ".join(row["remarks"])
    
    output_data.append({
        "issue": row["issue_name"],
        "date": row["issue_date"],
        "title": row["title"],
        "volume": vol_str,
        "remarks": remarks_str
    })
    
    if row["issue_date"] and is_published == 1:
        try:
            dt = datetime.strptime(row["issue_date"], "%Y-%m-%d")
            actual_release_dt = dt - timedelta(days=14)
            published_dates.append(actual_release_dt)
        except:
            pass

# Create continuous weekly timeline
published_dates.sort()
start_date = published_dates[0]
# Determine the end date (we want to cover up to today or the latest published date)
end_date = max(published_dates[-1], datetime.now())

chart_data = []
current_date = start_date

while current_date <= end_date:
    # Check if there is any published_date within +/- 3 days of current_date
    is_pub = 0
    issue_info = "休載"
    
    for pd in published_dates:
        if abs((pd - current_date).days) <= 3:
            is_pub = 1
            issue_info = "掲載"
            break
            
    chart_data.append({
        "x": current_date.strftime("%Y-%m-%d"),
        "y": is_pub,
        "issue": issue_info
    })
    
    current_date += timedelta(days=7)

html_output_path = "/Users/yu/Antigravity_workspace/HUNTERHUNTER-FANSITE/public/hunterkeisai/index.html"

# Generate HTML
html_content = f"""<!DOCTYPE html>
<html lang="ja">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>ジャンプ掲載データ | 電脳ハンター協会</title>
  <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
  <script src="https://cdn.jsdelivr.net/npm/chartjs-adapter-date-fns/dist/chartjs-adapter-date-fns.bundle.min.js"></script>
  <style>
    :root {{
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
    }}

    * {{ box-sizing: border-box; }}
    body {{
      margin: 0;
      min-height: 100vh;
      color: var(--text);
      background:
        radial-gradient(circle at 12% 34%, rgba(185, 229, 45, .055), transparent 30rem),
        radial-gradient(circle at 90% 74%, rgba(229, 67, 53, .07), transparent 28rem),
        var(--bg);
      font-family: Inter, "Hiragino Kaku Gothic ProN", "Yu Gothic", Meiryo, sans-serif;
      -webkit-font-smoothing: antialiased;
      padding-top: 100px;
      padding-bottom: 60px;
    }}
    
    a {{ color: inherit; text-decoration: none; }}

    .wrap {{ width: min(1180px, calc(100% - 48px)); margin: 0 auto; }}
    
    .site-header {{
      position: fixed;
      top: 0;
      left: 0;
      width: 100%;
      border-bottom: 1px solid rgba(255, 255, 255, .12);
      background: linear-gradient(to bottom, rgba(5, 6, 5, .95), rgba(5, 6, 5, .78));
      backdrop-filter: blur(8px);
      -webkit-backdrop-filter: blur(8px);
      z-index: 100;
    }}
    .nav {{ display: flex; align-items: center; justify-content: space-between; min-height: 86px; padding: 0 24px; }}
    .brand {{ display: flex; align-items: center; gap: 13px; }}
    .brand-mark {{
      display: grid;
      place-items: center;
      width: 38px;
      height: 38px;
      border: 1px solid rgba(185, 229, 45, .7);
      border-radius: 50%;
      color: var(--acid);
      font: 900 12px/1 Arial, sans-serif;
      box-shadow: inset 0 0 0 5px rgba(185, 229, 45, .06);
    }}
    .brand-copy {{ font-size: 13px; font-weight: 900; letter-spacing: .1em; }}
    
    .page-title {{
      font-size: 2rem;
      font-weight: 900;
      text-align: center;
      margin: 40px 0 10px;
      color: var(--acid);
      letter-spacing: 0.1em;
      text-shadow: 0 0 10px rgba(185, 229, 45, 0.2);
    }}
    
    .note {{
      text-align: center;
      font-size: 13px;
      color: var(--muted);
      margin-bottom: 30px;
      line-height: 1.6;
    }}

    .note strong {{
      color: var(--gold);
    }}

    .table-wrapper {{
      background: rgba(16, 18, 15, 0.8);
      backdrop-filter: blur(10px);
      -webkit-backdrop-filter: blur(10px);
      border: 1px solid var(--line);
      border-radius: 12px;
      overflow-y: auto;
      max-height: 600px;
      margin-bottom: 40px;
      box-shadow: var(--shadow);
    }}

    table {{
      width: 100%;
      border-collapse: collapse;
      text-align: left;
    }}
    
    thead {{
      position: sticky;
      top: 0;
      z-index: 10;
      background: rgba(20, 22, 19, 0.95);
      backdrop-filter: blur(5px);
    }}

    th, td {{
      padding: 16px 20px;
      border-bottom: 1px solid var(--line);
      white-space: nowrap;
    }}

    th {{
      color: var(--muted);
      font-size: 12px;
      font-weight: 700;
      letter-spacing: 0.1em;
      text-transform: uppercase;
      border-bottom: 2px solid var(--line-strong);
    }}

    td {{
      font-size: 14px;
    }}

    tr:hover td {{
      background: rgba(255, 255, 255, 0.04);
    }}

    .tag {{
      display: inline-block;
      padding: 4px 8px;
      border-radius: 4px;
      font-size: 11px;
      font-weight: bold;
      margin-right: 4px;
    }}

    .tag-new {{ background: rgba(229, 67, 53, 0.2); color: var(--red); border: 1px solid rgba(229, 67, 53, 0.4); }}
    .tag-color {{ background: rgba(215, 173, 74, 0.2); color: var(--gold); border: 1px solid rgba(215, 173, 74, 0.4); }}
    .tag-rest {{ background: rgba(255, 255, 255, 0.1); color: var(--muted); border: 1px solid var(--line); }}
    
    .vol-badge {{
      display: inline-block;
      padding: 4px 10px;
      background: rgba(185, 229, 45, 0.1);
      color: var(--acid);
      border-radius: 20px;
      font-weight: bold;
      font-size: 12px;
      border: 1px solid rgba(185, 229, 45, 0.3);
    }}
    .vol-badge.unrecorded {{
      background: transparent;
      color: var(--subtle);
      border-color: var(--line-strong);
    }}
    .vol-badge.rest {{
      background: transparent;
      color: var(--subtle);
      border-color: transparent;
    }}
    
    .chart-container {{
      background: rgba(16, 18, 15, 0.8);
      backdrop-filter: blur(10px);
      -webkit-backdrop-filter: blur(10px);
      border: 1px solid var(--line);
      border-radius: 12px;
      padding: 24px 24px 40px;
      box-shadow: var(--shadow);
      margin-bottom: 40px;
      height: 260px; 
      position: relative;
    }}
    
    .chart-title {{
      font-size: 1.2rem;
      font-weight: 700;
      color: var(--text);
      margin-top: 0;
      margin-bottom: 12px;
      text-align: center;
      letter-spacing: 0.05em;
    }}
    
    .chart-legend {{
      display: flex;
      justify-content: center;
      gap: 20px;
      margin-bottom: 12px;
      font-size: 12px;
      color: var(--muted);
    }}
    .legend-item {{
      display: flex;
      align-items: center;
      gap: 6px;
    }}
    .legend-color {{
      width: 12px;
      height: 12px;
      border-radius: 3px;
    }}
    .legend-published {{ background: var(--acid); }}
    .legend-rest {{ background: rgba(255, 255, 255, 0.1); border: 1px solid var(--line); }}

    .canvas-wrapper {{
      position: relative;
      height: 100%;
      width: 100%;
    }}
  </style>
</head>
<body>

  <header class="site-header">
    <div class="wrap nav">
      <a href="../" class="brand">
        <div class="brand-mark">HXH</div>
        <div class="brand-copy">電脳ハンター協会</div>
      </a>
    </div>
  </header>

  <div class="wrap">
    <h1 class="page-title">ジャンプ掲載データ</h1>
    <p class="note">
      ※一覧の「発刊日」は、ジャンプの<strong>表紙に印字されている日付（号数と同じ日付）</strong>を記載しています。<br>
      実際の発売日（書店で購入できる日）は、この発刊日より<strong>約2週間前</strong>となります。
    </p>
    
    <div class="table-wrapper">
      <table>
        <thead>
          <tr>
            <th>掲載号</th>
            <th>発刊日(表紙日付)</th>
            <th>タイトル</th>
            <th>コミックス</th>
            <th>備考</th>
          </tr>
        </thead>
        <tbody>
"""

def format_remarks(remarks_str, title_str):
    if not remarks_str:
        if "休載" in title_str:
            return '<span class="tag tag-rest">休載</span>'
        return ""
    
    html_tags = []
    for r in remarks_str.split(", "):
        if "新連載" in r:
            html_tags.append(f'<span class="tag tag-new">{r}</span>')
        elif "カラー" in r:
            html_tags.append(f'<span class="tag tag-color">{r}</span>')
        elif "休載" in r:
            html_tags.append(f'<span class="tag tag-rest">{r}</span>')
        else:
            html_tags.append(f'<span class="tag">{r}</span>')
    return "".join(html_tags)

def format_volume(vol_str):
    if vol_str == "未収録":
        return '<span class="vol-badge unrecorded">未収録</span>'
    elif vol_str == "-":
        return '<span class="vol-badge rest">-</span>'
    elif vol_str:
        return f'<span class="vol-badge">{vol_str}</span>'
    return ""

for row in output_data:
    html_content += f"""
          <tr>
            <td>{row['issue']}</td>
            <td>{row['date']}</td>
            <td>{row['title']}</td>
            <td>{format_volume(row['volume'])}</td>
            <td>{format_remarks(row['remarks'], row['title'])}</td>
          </tr>"""

html_content += f"""
        </tbody>
      </table>
    </div>
    
    <div class="chart-container">
      <h2 class="chart-title">HUNTER×HUNTER 掲載・休載履歴 (1998 - 2026)</h2>
      <div class="chart-legend">
        <div class="legend-item"><div class="legend-color legend-published"></div>掲載(1)</div>
        <div class="legend-item"><div class="legend-color legend-rest"></div>休載(0)</div>
      </div>
      <div class="canvas-wrapper">
        <canvas id="publishChart"></canvas>
      </div>
    </div>
  </div>

  <script>
    const chartData = {json.dumps(chart_data)};
    
    const dataPoints = chartData.map(d => ({{ x: d.x, y: d.y, issue: d.issue }}));
    
    const ctx = document.getElementById('publishChart').getContext('2d');
    
    let gradient = ctx.createLinearGradient(0, 0, 0, 200);
    gradient.addColorStop(0, 'rgba(185, 229, 45, 0.5)');
    gradient.addColorStop(1, 'rgba(185, 229, 45, 0.0)');

    new Chart(ctx, {{
      type: 'line',
      data: {{
        datasets: [{{
          label: '掲載状況',
          data: dataPoints,
          borderColor: '#b9e52d',
          backgroundColor: gradient,
          borderWidth: 1.5,
          pointRadius: 0,
          pointHoverRadius: 4,
          stepped: 'middle',
          fill: true
        }}]
      }},
      options: {{
        responsive: true,
        maintainAspectRatio: false,
        interaction: {{
          mode: 'index',
          intersect: false,
        }},
        plugins: {{
          legend: {{ display: false }},
          tooltip: {{
            backgroundColor: 'rgba(10, 12, 10, 0.9)',
            titleColor: '#f3f0e4',
            bodyColor: '#b9e52d',
            borderColor: 'rgba(231, 232, 216, 0.14)',
            borderWidth: 1,
            callbacks: {{
              title: function(context) {{
                const d = context[0].raw;
                return '週: ' + d.x;
              }},
              label: function(context) {{
                return context.raw.y === 1 ? '掲載' : '休載 (データなし)';
              }}
            }}
          }}
        }},
        scales: {{
          x: {{
            type: 'time',
            time: {{
              unit: 'year',
              displayFormats: {{
                year: 'yyyy年'
              }}
            }},
            grid: {{
              color: 'rgba(231, 232, 216, 0.05)',
              drawBorder: false,
            }},
            ticks: {{
              color: '#a7aa9f',
              font: {{ size: 11, weight: 'bold' }},
              maxRotation: 0
            }}
          }},
          y: {{
            min: 0,
            max: 1.1,
            grid: {{
              color: 'rgba(231, 232, 216, 0.08)',
              drawBorder: false,
            }},
            ticks: {{
              stepSize: 1,
              color: '#6f746b',
              callback: function(value) {{
                if (value === 1) return '掲載';
                if (value === 0) return '休載';
                return '';
              }},
              font: {{ size: 10 }}
            }}
          }}
        }}
      }}
    }});
  </script>
</body>
</html>
"""

with open(html_output_path, "w") as f:
    f.write(html_content)

print(f"HTML updated with interpolated chart at {html_output_path}")

