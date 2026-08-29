import re
import csv
from html.parser import HTMLParser
import json

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

# Calculate volume based on typical mapping
# We'll use a dynamic approach to map chapter number to volume
# Usually 9-10 chapters per volume.
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
    elif chapter_num <= 410: return 40
    else: return (chapter_num - 1) // 10 + 1 # fallback

output_data = []
for row in parser.data:
    row["title"] = re.sub(r'\s+', ' ', row["title"]).strip()
    # Extract chapter number
    match = re.search(r'No\.(\d+)', row["title"])
    vol_str = ""
    if match:
        chap_num = int(match.group(1))
        vol_str = f"{get_volume(chap_num)}巻"
    else:
        if "休載" in row["remarks"] or "休載" in row["title"]:
            vol_str = "-"
    
    remarks_str = ", ".join(row["remarks"])
    
    output_data.append({
        "掲載号": row["issue_name"],
        "発売日": row["issue_date"],
        "タイトル": row["title"],
        "コミックス": vol_str,
        "備考": remarks_str
    })

# Write to markdown file
output_path = "/Users/yu/Antigravity_workspace/HUNTERHUNTER-FANSITE/private/HUNTER_KEISAI/hunter_jajanken_list.md"
import os
os.makedirs(os.path.dirname(output_path), exist_ok=True)

with open(output_path, "w") as f:
    f.write("# HUNTER×HUNTER ジャンプ掲載・コミックス収録一覧\n\n")
    f.write("| 掲載号 | 発売日 | タイトル | コミックス | 備考 |\n")
    f.write("|---|---|---|---|---|\n")
    for row in output_data:
        f.write(f"| {row['掲載号']} | {row['発売日']} | {row['タイトル']} | {row['コミックス']} | {row['備考']} |\n")

print(f"List generated at {output_path}")

