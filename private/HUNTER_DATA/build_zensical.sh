#!/bin/bash
set -e
cd "$(dirname "$0")"

echo "1. オートリンカーを実行しています..."
source venv/bin/activate
python3 auto_linker.py

echo "1.5. 人物名一覧（index.md）を動的生成しています..."
python3 generate_char_index.py

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
site_url = "https://hunterhunter-fansite.pages.dev/hunterdata2/"

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

echo "6. SEO情報のインジェクション..."
python3 inject_seo.py

echo "7. llms.txt の生成と出力..."
cat << 'LLMS' > ../../public/hunterdata2/llms.txt
# HUNTER×HUNTER 神眼データベース (Shingan DB)

> 本ファイルは、AI（LLM）やエージェントが神眼データベースの構成とナレッジグラフを効率的にクローリング・把握できるよう提供されている `llms.txt` です。

## 概要
神眼データベースは、漫画『HUNTER×HUNTER』に関するあらゆる設定、登場人物、念能力、用語、作中の出来事を網羅し、それぞれを相互にリンクさせたナレッジグラフ（知識ベース）です。
各ページはOKF（Open Knowledge Format）に近い構造のMarkdownをベースに構築されており、高い情報密度と相互リンクを持ちます。AIエージェントがページ間のリンクを辿ることで、複雑な文脈や関連性を正確に把握できるように最適化されています。

## 主要なカテゴリと提供情報

### 📖 [ストーリー一覧](./ストーリー/)
各エピソード（ハンター試験編、ヨークシンシティ編、キメラ＝アント編など）のあらすじや、関連する出来事、登場人物へのリンクをまとめています。時系列やストーリー全体の流れを把握する際の起点となります。

### 👤 [登場人物一覧](./登場人物/)
HUNTER×HUNTERに登場する全キャラクターの詳細な解説インデックスです。
略歴、人物像、所属（幻影旅団、ゾルディック家、十二支んなど）のほか、修得している「念能力」や関係する「ストーリー編」へのリンクが含まれています。各キャラクターページには `tags` などのメタデータが付与されています。

### 💥 [念能力一覧](./念能力/)
作中に登場するあらゆる「念能力」の詳細情報のインデックスです。
能力名、使用者、念の系統（強化系、変化系、具現化系、放出系、操作系、特質系）、具体的な能力の仕組みや「制約と誓約」などについて解説しています。

### 🔍 [用語集一覧](./用語集/)
世界観を構成する専門用語の解説インデックスです。
「念」「ハンター協会」「暗黒大陸」などの大分類から、「水見式」「円」「絶」などの詳細な設定まで、作品の深い理解に不可欠な知識を網羅しています。

### 🃏 [グリードアイランド カード一覧](./グリードアイランド_カード/01_指定ポケットカード一覧/)
作中のゲーム「グリードアイランド」に登場する指定ポケットカード（No.000〜099）などのリストです。
カード名、入手難易度、ランク、限界化枚数、およびカードの具体的な効果を詳細に記載しています。

## AIエージェントへの推奨クローリング・探索手順
1. まず上記の各カテゴリの「一覧ページ」にアクセスし、全体像と利用可能な情報のリストを把握してください。
2. ユーザーの質問に応じて、一覧ページから関連する個別のエンティティ（人物、能力、用語）のページへとアクセスしてください。
3. 各ページ内の文中に含まれるリンクは、関連する重要な知識へのパスです。これらを芋づる式にたどる（GraphRAGアプローチ）ことで、情報が断片化せず、文脈に沿った正確かつ高度な推論が可能になります。
LLMS

echo "=========================================================="
echo "Zensical ビルド成功！デザインと順番が更新されました。" 
echo "=========================================================="
