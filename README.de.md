# ForgeProofGate – Deutsch

**Technische Referenzimplementierung für deterministische Sicherheitsgrenzen von KI-Agenten.**

Stand: **v0.1.0 / LOCAL_ONLY / nicht sicherheitszertifiziert**.

ForgeProofGate setzt nicht bloß einen Systemprompt ein, sondern prüft
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

Auf einem System mit Python 3.11 oder neuer:

```powershell
python tools/verify.py
python tools/smoke.py
```

Zur Installation optional: `python -m pip install -e .`. Für diesen Schritt
kann ein Build-Werkzeug erforderlich sein, für die Prüfskripte nicht.

Zur manuellen Nutzung die Befehle im englischen [README](README.md) verwenden.
Der Host muss sicherstellen, dass die Workspace- und Evidence-Verzeichnisse
getrennt sind und die KI weder die Operator-Parameter noch die Elternordner
oder die Audit-Datenbank kontrollieren kann.

## Veröffentlichungsstatus

Dieses Repository eignet sich als überprüfbares, lokales Open-Source-Beispiel,
**nicht** als sofort einsatzfähiger Sicherheitsagent für externe Tools.
Die Datei `docs/INVARIANTS.md` kennzeichnet explizit, welche Forschungsregeln
im Code umgesetzt sind und welche noch fehlen.

Das Paket erstellt lokale Textdateien und eine lokale SQLite-Evidence-Datenbank.
Es führt keine Uploads, Deployments, Secret-Zugriffe, VM-Verwaltung,
Änderungen produktiver Laufzeiten oder Datenbanken, Rechteänderungen oder
Current-Switches aus.
