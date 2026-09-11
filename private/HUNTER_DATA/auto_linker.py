import os
import re

def main():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    
    terms = {}
    aliases = {}
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
                    aliases[term] = term
                    
                    # 括弧書きのエイリアス抽出
                    m = re.match(r'^(.+)（(.+)）$', term)
                    if m:
                        base_name = m.group(1).strip()
                        sub_name = m.group(2).strip()
                        if len(base_name) >= 2 and base_name not in aliases:
                            aliases[base_name] = term
                        if len(sub_name) >= 2 and sub_name not in aliases:
                            aliases[sub_name] = term
                    else:
                        base_name = term
                        
                    # 「＝」でのエイリアス抽出
                    if '＝' in base_name:
                        first_name = base_name.split('＝')[0]
                        if len(first_name) >= 2 and first_name not in aliases:
                            aliases[first_name] = term
                            
    # 名前が他の一般名詞と衝突しやすいものを除外する場合はここに書く（今回はとりあえずそのまま）
    # 例： if "王" in aliases: del aliases["王"]
                    
    sorted_alias_keys = sorted(aliases.keys(), key=len, reverse=True)
    
    # スマートなエスケープ（カタカナのみの用語の場合、他のカタカナ文字と隣接している場合はマッチさせない）
    def make_pattern(term):
        if re.fullmatch(r'[ァ-ヶー＝]+', term):
            return r'(?<![ァ-ヶー])' + re.escape(term) + r'(?![ァ-ヶー])'
        return re.escape(term)
        
    escaped_terms = [make_pattern(t) for t in sorted_alias_keys]
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
                
            parts = re.split(r'^(---\n.*?\n---)\n', content, maxsplit=1, flags=re.DOTALL)
            if len(parts) == 3:
                yaml_part = parts[1]
                body = parts[2]
            else:
                yaml_part = ""
                body = content
                
            new_body_lines = []
            for line in body.split('\n'):
                # 既にあるリンクを無視
                segments = re.split(r'(\[[^\]]+\]\([^)]+\))', line)
                for i in range(0, len(segments), 2):
                    plain_text = segments[i]
                    def repl(match):
                        matched_str = match.group(1)
                        if matched_str == current_term: return matched_str
                        full_term = aliases[matched_str]
                        if full_term == current_term: return matched_str
                        rel_path = os.path.relpath(terms[full_term], root)
                        # フルネーム形式でリンクする
                        return f"[{full_term}]({rel_path})"
                        
                    segments[i] = pattern.sub(repl, plain_text)
                    
                new_body_lines.append("".join(segments))
                
            new_content = yaml_part + "\n" + "\n".join(new_body_lines)
            
            if new_content != content:
                with open(filepath, 'w', encoding='utf-8') as file:
                    file.write(new_content)
                modified += 1
            processed += 1
            
    print(f"オートリンク完了 (エイリアス・スマートカタカナ除外適用) スキャン: {processed} / 更新: {modified}")

if __name__ == "__main__":
    main()
