"""Render the website from index.html and content/*.md."""

from pathlib import Path
import re
import shutil

import markdown


content = Path("content")
output = Path("_site")
output.mkdir()
template = Path("index.html").read_text(encoding="utf-8")


def render(match):
    source = content / f"{match.group(1)}.md"
    if not source.is_file():
        raise FileNotFoundError(f"Missing Markdown file: {source}")
    return markdown.markdown(
        source.read_text(encoding="utf-8"),
        extensions=["extra", "sane_lists"],
        output_format="html",
    )


html = re.sub(r"\{\{\s*([a-zA-Z0-9_-]+)\s*\}\}", render, template)
if "{{" in html or "}}" in html:
    raise ValueError("Unresolved template placeholder in generated HTML")

(output / "index.html").write_text(html, encoding="utf-8")
shutil.copytree(content / "media", output / "content" / "media")
