#!/bin/bash
set -e
cd "$(dirname "$0")"

echo "1. オートリンカーを実行しています..."
python3 auto_linker.py

echo "2. 公開用の静的サイトビルドの準備..."
rm -rf build_src
mkdir -p build_src/docs/stylesheets

# 管理用ファイルはコピーせず、公開したいフォルダのみをdocsへコピー
cp -r 登場人物 ストーリー 念能力 用語集 グリードアイランド_カード build_src/docs/

# 公開用TOPページの作成
# 各カテゴリの掲載数を動的にカウント
STORY_COUNT=$(find ストーリー -type f -name "*.md" ! -name "index.md" | wc -l | tr -d ' ')
CHAR_COUNT=$(find 登場人物 -type f -name "*.md" ! -name "index.md" | wc -l | tr -d ' ')
NEN_COUNT=$(find 念能力 -type f -name "*.md" ! -name "index.md" | wc -l | tr -d ' ')
TERM_COUNT=$(find 用語集 -type f -name "*.md" ! -name "index.md" | wc -l | tr -d ' ')
GI_COUNT=$(grep -E "^\| No\." グリードアイランド_カード/*.md | wc -l | tr -d ' ')

# EOFをクォートせずに展開させる
cat << MD > build_src/docs/index.md
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
cat << 'CSS' > build_src/docs/stylesheets/extra.css
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
CSS

# MkDocs設定ファイルの作成（プレーン）
cat << 'YML' > build_src/mkdocs.yml
site_name: HUNTER×HUNTER 神眼データベース
docs_dir: docs
site_dir: ../../../public/hunterdata
use_directory_urls: false

theme:
  icon:
    logo: material/eye-circle
  favicon: assets/favicon.png

  name: material
  language: ja
  palette:
    - media: "(prefers-color-scheme: light)"
      scheme: default
      primary: black
      accent: amber
      toggle:
        icon: material/brightness-7
        name: ダークモードに切り替え
    - media: "(prefers-color-scheme: dark)"
      scheme: slate
      primary: black
      accent: amber
      toggle:
        icon: material/brightness-4
        name: ライトモードに切り替え
  font:
    text: Noto Sans JP
    code: Roboto Mono
  features:
    - navigation.tabs
    - navigation.sections
    - navigation.indexes
    - toc.integrate
    - search.suggest
    - search.highlight
    - header.autohide

markdown_extensions:
  - admonition
  - pymdownx.details
  - pymdownx.superfences

extra_css:
  - stylesheets/extra.css
YML

echo "3. ナビゲーション階層の動的生成..."
source /Users/yu/Documents/Daiv_Antigravity/Antigravity20/HUNTER_DATA/venv/bin/activate
python3 generate_nav.py

echo "4. MkDocsビルドの実行..."
cd build_src
mkdocs build

cd ..
rm -rf build_src

echo "=========================================================="
echo "ビルド成功！デザインと順番が更新されました。"
echo "=========================================================="
