#!/usr/bin/env python3
"""Add the shared Denno Hunter Association header assets to every public HTML file."""

from pathlib import Path
import os

ROOT = Path(__file__).resolve().parent
PUBLIC = ROOT / "public"
CSS = PUBLIC / "shared" / "site-header.css"
JS = PUBLIC / "shared" / "site-header.js"
FAVICON = PUBLIC / "shared" / "favicon.svg"
MARKER = "data-denno-shared-header"

def relative_url(target: Path, page: Path) -> str:
    return Path(os.path.relpath(target, page.parent)).as_posix()

def inject(page: Path) -> bool:
    source = page.read_text(encoding="utf-8")
    
    # Fast path: already injected?
    if MARKER in source:
        return False
        
    assets = (
        f'  <link rel="icon" type="image/svg+xml" href="{relative_url(FAVICON, page)}">\n'
        f'  <link rel="stylesheet" href="{relative_url(CSS, page)}" {MARKER}>\n'
        f'  <script defer src="{relative_url(JS, page)}" {MARKER}></script>\n'
    )
    
    if "</head>" not in source:
        raise RuntimeError(f"Could not find </head> in {page}")
        
    updated = source.replace("</head>", f"\n{assets}</head>")
    page.write_text(updated, encoding="utf-8")
    return True

def main() -> None:
    pages = sorted(PUBLIC.rglob("*.html"))
    changed = sum(inject(page) for page in pages)
    print(f"Shared header registered in {changed} of {len(pages)} HTML files.")

if __name__ == "__main__":
    main()
