#!/bin/bash
set -e
cd "$(dirname "$0")"

echo "1. オートリンカーを実行しています..."
source venv/bin/activate
python3 auto_linker.py

echo "2. 公開用の静的サイトビルドの準備..."
rm -rf build_zensical_src
mkdir -p build_zensical_src/docs/stylesheets

# 管理用ファイルはコピーせず、公開したいフォルダのみをdocsへコピー
cp -r 登場人物 ストーリー 念能力 用語集 グリードアイランド_カード build_zensical_src/docs/

# 公開用TOPページの作成
STORY_COUNT=$(find ストーリー -type f -name "*.md" ! -name "index.md" | wc -l | tr -d ' ')
CHAR_COUNT=$(find 登場人物 -type f -name "*.md" ! -name "index.md" | wc -l | tr -d ' ')
NEN_COUNT=$(find 念能力 -type f -name "*.md" ! -name "index.md" | wc -l | tr -d ' ')
TERM_COUNT=$(find 用語集 -type f -name "*.md" ! -name "index.md" | wc -l | tr -d ' ')
GI_COUNT=$(grep -E "^\| No\." グリードアイランド_カード/*.md | wc -l | tr -d ' ')

cat << MD > build_zensical_src/docs/index.md
---
title: HUNTER×HUNTER 神眼データベース
---
# HUNTER×HUNTER 神眼データベース

使用したプレイヤーは、HUNTER×HUNTERに関するあらゆる設定・人物・念能力、No.001から099までの全てのカードについて、「解析」と「名簿」の効果をいつでも得ることができる。

## カテゴリ一覧
以下のリンクから各データの一覧にアクセスできます。

* 📖 **[ストーリー一覧](ストーリー/index.md)** （${STORY_COUNT}編 掲載中）
* 👤 **[登場人物一覧](登場人物/index.md)** （${CHAR_COUNT}人 掲載中）
* 💥 **[念能力一覧](念能力/index.md)** （${NEN_COUNT}件 掲載中）
* 🃏 **[グリードアイランド カード一覧](グリードアイランド_カード/01_指定ポケットカード一覧.md)** （${GI_COUNT}枚 掲載中）
* 🔍 **[用語集一覧](用語集/index.md)** （${TERM_COUNT}件 掲載中）
MD

# カスタムCSSの作成
cat << 'CSS' > build_zensical_src/docs/stylesheets/extra.css
@import url('https://fonts.googleapis.com/css2?family=Noto+Sans+JP:wght@300;400;500;700&family=Noto+Serif+JP:wght@400;500;700&display=swap');

:root {
    --md-text-font: "Noto Sans JP", sans-serif;
}
.md-typeset h1,
.md-typeset h2,
.md-typeset h3 {
    font-family: "Noto Serif JP", serif;
    font-weight: 500;
    letter-spacing: 0.05em;
}
.md-typeset h1 {
    border-bottom: 2px solid var(--md-accent-fg-color);
    padding-bottom: 0.3em;
    margin-bottom: 1em;
}
.md-typeset h2 {
    border-bottom: 1px solid var(--md-default-fg-color--lightest);
    padding-bottom: 0.3em;
    margin-top: 1.5em;
}
.md-typeset p, .md-typeset li {
    line-height: 1.9;
    letter-spacing: 0.03em;
    color: var(--md-default-fg-color--light);
}
.md-typeset a {
    transition: color 0.2s ease;
    text-decoration: none;
}
.md-typeset a:hover {
    color: var(--md-accent-fg-color);
    text-decoration: underline;
}
.md-copyright {
    display: none !important;
}
CSS

# Zensical設定ファイルの作成
cat << 'TOML' > build_zensical_src/zensical.toml
[project]
site_name = "HUNTER×HUNTER 神眼データベース"

extra_css = ["stylesheets/extra.css"]

[project.theme]
language = "ja"
features = [
  "navigation.tabs",
  "navigation.sections",
  "navigation.indexes",
  "search.highlight",
  "search.suggest",
  "toc.integrate"
]

[project.theme.icon]
logo = "lucide/eye"

[[project.theme.palette]]
media = "(prefers-color-scheme: light)"
scheme = "default"
primary = "black"
accent = "amber"
toggle.icon = "lucide/sun"
toggle.name = "Switch to dark mode"

[[project.theme.palette]]
media = "(prefers-color-scheme: dark)"
scheme = "slate"
primary = "black"
accent = "amber"
toggle.icon = "lucide/moon"
toggle.name = "Switch to light mode"

[project.markdown_extensions]
admonition = {}
pymdownx.details = {}
pymdownx.superfences = {}
TOML

echo "3. ナビゲーション階層の動的生成..."
python3 generate_zensical_nav.py

echo "4. Zensicalビルドの実行..."
cd build_zensical_src
zensical build

cd ..
rm -rf ../../public/hunterdata2
mv build_zensical_src/site ../../public/hunterdata2
rm -rf build_zensical_src

echo "5. 共通ヘッダー（Denno Hunter Association）のインジェクション..."
python3 /Users/yu/Antigravity_workspace/HUNTERHUNTER-FANSITE/inject_shared_header.py

echo "=========================================================="
echo "Zensical ビルド成功！デザインと順番が更新されました。" 
echo "=========================================================="
