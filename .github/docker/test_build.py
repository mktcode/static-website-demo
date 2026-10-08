"""Run with: python -m unittest discover -s .github/docker -p 'test_*.py'."""

from pathlib import Path
import shutil
import tempfile
import unittest

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
