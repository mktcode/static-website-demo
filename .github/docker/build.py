"""Build localized Markdown pages into /<locale>/<slug>/ (index -> /<locale>/)."""

from html import escape
from pathlib import Path
import posixpath
import re
import shutil
from urllib.parse import quote

import markdown
import yaml

LOCALES = ("en", "de")
DEFAULT_LOCALE = "en"
COPY = {
    "en": {
        "home": "Home", "navigation_label": "Main navigation", "language_label": "Language",
        "hero_alt": "Aerial view of a building with rooftop solar panels",
        "hero_button": "find out more",
        "hero_copy": "Not every surgical challenge can be solved with the same implant.<br>We believe every indication deserves a solution engineered for its specific clinical requirements.<br>It’s the philosophy on which DynaMesh® was built—and one that continues to drive us today.",
    },
    "de": {
        "home": "Startseite", "navigation_label": "Hauptnavigation", "language_label": "Sprache",
        "hero_alt": "Luftaufnahme eines Gebäudes mit Solaranlage auf dem Dach",
        "hero_button": "mehr erfahren",
        "hero_copy": "Nicht jede chirurgische Herausforderung lässt sich mit demselben Implantat lösen.<br>Wir glauben, dass jede Indikation eine Lösung verdient, die für ihre spezifischen klinischen Anforderungen entwickelt wurde.<br>Auf dieser Philosophie wurde DynaMesh® aufgebaut – und sie treibt uns bis heute an.",
    },
}


def read_page(source):
    text = source.read_text(encoding="utf-8")
    match = re.fullmatch(r"---\r?\n(.*?)\r?\n---\r?\n(.*)", text, re.DOTALL)
    if not match:
        raise ValueError(f"Missing YAML front matter: {source}")
    data = yaml.safe_load(match[1])
    if not isinstance(data, dict) or not isinstance(data.get("title"), str) or not data["title"].strip():
        raise ValueError(f"Missing title: {source}")
    if not match[2].strip():
        raise ValueError(f"Missing content: {source}")
    for field in ("hero_image", "hero_alt"):
        if data.get(field) is not None and not isinstance(data[field], str):
            raise ValueError(f"Invalid {field}: {source}")
    return {
        "title": data["title"], "body": match[2],
        "hero_image": (data.get("hero_image") or "").strip(),
        # None means absent: preserve the existing alt text for the default image.
        "hero_alt": data.get("hero_alt"),
    }


def hero_values(root, page, locale, current):
    # Sveltia may store root-relative URLs even with a relative public_folder.
    # Remove exactly one slash; protocol-relative URLs (//host/...) stay invalid.
    image = (page["hero_image"] or "content/media/hero.jpg").removeprefix("/")
    parts = image.split("/")
    if parts[:2] != ["content", "media"] or any(part in ("", ".", "..") for part in parts):
        raise ValueError(f"Hero image must be inside content/media: {image}")
    media = (root / "content/media").resolve()
    source = (root / image).resolve()
    if not source.is_relative_to(media) or not source.is_file():
        raise ValueError(f"Missing or invalid hero image: {image}")
    alt = page["hero_alt"]
    if alt is None:
        alt = COPY[locale]["hero_alt"] if image == "content/media/hero.jpg" else ""
    return {
        "hero_image": escape(quote(posixpath.relpath(image, current), safe="/")),
        "hero_alt": escape(alt),
    }


def route(locale, slug):
    return f"{locale}/" if slug == "index" else f"{locale}/{slug}/"


def relative_url(target, current):
    return posixpath.relpath(target, current) + "/"


def build(root=Path(".")):
    output = root / "_site"
    template = (root / "index.html").read_text(encoding="utf-8")
    pages = {}
    for locale in LOCALES:
        for source in sorted((root / "content" / "pages" / locale).glob("*.md")):
            slug = source.stem
            if not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", slug):
                raise ValueError(f"Invalid slug: {source}")
            pages[locale, slug] = read_page(source)
        if (locale, "index") not in pages:
            raise ValueError(f"Missing homepage for {locale}")

    if output.exists():
        shutil.rmtree(output)
    output.mkdir()
    for (locale, slug), page in pages.items():
        current = route(locale, slug)
        home = relative_url(route(locale, "index"), current)
        nav = [f'<a href="{home}">{COPY[locale]["home"]}</a>']
        for (lang, key), item in pages.items():
            if lang == locale and key != "index":
                href = relative_url(route(lang, key), current)
                nav.append(f'<a href="{href}">{escape(item["title"])}</a>')
        switches, alternates = [], []
        for lang in LOCALES:
            if (lang, slug) in pages:
                href = relative_url(route(lang, slug), current)
                alternates.append(f'<link rel="alternate" hreflang="{lang}" href="{href}">')
                active = ' aria-current="page"' if lang == locale else ""
                switches.append(f'<a href="{href}" hreflang="{lang}" lang="{lang}"{active}>{lang.upper()}</a>')
        media_root = posixpath.relpath("content/media", current)
        body = markdown.markdown(page["body"], extensions=["extra", "sane_lists"], output_format="html")
        # CMS image URLs are relative to the shared media folder, not the page route.
        body = re.sub(r'((?:src|href)=")/?content/media/', lambda m: m[1] + media_root + "/", body)
        values = {
            **COPY[locale], "locale": locale, "page_title": escape(page["title"]),
            "page_content": body, "home_href": home, "media_root": media_root,
            **hero_values(root, page, locale, current),
            "navigation": "\n      ".join(nav), "language_switch": " ".join(switches),
            "alternate_links": "\n  ".join(alternates),
        }
        def substitute(match):
            if match[1] not in values:
                raise ValueError(f"Unknown template placeholder: {match[1]}")
            return values[match[1]]
        html = re.sub(r"\{\{\s*([a-zA-Z0-9_]+)\s*\}\}", substitute, template)
        target = output / current / "index.html"
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(html, encoding="utf-8")

    (output / "index.html").write_text(
        '<!doctype html><html lang="en"><head><meta charset="utf-8">'
        f'<meta http-equiv="refresh" content="0; url={DEFAULT_LOCALE}/">'
        '<meta name="robots" content="noindex, nofollow">'
        '<title>DynaMesh</title></head><body>'
        f'<a href="{DEFAULT_LOCALE}/">Continue / Weiter</a></body></html>\n', encoding="utf-8",
    )
    # Allow fetching so crawlers can read the noindex meta tags. A robots.txt
    # under a GitHub Pages project path is not authoritative for the domain.
    (output / "robots.txt").write_text(
        "# Demo: indexing is disabled by robots meta tags in every HTML page.\n"
        "# Allow fetching so crawlers can read those tags.\n"
        "User-agent: *\nAllow: /\n", encoding="utf-8",
    )
    (output / ".nojekyll").touch()
    shutil.copytree(root / "content" / "media", output / "content" / "media")


if __name__ == "__main__":
    build()
