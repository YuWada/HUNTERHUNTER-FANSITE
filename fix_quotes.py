import re

html_path = '/Users/yu/Antigravity_workspace/HUNTERHUNTER-FANSITE/public/huntermeigen/index.html'

with open(html_path, 'r', encoding='utf-8') as f:
    content = f.read()

replacements = {
    "「キミの敗因は 容量（メモリ）のムダ使い♣」": "「キミの敗因は容量（メモリ）のムダ使い❤︎」",
    "「答は『ボクと戦う』だ♠」": "「答は『ボクと戦う』だ♣」",
    "「うん 合格♣」": "「うん 合格♠」",
    "「奇術師に不可能はない♠」": "「奇術師に不可能はない♦」",
    "「残念ながらキミには惹かれないなァ♠」": "「残念ながらキミには惹かれないなァ♣」",
}

for old, new in replacements.items():
    content = content.replace(old, new)

with open(html_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("Quotes replaced.")
