#!/bin/bash
set -e
cd "$(dirname "$0")"

echo "1. オートリンカーを実行しています..."
python3 auto_linker.py

echo "2. 公開用の静的サイトビルドの準備..."
rm -rf build_src
mkdir -p build_src/docs

# 管理用ファイル（検討中キーワードなど）はコピーせず、公開したいフォルダのみをdocsへコピー
cp -r 登場人物 ストーリー 念能力 用語集 グリードアイランド_カード build_src/docs/

# 公開用TOPページの作成
cat << 'MD' > build_src/docs/index.md
---
title: HUNTER×HUNTER Wiki ホーム
---
# HUNTER×HUNTER Wiki へようこそ

当Wikiは、HUNTER×HUNTERに関するあらゆる設定・人物・念能力を網羅したデータベースです。

## カテゴリ一覧
以下のリンクから各データの一覧にアクセスできます。

* 👤 **[登場人物一覧](登場人物/index.html)**
* 📖 **[ストーリー一覧](ストーリー/index.html)**
* 🔍 **[用語集一覧](用語集/index.html)**
* 💥 **[念能力一覧](念能力/index.html)**
* 🃏 **[グリードアイランド カード一覧](グリードアイランド_カード/指定ポケットカード一覧.html)**
MD

# MkDocs設定ファイルの作成
cat << 'YML' > build_src/mkdocs.yml
site_name: HUNTER×HUNTER Wiki
docs_dir: docs
site_dir: /Users/yu/Antigravity_workspace/HUNTERHUNTER-FANSITE/public/hunterdata
use_directory_urls: false
theme:
  name: material
  language: ja
  features:
    - navigation.tabs
    - navigation.top
    - search.suggest
    - search.highlight
markdown_extensions:
  - admonition
  - pymdownx.details
  - pymdownx.superfences
YML

echo "3. MkDocsビルドの実行..."
cd build_src
source /Users/yu/Documents/Daiv_Antigravity/Antigravity20/HUNTER_DATA/venv/bin/activate
mkdocs build

cd ..
rm -rf build_src

echo "=========================================================="
echo "ビルド成功！"
echo "HTMLファイルは /Users/yu/Antigravity_workspace/HUNTERHUNTER-FANSITE/public/hunterdata に出力されました。"
echo "=========================================================="
