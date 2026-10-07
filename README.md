# Inhalte bearbeiten und veröffentlichen

Demo-Website: https://mktcode.github.io/static-website-demo/

## 1. Text ändern

Öffne `content/engineering-principles.md` und klicke auf das **Stift-Symbol** oben rechts. Ändere den Text und prüfe ihn unter **Preview**.

Die Formatierung ist einfach:

```markdown
# Überschrift

Ein Absatz mit **fettem** und *kursivem* Text.
```

## 2. Bild ändern

Öffne den Ordner `content/media` und klicke oben rechts auf **Add file → Upload files**.

Wähle das neue Bild auf deinem Computer aus oder ziehe es in das Upload-Feld. Bei gleichem Dateinamen (z.B. `hero.jpg` wird das bisherige Bild ersetzt.

> Neue Dateien, mit anderen Dateinamen, werden ohne Anpassung der HTML-Datei nicht automatisch auf der Website verwendet.

## 3. Änderung speichern

Klicke auf **Commit changes…** und beschreibe kurz deine Änderung, zum Beispiel „Einleitung überarbeitet“.

### Direkt veröffentlichen

Wähle **Commit directly to the main branch** und bestätige.

Die Änderung wird automatisch nach wenigen Minuten auf der Website veröffentlicht, sofern der Workflow erfolgreich durchläuft.

### Erst prüfen lassen

Wähle **Create a new branch … and start a pull request**. Ein Branch ist eine separate Arbeitsfassung, die noch nicht veröffentlicht wird.

Vergib einen Namen, zum Beispiel `neue-einleitung`, und speichere. Erstelle anschließend über **Create pull request** einen Vorschlag zur Prüfung; das Ziel (**base**) muss `main` sein.

Nach der Prüfung übernimmt die zuständige Person den Vorschlag mit **Merge pull request**. Erst dann startet die Veröffentlichung.
