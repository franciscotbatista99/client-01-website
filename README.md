# client-01-website – Nordwerk Industrie-Service

A website for Nordwerk Industrie-Service, a fictional small B2B service provider in Hamburg.

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

Geprüft wird: Firmenname und Hauptaussage, mindestens eine Leistung mit Pflichttext,
Kontaktlink `mailto:kontakt@nordwerk.example` und Übungshinweis, außerdem Sprache/Titel und lokale Assets.

## Struktur

| Pfad | Inhalt |
|---|---|
| `site/` | Website |
| `tests/` | Produkttests |
| `docs/` | Klärungen, Abnahme, Lieferbericht |

## AC-08: Fresh Checkout Instructions

To perform a fresh checkout and run the project from scratch:

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/franciscotbatista99/client-01-website.git](https://github.com/franciscotbatista99/client-01-website.git)
   cd client-01-website