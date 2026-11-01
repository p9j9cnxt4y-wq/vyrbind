# VyrBind – Deutsch

> **VyrBind-Umbenennung (lokaler Kandidat, unveröffentlicht):**
> Die private CI-Prüfung 9/9 betrifft den vorherigen Commit
> `d9490644694d108d85a844ed1d9efeb72c64176c` unter altem Paketnamen. Für diese umbenannten
> Dateien wurde noch keine GitHub-CI ausgeführt. Keine vollständige
> Plattform- oder Sicherheitsfreigabe. Siehe RELEASE_EVIDENCE.md.


Projekt- und Herausgebermarke: **vYronFORGE.**

Copyright (c) 2026 vYronFORGE.

Die öffentliche Kennzeichnung verwendet die Marke und behauptet keine Rechtsform.
Unabhängige Referenz; kein OpenAI-Produkt und keine Betriebssystem-Sandbox.

**Technische Referenzimplementierung für deterministische Sicherheitsgrenzen von KI-Agenten.**

Geltungsbereich: **v0.1.0 / experimentelle lokale Referenz / nicht sicherheitszertifiziert**.

VyrBind setzt nicht bloß einen Systemprompt ein, sondern prüft
Aktionen vor der lokalen Ausführung anhand eines vorab vom Host gebundenen
Run-/Scope-Vertrags. Das Modell darf diesen Vertrag nicht erzeugen oder
verändern. Der technische Code erzwingt **genau eine** lokale Operation:
die Erstellung einer neuen `.txt`-Datei direkt im gebundenen Workspace.

Unterstützt: striktes Eingabeschema, Dateinamen-Allowlist, keine Überschreibung,
Readback mit SHA-256, Erkennung unverzeichneter/alterierter Dateien,
SQLite-Evidence-Kette, Stop bei unbekannter Wirkung und Negativtests.

**Nicht implementiert:** menschliche Identitätsprüfung, eigenständige
Approval-Ausstellung, System-/Sandbox-Isolation, Netzwerkfirewall, Cloud-Deploy,
Secrets-Broker, selbstständige Wahrheitsprüfung oder Modelltraining.
Sicherheitskritische Aktionen werden nicht freigegeben, sondern ohne Executor
als `HUMAN_GATE_REQUIRED` markiert. Es gibt keinen versteckten Apply-Pfad.

## Lokal prüfen

Python 3.11 ist die deklarierte Mindestversion; daraus folgt keine bestätigte
Kompatibilität für jede Plattform oder Interpreterversion. Die Prüfskripte
benötigen nur die Standardbibliothek:

```powershell
python tools/verify.py
python tools/smoke.py
```

Für eine optionale Offline-Installation mit bereits vorhandenem setuptools >=77:
`python -m pip install --no-index --no-deps --no-build-isolation -e .`.
Eine normale pip-Installation ohne diese Optionen kann Build-Abhängigkeiten
herunterladen; das ist von den Offline-Prüfskripten getrennt.

Das englische [README](README.md) enthält ein Python-Integrationsbeispiel und ein
ausdrücklich als POSIX-Shell-Beispiel gekennzeichnetes CLI-Rezept.
Der Host muss sicherstellen, dass die Workspace- und Evidence-Verzeichnisse
getrennt sind und die KI weder die Operator-Parameter noch die Elternordner
oder die Audit-Datenbank kontrollieren kann.
Originale absolute Pfade übergeben; direkte Links nicht vorab mit `resolve()`
verbergen. Vertrauenswürdige Pfad-Aliase in Elternverzeichnissen werden bei der
physischen Audit-/Workspace-Trennung berücksichtigt.

## Prüfstand und Plattformgrenzen

- **Windows:** gezielte Code-, Unit-, Regressions-, Negativ- und Smoke-Prüfungen
  im tatsächlich getesteten Scope; **keine vollständige funktionale Produktabnahme**.
  Python 3.12.10, 3.13.13 und 3.15.0: jeweils 47 Tests entdeckt, 46 bestanden,
  ein Skip; Test- und Smoke-Exitcode jeweils 0.
- **Skip:** Das Fixture-Volume erlaubt keine getrennten Verzeichnisnamen nur
  durch Groß-/Kleinschreibung. Dieser case-sensitive Test lief dort nicht.
- **Abgeschlossene private Qualifikation:** neun erfolgreiche Jobs unter
  Windows/Linux/macOS mit Python 3.11/3.12/3.13. Je Windows-Job: 47 entdeckt,
  46 bestanden, ein Skip; je Linux-/macOS-Job: 47 entdeckt, 45 bestanden,
  zwei Skips. Der feste Bezugsstand, frühere Fehler und die Grenzen der
  Übertragbarkeit stehen in [RELEASE_EVIDENCE.md](RELEASE_EVIDENCE.md).
- **Release-Bindung:** spätere Quelldateiänderungen erfordern eine eigene
  Commit-/CI-/Asset-Zuordnung. Version 0.1.0 allein identifiziert keine Bytes.
  Der externe Release-Nachweis hält diese Zuordnung fest, ohne die eigene
  Commit-SHA in Quelldokumenten nachzuführen.
- **GitHub Actions PASS** bedeutet ausschließlich, dass die dokumentierten
  Tests dieses konkreten Commits in der jeweiligen Umgebung erfolgreich liefen.

Keine allgemeine Fehlerfreiheit, vollständige Sandbox-Sicherheit,
Produktionsreife oder garantierte plattformübergreifende Kompatibilität wird
behauptet. Python 3.15 lokal ersetzt keinen Python-3.11-CI-Lauf. Einzelheiten,
historische Fehler und Build-/Wheel-Prüfungen: [RELEASE_EVIDENCE.md](RELEASE_EVIDENCE.md).

Die Sicherheitsgrenzen bleiben: vertrauenswürdiger Host und geschützte
Elternverzeichnisse, kein Schutz vor einem Angreifer mit Host-Schreibrechten,
keine Racefreiheit und keine authentifizierte Audit-Signatur. Inhaltsdaten werden
unverändert geschrieben und nicht zuverlässig auf Secrets geprüft. Siehe
[Threat Model](docs/THREAT_MODEL.md) und [Invariant-Abdeckung](docs/INVARIANTS.md).

## Veröffentlichungsstatus

Dieses Repository eignet sich als überprüfbares, lokales Open-Source-Beispiel,
**nicht** als sofort einsatzfähiger Sicherheitsagent für externe Tools.
Die Datei `docs/INVARIANTS.md` kennzeichnet explizit, welche Forschungsregeln
im Code umgesetzt sind und welche noch fehlen.

Das Paket erstellt lokale Textdateien und eine lokale SQLite-Evidence-Datenbank.
Es führt keine Uploads, Deployments, Secret-Zugriffe, VM-Verwaltung,
Änderungen produktiver Laufzeiten oder Datenbanken, Rechteänderungen oder
Current-Switches aus.
Das gilt für den Runtime-Executor. Tests verwenden synthetische Dateien,
bereinigen eigene temporäre Fixtures und nutzen unter Windows `mklink` für echte
Junctions. Ein Test-PASS autorisiert weder Commit/Push noch Veröffentlichung.
Release-Entwurf und getrennte Gates: [PUBLISHING.md](PUBLISHING.md).

Der bevorzugte vertrauliche Meldeweg ist GitHub Private Vulnerability Reporting.
Seine Aktivierung wird hier nicht behauptet; maßgeblich ist die tatsächlich
verfügbare private Meldefunktion. Details und Ausfallverhalten: [SECURITY.md](SECURITY.md).
Keine Sicherheitsdetails in öffentliche Issues schreiben. Verfügbarkeit und
Identität einer Veröffentlichung ergeben sich erst aus dem Release-Nachweis.
