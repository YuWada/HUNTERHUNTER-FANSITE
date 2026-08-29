import os
import re

def main():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    
    terms = {}
    exclude_files = {'index.md', 'README_WIKI_MAINTENANCE.md', '検討中キーワード.md'}
    
    # 1. リンク対象用語の収集
    for root, dirs, files in os.walk(base_dir):
        if "venv" in root or "build_src" in root: 
            continue
        for f in files:
            if f.endswith('.md') and f not in exclude_files:
                term = f[:-3]
                if len(term) >= 2:
                    terms[term] = os.path.join(root, f)
                    
    sorted_term_keys = sorted(terms.keys(), key=len, reverse=True)
    
    # スマートなエスケープ（カタカナのみの用語の場合、他のカタカナ文字と隣接している場合はマッチさせない）
    def make_pattern(term):
        if re.fullmatch(r'[ァ-ヶー＝]+', term):
            return r'(?<![ァ-ヶー])' + re.escape(term) + r'(?![ァ-ヶー])'
        return re.escape(term)
        
    escaped_terms = [make_pattern(t) for t in sorted_term_keys]
    pattern = re.compile(r'(' + '|'.join(escaped_terms) + r')')
    
    processed = 0
    modified = 0
    
    # 2. スキャンと一斉置換
    for root, dirs, files in os.walk(base_dir):
        if "venv" in root or "build_src" in root: 
            continue
        for f in files:
            if not f.endswith('.md') or f in exclude_files:
                continue
                
            filepath = os.path.join(root, f)
            current_term = f[:-3]
            
            with open(filepath, 'r', encoding='utf-8') as file:
                content = file.read()
                
            # 過去の「1文字リンク」や、今回問題になったカタカナの一部リンクを解除する
            # ※ 今回は手動の [ギド](...)ン のようなリンクも事前に消す必要があるため、
            #    メインの実行前にsed等で綺麗にするか、ここで一括処理する。
            
            parts = re.split(r'^(---\n.*?\n---)\n', content, maxsplit=1, flags=re.DOTALL)
            if len(parts) == 3:
                yaml_part = parts[1]
                body = parts[2]
            else:
                yaml_part = ""
                body = content
                
            new_body_lines = []
            for line in body.split('\n'):
                    
                segments = re.split(r'(\[[^\]]+\]\([^)]+\))', line)
                for i in range(0, len(segments), 2):
                    plain_text = segments[i]
                    def repl(match):
                        term = match.group(1)
                        if term == current_term: return term
                        rel_path = os.path.relpath(terms[term], root)
                        return f"[{term}]({rel_path})"
                        
                    segments[i] = pattern.sub(repl, plain_text)
                    
                new_body_lines.append("".join(segments))
                
            new_content = yaml_part + "\n" + "\n".join(new_body_lines)
            
            if new_content != content:
                with open(filepath, 'w', encoding='utf-8') as file:
                    file.write(new_content)
                modified += 1
            processed += 1
            
    print(f"オートリンク完了 (スマートカタカナ除外適用) スキャン: {processed} / 更新: {modified}")

if __name__ == "__main__":
    main()
