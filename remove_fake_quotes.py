import re

fake_quotes = [
    "「俺はオレの道を行く」",
    "「親父に会いに行く！」",
    "「アホか お前ら！」",
    "「もう 少し ほめて……」",
    "「コインは表か？ 裏か？」",
    "「オレは俳句で勝負するぜ」",
    "「あいつはオレのダチだ！」",
    "「斬る!!」",
    "「オレの望みは 全てをぶっ壊すこと」",
    "「信じない!! この眼で確かめるまで!!」",
    "「オレが クモを捕まえる！」",
    "「鎖野郎の記憶…！！」",
    "「オレ達の命よりも ゴンの命が大事だ」",
    "「何もしないで後悔するのは嫌だ」",
    "「金で買えないモノは 山ほどあるぜ」",
    "「命の音を… 聴かせてやる…」",
    "「命を粗末にするなよ」",
    "「楽しもうぜ………!!」",
    "「一坪の海岸線……… 手に入れたぞ!!」",
    "「あいつは……… オレが………!!」",
    "「生き残る気がない奴は 足手まといだ」",
    "「助けて…」",
    "「私が… 守る…!!」",
    "「お前ら…… 全員…… ぶっ飛ばす……!!」",
    "「私に…… 指図するな……!!」",
    "「煙に巻いてやるよ……」",
    "「私は…… 王を…… 愛している……!!」",
    "「貴様らに…… 明日はない……!!」",
    "「お前は…… 誰だ……？」",
    "「オレは…… タコだ……!!」",
    "「もう…… 終わりか……？」",
    "「お前達に…… 未来は…… ない……!!」",
    "「カイトを…… 返せ……!!」",
    "「なんだ…… この感情は……？」",
    "「虫が…… 上からもの言ってんじゃねーぞ」",
    "「オレは…… 会長に…… なります……!!」",
    "「オレ達で 世界樹（トップ）へ 行こう」",
    "「私は…王になる」",
    "「均衡（バランス）は… 崩れた」",
    "「逃げるのが一番さ」"
]

with open("/Users/yu/Antigravity_workspace/HUNTERHUNTER-FANSITE/public/huntermeigen/index.html", "r", encoding="utf-8") as f:
    html = f.read()

def replacer(match):
    tr_content = match.group(0)
    for fq in fake_quotes:
        if fq in tr_content:
            return ""  # Remove the tr entirely
    return tr_content

new_html = re.sub(r"<tr[^>]*>.*?</tr>", replacer, html, flags=re.DOTALL)

with open("/Users/yu/Antigravity_workspace/HUNTERHUNTER-FANSITE/public/huntermeigen/index.html", "w", encoding="utf-8") as f:
    f.write(new_html)

print("Removed fake quotes.")
