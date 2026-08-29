#!/usr/bin/env python3
"""Add the shared Denno Hunter Association header assets to every public HTML file."""

from pathlib import Path
import os
import re


ROOT = Path(__file__).resolve().parent
PUBLIC = ROOT / "public"
CSS = PUBLIC / "shared" / "site-header.css"
JS = PUBLIC / "shared" / "site-header.js"
MARKER = "data-denno-shared-header"
GA_PATTERN = re.compile(
    r"\s*<!-- Google tag \(gtag\.js\) -->\s*"
    r'<script async src="https://www\.googletagmanager\.com/gtag/js\?id=G-FJMHVLKN37"></script>\s*'
    r"<script>.*?gtag\('config', 'G-FJMHVLKN37'\);\s*</script>",
    re.DOTALL,
)


def relative_url(target: Path, page: Path) -> str:
    return Path(os.path.relpath(target, page.parent)).as_posix()


def inject(page: Path) -> bool:
    source = page.read_text(encoding="utf-8")
    updated = GA_PATTERN.sub("", source)

    if MARKER in updated:
        if updated == source:
            return False
        page.write_text(updated, encoding="utf-8")
        return True

    assets = (
        f'  <link rel="stylesheet" href="{relative_url(CSS, page)}" {MARKER}>\n'
        f'  <script defer src="{relative_url(JS, page)}" {MARKER}></script>\n'
    )
    updated, replacements = re.subn(r"\s*</head>", f"\n{assets}</head>", updated, count=1)
    if replacements != 1:
        raise RuntimeError(f"Could not find </head> in {page}")
    page.write_text(updated, encoding="utf-8")
    return True


def main() -> None:
    pages = sorted(PUBLIC.rglob("*.html"))
    changed = sum(inject(page) for page in pages)
    print(f"Shared header registered in {changed} of {len(pages)} HTML files.")


if __name__ == "__main__":
    main()
