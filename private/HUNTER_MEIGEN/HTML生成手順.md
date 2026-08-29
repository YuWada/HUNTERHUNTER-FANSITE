# HTML生成手順

データベース（マークダウンファイル）からHTMLページ（`public/huntermeigen/index.html` など）を自動生成する際は、以下の手順を必ず踏むこと。

## 1. データの整形・HTML生成
`process_quotes.py` 等のスクリプトを実行し、マークダウンのデータを元に最新のHTMLファイルを `public` フォルダ内に出力する。
この際、名寄せ（重複排除）やソート、星の数などのフォーマット処理をスクリプト内で行う。

## 2. 共通ヘッダーのインジェクション（必須）
全ページのサイトヘッダー（電脳ハンター協会共通ヘッダー）を統一するため、HTML生成直後に必ず以下のスクリプトを実行し、共通ヘッダーのアセット（CSS/JS）をインジェクションすること。

```bash
python3 /Users/yu/Antigravity_workspace/HUNTERHUNTER-FANSITE/inject_shared_header.py
```

※現在、`process_quotes.py` の末尾からこのインジェクション処理を自動で呼び出すように設計されています。スクリプトを改修する際も、このインジェクションの手順を絶対に外さないように注意してください。
