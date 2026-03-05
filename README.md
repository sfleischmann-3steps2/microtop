# MICROTOP TW — Landing Page & Produktvergleich

Marketing-Projekt fuer die MICROTOP TW Produktfamilie (Trinkwasser-Beschichtungsmoertel) von KORODUR.

## Live Landing Page

**https://sfleischmann-3steps2.github.io/microtop/landing-page/**

Standalone HTML-Landingpage im KORODUR Corporate Design (ARM-Style) mit:
- 3 Referenzprojekte mit Bildern von korodur.de
- Dreifach-Vergleich (Mineralisch vs. Epoxid vs. Edelstahl)
- Produktfinder mit 8 DVGW-zugelassenen Produkten
- Responsive Design (Mobile, Tablet, Desktop)
- Schema.org Markup (Product, FAQPage, Organization)

## Projektstruktur

```
microtop/
├── landing-page/
│   ├── index.html               # Landing Page (Single-File, inline CSS+JS)
│   ├── img/                     # Bilder (Logo, Hero, Referenzen, Verfahren, Berater)
│   ├── 01-strategie-analyse.md  # Strategisches Konzept
│   ├── 02-seo-analyse.md        # Keywords, Meta-Tags, Schema Markup
│   ├── 03-content-texte.md      # Alle Texte
│   ├── 04-cro-analyse.md        # CRO-Analyse (7 Punkte)
│   ├── 05-umsetzungskonzept.md  # Technische Spezifikation
│   └── 06-redesign-plan.md      # ARM Corporate Design Angleichung
├── src/                         # Notion Comparison Page Builder (Python)
│   ├── main.py, config.py, models.py
│   ├── pdf_parser.py, notion_reader.py
│   ├── notion_updater.py, page_builder.py
├── data/pdfs/                   # 6 Produktdatenblaetter (PDF)
├── requirements.txt
└── .env                         # NOTION_TOKEN (nicht im Repo)
```

## Produkte

| Produkt | Koernung | Verfahren |
|---------|----------|-----------|
| MICROTOP TW 3 | 0 – 3 mm | Trockenspritzen |
| MICROTOP TW 5 | 0 – 5 mm | Trockenspritzen |
| MICROTOP TW 8 | 0 – 8 mm | Trockenspritzen |
| MICROTOP TW NSM | 0 – 3 mm | Nassspritzen |
| MICROTOP TW BM | 0 – 1 mm | Schleudern/Spritzen/Hand |
| MICROTOP TW VSM | 0 – 2 mm | Spritzen/Hand |
| MICROTOP TW Mineral | fluessig | Pinsel/Spruehen |
| MICROTOP TW 02 | 0 – 0,2 mm | Spritzen/Spachteln |

## Referenzen auf der Landing Page

| Projekt | Volumen | Link |
|---------|---------|------|
| Hochbehaelter Haidberg | 75.000 m3 | [korodur.de](https://www.korodur.de/referenzen/sanierung-trinkwasser-hochbehalter-haidberg/) |
| Hochbehaelter Krottenbach Nuernberg | 10.000 m3 | [korodur.de](https://www.korodur.de/referenzen/hochbehalter-krottenbach-nurnberg/) |
| Trinkwasserturm Budapest | 3.000 m3 | [korodur.de](https://www.korodur.de/referenzen/trinkwasserturm-budapest/) |

## Status

### Erledigt
- [x] Strategie-Analyse, SEO-Analyse, Content-Texte, CRO-Analyse, Umsetzungskonzept
- [x] Landing Page v1 (Standalone HTML)
- [x] Landing Page v2 (ARM Corporate Design Angleichung)
- [x] 6 Referenzprojekte mit Bildern von korodur.de integriert
- [x] Landing Page v3: Kollegen-Review eingearbeitet (3 Wiedemann-Referenzen entfernt, Key Figures, Fettdruck DVGW/W300/W347, Headline angepasst)
- [x] 3 Verfahren-Bilder (Nassspritzen, Trockenspritzen, Manuell/Schleudern)
- [x] KORODUR Logo + Header-Bild eingebaut
- [x] CTA aufgeteilt: Benjamin Lorenz (Technik) + KORODUR Zentrale (Allgemein)
- [x] GitHub Pages live
- [x] Notion Comparison Page Builder (PDF-Parsing, DB-Update, Vergleichsseite)

### Offen
- [ ] Produktnamen in Produktfinder mit Datenblaettern verlinken
- [ ] Ggf. bessere Verfahren-Bilder vom Kunden
- [ ] Ggf. Header-Logo als SVG (aktuell PNG)
- [ ] Kundenzitat / Testimonial einholen
- [ ] Google Analytics / Tracking einrichten

## Notion-IDs

- **Produktdatenbank**: `2ec670e1-9e1a-8110-8100-c85e74a74750`
- **Parent Page**: `309670e1-9e1a-80da-80b7-cd881f017bef`
- **Vergleichsseite**: `30b670e1-9e1a-81e9-8d65-e21d36378a5a`

## Setup (Notion Page Builder)

```bash
pip install -r requirements.txt
echo "NOTION_TOKEN=secret_..." > .env
python -m src --all
```
