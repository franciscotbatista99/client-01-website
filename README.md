# client-01-website – Nordwerk Industrie-Service

Kundenprodukt aus dem Kursprojekt Agentic AI (HAW Hamburg). Fiktives Unternehmen, Lehrprojekt.
Die Inhalte werden von der Software Factory erzeugt (Factory-Repo: `cait33/agentic_ai`).
Dieses Repo enthält **nur** das Produkt: statisches HTML/CSS, Produkttests und Lieferdokumentation.
Keine Factory, kein LLM, keine Datenbank, keine Secrets.

## Starten

```bash
python3 -m http.server 8000 --directory site
```

Dann <http://localhost:8000> öffnen. Alternativ `site/index.html` direkt im Browser öffnen.

## Produkttests

```bash
python3 -m pip install pytest   # einmalig, falls nicht vorhanden
python3 -m pytest tests -q
```

Geprüft wird (Termin 3): Firmenname und Hauptaussage (AC-01), mindestens eine Leistung mit Pflichttext (AC-02),
Kontaktlink `mailto:kontakt@nordwerk.example` und Übungshinweis (AC-04), außerdem Sprache/Titel und lokale Assets.

## Struktur

| Pfad | Inhalt |
|---|---|
| `site/` | Website (einziger Bereich, den Factory-Agenten schreiben dürfen) |
| `tests/` | Produkttests |
| `docs/` | Klärungen, Abnahme, Lieferbericht |

## AC-08: Fresh Checkout Instructions

To perform a fresh checkout and run the project from scratch:

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/franciscotbatista99/client-01-website.git](https://github.com/franciscotbatista99/client-01-website.git)
   cd client-01-website