"""Run with: python -m unittest discover -s .github/docker -p 'test_*.py'."""

from pathlib import Path
import shutil
import tempfile
import unittest

import yaml

from build import build


class BuildTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        shutil.copy("index.html", self.root / "index.html")
        shutil.copytree("content", self.root / "content")

    def page(self, locale, slug, title="Test"):
        path = self.root / "content" / "pages" / locale / f"{slug}.md"
        path.write_text(f'---\ntitle: "{title}"\n---\n\nText **bold**.\n\n![Image](content/media/hero.jpg)\n', encoding="utf-8")

    def test_homepages(self):
        build(self.root)
        output = self.root / "_site"
        self.assertIn('url=en/', (output / "index.html").read_text())
        for locale in ("en", "de"):
            html = (output / locale / "index.html").read_text()
            self.assertIn(f'<html lang="{locale}">', html)
            self.assertIn('src="../content/media/hero.jpg"', html)
            self.assertNotIn("{{", html)
        self.assertTrue((output / "content/media/hero.jpg").is_file())

    def test_new_pages_and_translation_links(self):
        self.page("en", "about", "About &amp; more")
        self.page("de", "about", "Über uns")
        build(self.root)
        html = (self.root / "_site/en/about/index.html").read_text()
        self.assertIn('href="../../de/about/"', html)
        self.assertIn('href="../"', html)
        self.assertIn('src="../../content/media/hero.jpg"', html)
        self.assertIn('<strong>bold</strong>', html)
        self.assertIn('About &amp;amp; more', html)
        home = (self.root / "_site/de/index.html").read_text()
        self.assertIn('href="about/"', home)
        self.assertIn("Über uns", home)

    def set_hero(self, locale, slug, **fields):
        path = self.root / "content/pages" / locale / f"{slug}.md"
        header, body = path.read_text().split("---\n", 2)[1:]
        data = yaml.safe_load(header)
        data.update(fields)
        path.write_text("---\n" + yaml.safe_dump(data, allow_unicode=True) + "---\n" + body)

    def test_localized_hero_images(self):
        self.page("en", "localized")
        self.page("de", "localized")
        for locale in ("en", "de"):
            name = f"hero {locale}.jpg"
            shutil.copy(self.root / "content/media/hero.jpg", self.root / "content/media" / name)
            self.set_hero(locale, "localized", hero_image=f"content/media/{name}", hero_alt=f'Image "{locale}" & text')
        build(self.root)
        for locale in ("en", "de"):
            html = (self.root / "_site" / locale / "localized/index.html").read_text()
            self.assertIn(f'src="../../content/media/hero%20{locale}.jpg"', html)
            self.assertIn(f'alt="Image &quot;{locale}&quot; &amp; text"', html)
            self.assertTrue((self.root / "_site/content/media" / f"hero {locale}.jpg").is_file())

    def test_empty_image_falls_back_and_empty_alt_is_preserved(self):
        self.set_hero("en", "index", hero_image="", hero_alt="")
        self.set_hero("de", "index", hero_image=None, hero_alt=None)
        build(self.root)
        english = (self.root / "_site/en/index.html").read_text()
        german = (self.root / "_site/de/index.html").read_text()
        self.assertIn('src="../content/media/hero.jpg" alt=""', english)
        self.assertIn('alt="Luftaufnahme', german)

    def test_missing_hero_image_rejected(self):
        self.set_hero("en", "index", hero_image="content/media/missing.jpg")
        with self.assertRaisesRegex(ValueError, "Missing or invalid hero image"):
            build(self.root)

    def test_hero_image_outside_media_rejected(self):
        for image in ("content/media/../pages/en/index.md", "https://example.com/image.jpg"):
            with self.subTest(image=image):
                self.set_hero("en", "index", hero_image=image)
                with self.assertRaisesRegex(ValueError, "must be inside content/media"):
                    build(self.root)

    def test_invalid_hero_field_types_rejected(self):
        for fields in ({"hero_image": ["content/media/hero.jpg"]}, {"hero_image": "", "hero_alt": 123}):
            with self.subTest(fields=fields):
                self.set_hero("en", "index", **fields)
                with self.assertRaisesRegex(ValueError, "Invalid hero_"):
                    build(self.root)

    def test_missing_translation_not_linked(self):
        self.page("en", "english-only")
        build(self.root)
        html = (self.root / "_site/en/english-only/index.html").read_text()
        self.assertNotIn('hreflang="de"', html)

    def test_rebuild_removes_stale_pages(self):
        self.page("en", "removed")
        build(self.root)
        (self.root / "content/pages/en/removed.md").unlink()
        build(self.root)
        self.assertFalse((self.root / "_site/en/removed").exists())

    def test_missing_homepage_rejected(self):
        (self.root / "content/pages/de/index.md").unlink()
        with self.assertRaisesRegex(ValueError, "Missing homepage"):
            build(self.root)

    def test_missing_title_rejected(self):
        (self.root / "content/pages/en/index.md").write_text('---\nother: field\n---\nText')
        with self.assertRaisesRegex(ValueError, "Missing title"):
            build(self.root)

    def test_invalid_slug_rejected(self):
        self.page("en", "UPPER")
        with self.assertRaisesRegex(ValueError, "Invalid slug"):
            build(self.root)


if __name__ == "__main__":
    unittest.main()
