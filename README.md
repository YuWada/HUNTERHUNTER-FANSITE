# HUNTER×HUNTER FAN SITE

『HUNTER×HUNTER』をテーマにした、個人制作の非公式ファンサイトです。

## 構成

- `/public/` — Cloudflare PagesでWeb公開するファイル
  - `/public/index.html` — ファンサイトのトップページ
  - `/public/hunterdata/` — HUNTER×HUNTER 神眼データベース
  - `/public/huntermizumi/` — 念能力 系統診断
  - `/public/hunterkeisai/` — ジャンプ掲載号リスト
  - `/public/huntermeigen/` — 俺でなきゃ見逃しちゃう名台詞集
  - `/public/shared/` — 全ページ共通ヘッダー、ナビゲーション、GA4設定
- `/private/` — Git管理するがWeb公開しない資料・下書き
- `/inject_shared_header.py` — 全公開HTMLに共通ヘッダーを登録するサイト共通処理

このリポジトリの `main` ブランチへのプッシュを、Cloudflare Pagesの本番公開へ自動反映します。Cloudflare PagesのBuild output directoryは `public` に設定しています。

`private/` の内容はWebサイトには公開されません。ただし、このGitHubリポジトリ自体はPublicのため、GitHub上では閲覧できます。秘密情報、個人情報、APIキーなどは保存しないでください。

## 権利関係について

本サイトは非公式のファンメイドサイトです。原作者・出版社・アニメ制作会社・その他の権利者とは一切関係なく、公式の商品・サービスではありません。
