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
                # 【変更点】1文字の用語（絶、円、凝など）はリンク化対象から除外
                if len(term) >= 2:
                    terms[term] = os.path.join(root, f)
                    
    sorted_term_keys = sorted(terms.keys(), key=len, reverse=True)
    escaped_terms = [re.escape(t) for t in sorted_term_keys]
    pattern = re.compile(r'(' + '|'.join(escaped_terms) + r')')
    
    processed = 0
    modified = 0
    
    # 2. スキャンと一斉置換
    for root, dirs, files in os.walk(base_dir):
        if "venv" in root or "build_src" in root: 
            continue
        for f in files:
            if not f.endswith('.md'):
                continue
                
            filepath = os.path.join(root, f)
            current_term = f[:-3]
            
            with open(filepath, 'r', encoding='utf-8') as file:
                content = file.read()
                
            # 【変更点】過去に作られてしまった「1文字のリンク（例：[絶](...)）」を解除してプレーンテキストに戻す
            content = re.sub(r'\[(.)\]\([^)]+\)', r'\1', content)
            
            parts = re.split(r'^(---\n.*?\n---)\n', content, maxsplit=1, flags=re.DOTALL)
            if len(parts) == 3:
                yaml_part = parts[1]
                body = parts[2]
            else:
                yaml_part = ""
                body = content
                
            new_body_lines = []
            for line in body.split('\n'):
                if line.startswith('#'):
                    new_body_lines.append(line)
                    continue
                    
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
            
    print(f"オートリンク完了 (1文字の単語を除外済) スキャン: {processed} / 更新: {modified}")

if __name__ == "__main__":
    main()
