# Mehrsprachige DynaMesh-Website

Website: https://mktcode.github.io/static-website-demo/

Redaktion: https://admin.feg.mktco.de/

## Seiten und Sprachen

| Inhaltsdatei | URL relativ zur Website |
| --- | --- |
| `content/pages/en/index.md` | `/en/` |
| `content/pages/de/index.md` | `/de/` |
| `content/pages/en/about.md` | `/en/about/` |
| `content/pages/de/about.md` | `/de/about/` |

Der Website-Einstieg leitet auf `en/` weiter. Auf GitHub Pages steht vor diesen Pfaden weiterhin `/static-website-demo`. Alle Navigations- und Medienlinks sind relativ, sodass derselbe Build auch unter einer eigenen Domain oder als Dokploy-Preview funktioniert.

## Im CMS bearbeiten

1. **Seiten** öffnen und einen vorhandenen Eintrag bearbeiten oder eine **neue Seite** anlegen.
2. Titel und Markdown-Inhalt in Englisch und Deutsch eingeben. Übersetzungen sind im selben CMS-Eintrag verknüpft; der Dateiname/Slug ist in beiden Sprachen gleich.
3. Speichern und zur Prüfung senden. Der Editorial Workflow erstellt einen Pull Request gegen `main`.
4. Nach Review veröffentlichen. Erst der Merge nach `main` löst den Pages-Build aus.

Alle veröffentlichten Seiten werden automatisch in der Navigation ihrer Sprache verlinkt. Der Sprachwechsel führt zur entsprechenden Übersetzung; fehlt sie, wird kein Link auf eine nicht existierende Seite angezeigt. Neue Übersetzungen werden zunächst angeboten, können im CMS aber deaktiviert werden.

Die Hauptüberschrift kommt aus dem Feld **Titel**. Im Markdown-Inhalt deshalb mit `##` beginnen. Die Startseiten heißen fest **`index`**: nicht umbenennen oder entfernen. CMS-Löschungen sind für die Collection deaktiviert, damit die Startseiten nicht versehentlich gelöscht werden. Andere Seiten können mit einem geprüften GitHub-PR entfernt werden.

## Direkt in GitHub bearbeiten

Die Seiten enthalten YAML Front Matter und Markdown:

```markdown
---
title: Über uns
---

Hier steht ein Absatz mit **fettem** und *kursivem* Text.

## Weitere Informationen
```

Neue Seiten als `content/pages/en/<slug>.md` und gegebenenfalls `content/pages/de/<slug>.md` anlegen. Slugs: Kleinbuchstaben, Zahlen und Bindestriche. Änderungen über einen Branch und Pull Request gegen `main` prüfen lassen.

**Migration:** `content/engineering-principles.md` bleibt als historische Datei erhalten, wird aber nicht mehr gerendert. Offene CMS-PRs für diese alte Datei vor dem Merge prüfen und deren Inhalte gegebenenfalls in die neuen `index.md`-Dateien übertragen. Die englische Startseite wurde aus dem aktuellen `main` übernommen; die deutsche Übersetzung ist ein initialer Entwurf und sollte fachlich geprüft werden.

## Bilder und Layout

Gemeinsame Medien liegen in `content/media`. Markdown-Bilder verwenden beispielsweise `![Beschreibung](content/media/bild.jpg)`; der Build passt den Pfad an die Seitentiefe an. Das CMS schreibt genau solche relativen Medienpfade.

Der Hero verwendet weiterhin fest `content/media/hero.jpg`. Dessen Austausch und Layoutänderungen erfolgen über GitHub. Die separate CMS-Medienbibliothek schreibt direkt nach `main`, nicht über den Editorial Workflow; für geprüfte Uploads den Inhaltseditor verwenden.

Alle Seiten verwenden die gemeinsame Vorlage `index.html` inklusive Hero und Footer. Hero-Texte, Navigation und Sprachsteuerung sind übersetzt. Die Produktnamen und der ausdrücklich deutsch markierte Footer bleiben gemeinsam/statisch. Weitere Sprachen müssen in CMS-Konfiguration und `LOCALES`/`COPY` in `.github/docker/build.py` ergänzt werden.

## Build und Tests

```sh
docker build -f .github/docker/Dockerfile -t dynamesh-website .
docker run --rm -p 8080:80 dynamesh-website
# http://localhost:8080/en/ und http://localhost:8080/de/
```

Der Docker-Build führt sieben Regressionstests aus, bevor er die Website generiert. Der bestehende GitHub-Pages-Workflow nutzt dasselbe Dockerfile. Ungültige Slugs, fehlende Titel, leere Inhalte und fehlende Startseiten lassen den Build fehlschlagen.
