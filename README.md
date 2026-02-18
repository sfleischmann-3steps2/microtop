# MICROTOP TW — Produktvergleich Trinkwasserbeschichtungen

Automatisierte Vergleichsseite in Notion für die 8 MICROTOP TW Produkte (Trinkwasser-Beschichtungsmörtel) von KORODUR.

## Was macht dieses Projekt?

1. **PDF-Parsing**: Extrahiert technische Daten aus 6 Produktdatenblättern (8 Produkte)
2. **Notion-DB-Update**: Schreibt fehlende Properties in die bestehende Produktdatenbank
3. **Vergleichsseite**: Erstellt eine vertriebsorientierte Übersichtsseite in Notion

## Produkte

| Produkt | Körnung | Verfahren | PDF |
|---------|---------|-----------|-----|
| MICROTOP TW 3 | 0 – 3 mm | Trockenspritzen | TW_3_5_8 |
| MICROTOP TW 5 | 0 – 5 mm | Trockenspritzen | TW_3_5_8 |
| MICROTOP TW 8 | 0 – 8 mm | Trockenspritzen | TW_3_5_8 |
| MICROTOP TW NSM | 0 – 3 mm | Nassspritzen | NSM |
| MICROTOP TW BM | 0 – 1 mm | Schleudern/Spritzen/Hand | BM |
| MICROTOP TW VSM | 0 – 2 mm | Spritzen/Hand | VSM |
| MICROTOP TW Mineral | flüssig | Pinsel/Sprühen | Mineral |
| MICROTOP TW 02 | 0 – 0,2 mm | Spritzen/Spachteln | 02 |

## Setup

```bash
# Python-Abhängigkeiten installieren
pip install -r requirements.txt

# .env anlegen mit Notion-Token
echo "NOTION_TOKEN=secret_..." > .env
```

## Verwendung

```bash
# PDFs parsen + fehlende Notion-DB-Properties updaten
python -m src --extract

# Vergleichsseite in Notion erstellen
python -m src --build-page

# Beides zusammen
python -m src --all

# Preview ohne Notion-Writes (JSON-Dump nach data/page_blocks.json)
python -m src --dry-run --all

# Debug-Logging
python -m src --all -v
```

## Projektstruktur

```
microtop/
├── src/
│   ├── main.py             # Orchestrator, CLI
│   ├── config.py            # Notion-IDs, Produkt-Mappings
│   ├── models.py            # MicroTopProduct Dataclass
│   ├── pdf_parser.py        # PDF-Extraktion (PyMuPDF)
│   ├── notion_reader.py     # Bestehende Daten aus Notion-DB lesen
│   ├── notion_updater.py    # Fehlende Properties in Notion-DB schreiben
│   └── page_builder.py      # Vergleichsseite als Notion-Blocks
├── data/
│   └── pdfs/                # 6 Produktdatenblätter (PDF)
├── requirements.txt
├── .env                     # NOTION_TOKEN (nicht im Repo)
└── .gitignore
```

## Seitenlayout (v2)

Die generierte Notion-Seite enthält:

1. **Hero** — Bild-Platzhalter + blauer Callout (Produktfamilie)
2. **"Das kennen Sie"** — Problem-Statement (orange)
3. **"Die Lösung"** — Solution-Statement (grün)
4. **Entscheidungstabelle** — Bedarf / Produkt / Schichtdicke / Verfahren
5. **Körnungsvarianten** — TW 3 · TW 5 · TW 8 Vergleich
6. **Spezialverfahren** — TW NSM · TW BM · TW VSM Vergleich
7. **Spezialprodukte** — TW Mineral · TW 02 Vergleich
8. **DVGW-Zulassungen** — Qualitätsmerkmal
9. **Gesamtübersicht** — 2 Toggle-Tabellen (Spritz-Mörtel + Spezialprodukte)
10. **Leistungsmerkmale** — Bullet-Liste
11. **Normen & Regelwerke**
12. **Produkte** — Page-Mentions zu allen 8 DB-Einträgen
13. **CTA** — Kontakt-Callout
14. **Footer** — Zementhinweis, Stand, Datenquelle

## Notion-IDs

- **Produktdatenbank**: `2ec670e1-9e1a-8110-8100-c85e74a74750`
- **Parent Page** (Produktkatalog): `309670e1-9e1a-80da-80b7-cd881f017bef`
- **Vergleichsseite** (v2): `30b670e1-9e1a-81e9-8d65-e21d36378a5a`

## Status

- [x] PDF-Parsing aller 8 Produkte
- [x] Notion-DB-Update (10 Properties)
- [x] Vergleichsseite v2 live
- [x] Bild-Platzhalter eingefügt (3x 📷)
- [ ] Kollegen-Review / Feedback
- [ ] Bilder manuell einfügen
- [ ] Ggf. Layout-Anpassungen nach Feedback
