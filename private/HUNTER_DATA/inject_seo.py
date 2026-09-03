import os
import re
import yaml
from pathlib import Path

def inject_seo_tags():
    base_dir = Path(__file__).resolve().parent
    public_dir = base_dir.parent.parent / "public" / "hunterdata2"
    
    categories = ["登場人物", "ストーリー", "念能力", "用語集", "グリードアイランド_カード"]
    
    injected_count = 0
    
    for category in categories:
        cat_path = base_dir / category
        if not cat_path.exists(): 
            continue
            
        for md_file in cat_path.rglob("*.md"):
            # Calculate the relative path from base_dir to the markdown file
            rel_path = md_file.relative_to(base_dir)
            
            # The HTML file path depends on MkDocs directory URLs behavior
            if md_file.name == "index.md":
                html_path = public_dir / rel_path.parent / "index.html"
            else:
                html_path = public_dir / rel_path.parent / md_file.stem / "index.html"
                
            if not html_path.exists():
                continue
                
            # Parse YAML frontmatter
            content = md_file.read_text(encoding="utf-8")
            parts = re.split(r'^---\n', content, maxsplit=2, flags=re.MULTILINE)
            
            meta = {}
            if len(parts) >= 3:
                try:
                    meta = yaml.safe_load(parts[1])
                except Exception:
                    pass
            
            title = meta.get("title", md_file.stem) if meta else md_file.stem
            desc = meta.get("description", "HUNTER×HUNTER 神眼データベース") if meta else "HUNTER×HUNTER 神眼データベース"
            
            # Read generated HTML
            html_content = html_path.read_text(encoding="utf-8")
            
            # Skip if already injected
            if 'property="og:title"' in html_content:
                continue
                
            seo_tags = f"""
    <!-- SEO tags injected from OKF (Markdown) frontmatter -->
    <meta property="og:title" content="{title}">
    <meta property="og:description" content="{desc}">
    <meta property="og:type" content="article">
    <meta property="og:site_name" content="HUNTER×HUNTER 神眼データベース">
    <meta name="twitter:card" content="summary">
    <meta name="twitter:title" content="{title}">
    <meta name="twitter:description" content="{desc}">
"""
            # Insert before </head>
            if "</head>" in html_content:
                html_content = html_content.replace("</head>", f"{seo_tags}</head>")
                html_path.write_text(html_content, encoding="utf-8")
                injected_count += 1
                
    print(f"SEO tags injected in {injected_count} HTML files in hunterdata2.")

if __name__ == "__main__":
    inject_seo_tags()
