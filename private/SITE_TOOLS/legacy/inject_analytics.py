import os
import re
from pathlib import Path

# 旧方式の保管用スクリプトです。現在のGA4は public/shared/site-header.js から読み込みます。
# 通常は実行せず、過去の処理を確認する場合だけ参照してください。

# =============== 設定 ===============
# Googleアナリティクスで取得した「測定ID（G-XXXXXXXXXX）」をここに設定してください。
MEASUREMENT_ID = 'G-FJMHVLKN37'
# ====================================

# 移動後も参照先を解決できるよう、プロジェクトルートからpublicを指定します。
PROJECT_ROOT = Path(__file__).resolve().parents[3]
PUBLIC_DIR = str(PROJECT_ROOT / 'public')

def get_ga_snippet(measurement_id):
    # Google Analytics 4 (GA4) の標準的なタグスニペット
    return f"""
    <!-- Google tag (gtag.js) -->
    <script async src="https://www.googletagmanager.com/gtag/js?id={measurement_id}"></script>
    <script>
      window.dataLayer = window.dataLayer || [];
      function gtag(){{dataLayer.push(arguments);}}
      gtag('js', new Date());

      gtag('config', '{measurement_id}');
    </script>
"""

def inject_to_file(filepath, measurement_id):
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
            
        # すでにタグが含まれているかチェック（二重登録防止）
        # gtag.jsのURLが含まれているかで判定します
        if f"googletagmanager.com/gtag/js" in content:
            print(f"スキップ (既にタグが存在します): {filepath}")
            return

        # </head> タグを探して、その直前にスニペットを挿入する
        snippet = get_ga_snippet(measurement_id)
        
        if not re.search(r'</head>', content, re.IGNORECASE):
            print(f"スキップ (</head>タグが見つかりません): {filepath}")
            return

        # 正規表現で </head> の直前にタグを挿入
        new_content = re.sub(r'(</head>)', f"{snippet}\\1", content, count=1, flags=re.IGNORECASE)

        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
            
        print(f"更新完了: {filepath}")
        
    except Exception as e:
        print(f"エラー発生 ({filepath}): {e}")

def main():
    if MEASUREMENT_ID == 'G-XXXXXXXXXX' or not MEASUREMENT_ID:
        print("【注意】MEASUREMENT_IDが設定されていません。")
        print("スクリプト（inject_analytics.py）の6行目にある 'G-XXXXXXXXXX' を、実際の測定IDに書き換えてから実行してください。")
        return

    print("Googleアナリティクスタグの挿入処理を開始します...")
    
    html_files_count = 0
    for root, dirs, files in os.walk(PUBLIC_DIR):
        for file in files:
            if file.endswith('.html'):
                html_files_count += 1
                filepath = os.path.join(root, file)
                inject_to_file(filepath, MEASUREMENT_ID)

    print(f"\n処理完了! (チェックしたHTMLファイル数: {html_files_count})")

if __name__ == '__main__':
    main()
