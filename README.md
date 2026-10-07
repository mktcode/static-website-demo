# Website-Inhalte bearbeiten – Anleitung für die Redaktion

Du kannst die Texte dieser Website direkt im Browser auf GitHub ändern. Du brauchst dafür weder ein Programm zu installieren noch Git zu kennen.

**Du benötigst:** ein GitHub-Konto und die Berechtigung, dieses Projekt zu bearbeiten. Falls dir die unten beschriebenen Schaltflächen fehlen, frage die Person, die das Projekt betreut.

## Wo finde ich den Text?

1. Öffne das Projekt: [static-website-demo auf GitHub](https://github.com/mktcode/static-website-demo).
2. Wähle links oberhalb der Dateiliste den Eintrag **main** aus, falls dort etwas anderes steht. Das ist die veröffentlichte Fassung.
3. Öffne den Ordner **content**.
4. Klicke auf **engineering-principles.md**. Diese Datei enthält die Überschrift und den Text des Abschnitts „Engineering Principles“.
5. Klicke oben rechts im Dateibereich auf das **Stift-Symbol** („Edit this file“).

Du kannst jetzt den Text im Eingabefeld bearbeiten. Die Datei `index.html` und den Ordner `.github` musst du für diese Textänderung **nicht** anfassen: Sie enthalten das Layout und die automatische Veröffentlichung.

> Diese Anleitung gilt für den Abschnitt „Engineering Principles“. Andere Texte der Website, etwa der Text über dem großen Bild, sind derzeit noch nicht in einer eigenen Textdatei hinterlegt.

## Beispiel: einen Satz ändern

Die Textdatei verwendet **Markdown**. Das ist normaler Text mit wenigen Zeichen für Überschriften und Hervorhebungen:

```markdown
# Engineering Principles

Every DynaMesh® implant begins with a clinical challenge—but **every solution is shaped by the same engineering principles**.
```

Du könntest den Absatz beispielsweise so ändern:

```markdown
# Engineering Principles

Every DynaMesh® implant is designed for a specific clinical challenge. **Patient needs guide our engineering decisions.**
```

Die wichtigsten Schreibweisen:

| Eingabe | Bedeutung |
| --- | --- |
| `# Engineering Principles` | Große Überschrift; das Leerzeichen nach `#` ist wichtig |
| `**wichtiger Text**` | **Fetter Text** |
| `*betonter Text*` | *Kursiver Text* |
| Leerzeile zwischen Texten | Neuer Absatz |
| `[Linktext](https://example.com)` | Anklickbarer Link |

Behalte die Überschrift und die Formatierungszeichen bei, sofern du sie nicht bewusst ändern möchtest. Die drei Backticks, die hier die Beispiele einrahmen, gehören **nicht** in deine Textdatei.

Über **Preview** kannst du dir die Formatierung ansehen. Das ist eine Vorschau des Textes, nicht des vollständigen Website-Layouts.

## Weg A: direkt veröffentlichen

**Nutze diesen Weg nur, wenn die Änderung ohne weitere Freigabe online gehen darf.**

1. Klicke nach der Bearbeitung auf **Commit changes…**.
2. Gib eine kurze Beschreibung ein, zum Beispiel: `Einleitung der Engineering Principles überarbeitet`.
3. Wähle **Commit directly to the main branch**. Das bedeutet: „In der veröffentlichten Fassung speichern“.
4. Bestätige mit **Commit changes**.

Damit ist deine Änderung gespeichert und die automatische Veröffentlichung startet. Nach einem erfolgreichen Durchlauf ist sie in der Regel innerhalb weniger Minuten auf der Website sichtbar.

**Achtung:** Du bekommst keine weitere redaktionelle Freigabeabfrage. Dieser Weg veröffentlicht direkt.

Falls GitHub die direkte Speicherung auf `main` nicht erlaubt, verwende **Weg B**. Das kann eine bewusst eingerichtete Schutzregel sein.

## Weg B: Änderung zur Prüfung einreichen

**Nutze diesen Weg, wenn jemand den Text vor der Veröffentlichung prüfen soll.**

1. Klicke nach der Bearbeitung auf **Commit changes…**.
2. Gib eine kurze Beschreibung ein, zum Beispiel: `Vorschlag für neue Einleitung`.
3. Wähle **Create a new branch for this commit and start a pull request**.
4. Gib dem Branch einen kurzen Namen, zum Beispiel `text-engineering-principles`. Falls der Name bereits vergeben ist, ergänze etwa ein Datum.
5. Bestätige das Speichern. Je nach GitHub-Ansicht heißt die Schaltfläche **Propose changes** oder **Commit changes**.
6. GitHub führt dich zur Erstellung eines **Pull Requests**. Falls zunächst eine Vergleichsseite erscheint, klicke dort auf **Create pull request**.
7. Prüfe, dass als Ziel (**base**) `main` und als Vorschlag (**compare**) dein neuer Branch ausgewählt sind.
8. Gib einen verständlichen Titel und eine kurze Erklärung ein: Was hast du geändert, und warum?
9. Klicke auf **Create pull request**. Informiere die zuständige Person oder wähle sie unter **Reviewers** aus, wenn diese Auswahl verfügbar ist.

**Dein Text ist jetzt noch nicht veröffentlicht.** Ein Branch ist eine separate Arbeitsfassung. Ein Pull Request ist die Bitte, diese Arbeitsfassung zu prüfen und in die veröffentlichte Fassung zu übernehmen.

Die prüfende Person kann Rückfragen stellen oder Änderungen wünschen. Antworten könnt ihr direkt im Pull Request über Kommentare austauschen.

### Nach der Freigabe

Die zuständige Person übernimmt den Vorschlag über **Merge pull request** und bestätigt die Übernahme. Je nach Projekteinstellungen kann die Schaltfläche auch **Squash and merge** oder **Rebase and merge** heißen.

Erst mit dieser Übernahme nach `main` startet die Veröffentlichung. Ein Kommentar wie „Freigegeben“ oder eine bestätigte Prüfung allein veröffentlicht den Text noch nicht.

> Der Workflow erstellt für einen Pull Request derzeit keine separate Website-Vorschau. Du kannst dort die Textänderungen vergleichen, aber keine fertige Vorschau-Website öffnen.

## Wie erkenne ich, ob die Veröffentlichung geklappt hat?

1. Öffne im Projekt den Reiter **Actions**.
2. Klicke auf den neuesten Durchlauf von **Build and deploy GitHub Pages**, der zu deiner Änderung gehört.
3. Warte, bis die Schritte **build** und **deploy** erfolgreich abgeschlossen sind.
   - **Grün:** erfolgreich.
   - **Gelb / in Bearbeitung:** bitte noch warten.
   - **Rot:** fehlgeschlagen; informiere die technische Betreuung und schicke den Link zum Durchlauf mit.
4. Die Website-Adresse findest du nach erfolgreicher Veröffentlichung in der Zusammenfassung des Durchlaufs beim Deployment. Alternativ findest du sie auf der Projektstartseite unter **Deployments → github-pages**.
5. Öffne die Website und lade sie neu. Prüfe die geänderte Stelle.

Die ursprüngliche `index.html` auf GitHub enthält weiterhin einen Platzhalter für den Text. Das ist beabsichtigt: Erst bei der Veröffentlichung wird der Inhalt der Markdown-Datei automatisch eingesetzt.

## Kleine Begriffshilfe

| GitHub-Begriff | Einfach erklärt |
| --- | --- |
| Repository / Projekt | Der gemeinsame Ordner für diese Website auf GitHub |
| `main` | Die Fassung, aus der die Website veröffentlicht wird |
| Branch | Eine separate Arbeitsfassung für einen Änderungsvorschlag |
| Commit | Eine gespeicherte Änderung mit kurzer Beschreibung |
| Pull Request | Eine Bitte, einen Änderungsvorschlag zu prüfen und zu übernehmen |
| Merge | Einen Vorschlag in die veröffentlichte Fassung übernehmen |
| Actions / Workflow | Die Automatik, die aus den Textdateien die Website erstellt und veröffentlicht |

## Wenn etwas schiefgeht

- **Noch nicht gespeichert?** Verlasse die Bearbeitung ohne „Commit changes“, um deinen Entwurf zu verwerfen.
- **Vorschlag soll nicht übernommen werden?** Schließe den Pull Request über **Close pull request**, statt ihn zu übernehmen. Dadurch wird er nicht veröffentlicht.
- **Fehler bereits veröffentlicht?** Korrigiere die Textdatei erneut über Weg A oder B. Eine neue Änderung kann den Fehler beheben.
- **Unsicher oder Fehlermeldung?** Bitte die technische Betreuung um Hilfe. Ändere nicht auf Verdacht den Workflow oder die HTML-Datei.
