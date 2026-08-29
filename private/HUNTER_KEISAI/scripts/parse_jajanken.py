import urllib.request
import re
from html.parser import HTMLParser

class JajankenParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.in_tr = False
        self.in_td = False
        self.td_class = ""
        self.current_row = {}
        self.data = []
        self.current_href = ""
        self.current_text = ""
        
    def handle_starttag(self, tag, attrs):
        attrs_dict = dict(attrs)
        if tag == "tr":
            self.in_tr = True
            self.current_row = {"issue_name": "", "issue_date": "", "title": "", "remarks": [], "order": ""}
        elif tag == "td" and self.in_tr:
            self.in_td = True
            self.td_class = attrs_dict.get("class", "").strip()
            self.current_text = ""
        elif tag == "a" and self.in_td and "issue" in self.td_class:
            self.current_href = attrs_dict.get("href", "")
        elif tag == "span" and self.in_td and "title" in self.td_class:
            if "chapter-pill" in attrs_dict.get("class", ""):
                pass # Text will be captured
                
    def handle_endtag(self, tag):
        if tag == "tr":
            self.in_tr = False
            if self.current_row.get("issue_name"):
                self.data.append(self.current_row)
        elif tag == "td":
            self.in_td = False
            if "issue" in self.td_class:
                self.current_row["issue_name"] = self.current_text.strip()
                if self.current_href.startswith("/issues/"):
                    self.current_row["issue_date"] = self.current_href.split("/")[2]
            elif "title" in self.td_class:
                # Remove extra spaces
                text = re.sub(r'\s+', ' ', self.current_text.strip())
                self.current_row["title"] = text
            elif "order" in self.td_class:
                self.current_row["order"] = self.current_text.strip()
            self.current_text = ""
            self.td_class = ""

    def handle_data(self, data):
        if self.in_td:
            if "title" in self.td_class:
                # Extract remarks if they are in span, but it's simpler to just collect text.
                # Actually, the parser calls handle_data for spans too.
                # Let's accumulate.
                self.current_text += data + " "
            else:
                self.current_text += data

with open('/Users/yu/.gemini/antigravity/brain/5e19d2a4-4e72-4120-9d34-f2217034f781/.system_generated/steps/3/content.md', 'r') as f:
    html = f.read()

parser = JajankenParser()
parser.feed(html)

for row in parser.data[:5]:
    print(row)

