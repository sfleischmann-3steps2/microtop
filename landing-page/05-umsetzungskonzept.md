# Umsetzungskonzept: MICROTOP TW Landingpage

**Datum:** 04.03.2026
**Agent:** Landing Page Builder (Agent 6)
**Status:** Entwurf v1

---

## 1. Technische Entscheidung: Notion vs. Standalone HTML

### Option A: Notion Page Builder erweitern
| Pro | Contra |
|-----|--------|
| Bestehende Infrastruktur | Kein Custom-Design möglich |
| Schnell umsetzbar (Python-Code existiert) | Keine Sticky CTAs, kein JS |
| Notion-Ökosystem (Produktlinks funktionieren) | Keine klickbaren Tel/Mail-Links |
| Team kann direkt in Notion editieren | Kein Schema.org Markup |
| | Kein Responsive-Control |
| | Keine Analytics/Tracking |
| | Tabellen nicht mobile-friendly |

### Option B: Standalone HTML/CSS Landingpage
| Pro | Contra |
|-----|--------|
| Volle Design-Kontrolle (KORODUR CI) | Mehr Aufwand initial |
| Sticky CTA, Akkordeon, Tabs | Braucht Hosting |
| Schema.org für SEO | Separate Pflege |
| Responsive Design | |
| Klickbare Tel/Mail-Links | |
| Analytics-Integration | |
| A/B-Testing möglich | |
| Bild-Optimierung (WebP, lazy load) | |

### Empfehlung: **Option B — Standalone HTML**

**Begründung:** Die CRO-Analyse zeigt, dass die wichtigsten Conversion-Elemente (Sticky CTA, klickbare Telefonnummer, Akkordeon-FAQ, responsive Tabellen) in Notion nicht umsetzbar sind. Der persönliche Ansprechpartner Benjamin Lorenz mit Direktnummer ist das stärkste Conversion-Element — das muss klickbar und sticky sein.

**Zusätzlich:** Notion Page Builder als Zweitnutzung beibehalten für interne/Vertriebsnutzung.

---

## 2. Technische Spezifikation

### Stack
- **Single-File:** `landing-page/index.html` (inline CSS + JS)
- **Framework:** Kein Framework — Vanilla HTML5 + CSS3 + ES6
- **Fonts:** Gabarito (Google Fonts) + Arial Fallback
- **Design-System:** KORODUR Corporate Design

### CSS Variables
```css
:root {
  --primary: #002d59;
  --secondary: #009ee3;
  --light-gray: #ececed;
  --mid-gray: #d9dada;
  --white: #ffffff;
  --cta: #009ee3;
  --cta-hover: #007bb8;
  --success: #28a745;
  --warning: #f5a623;
  --danger: #e74c3c;
  --font: "Gabarito", Arial, sans-serif;
  --radius: 8px;
  --card-radius: 12px;
  --section-pad-d: 80px 0;
  --section-pad-m: 48px 0;
  --max-width: 1140px;
}
```

### Responsive Breakpoints
- Mobile: < 768px
- Tablet: 768px – 1024px
- Desktop: > 1024px

---

## 3. Sektions-Bauplan

### Sektion 1: Header (sticky)
```
┌──────────────────────────────────────────────┐
│ KORODUR (Text-Logo, Gabarito)    [Anrufen]   │
└──────────────────────────────────────────────┘
```
- Sticky auf Scroll
- Mobile: Hamburger-Menü nicht nötig (Single-Page)
- Rechts: CTA-Button "Anrufen: +49 170 3733988" (tel:-Link)

### Sektion 2: Hero
```
┌──────────────────────────────────────────────┐
│  Background: 4.png (Behälter-Innenraum)      │
│  Overlay: linear-gradient rgba(0,45,89,.75)  │
│                                               │
│  H1: Trinkwasserbehälter sanieren –           │
│      mit dem mineralischen Komplettsystem     │
│                                               │
│  Subline: 8 DVGW-zugelassene Produkte.       │
│  12+ Referenzprojekte. Ein System.            │
│                                               │
│  [Jetzt beraten lassen]  [Referenzen ↓]      │
└──────────────────────────────────────────────┘
```
- Hintergrundbild: `4.png`, `background-size: cover`, `background-position: center`
- Gradient-Overlay: `--primary` mit 75% Opacity
- H1: weiß, Gabarito, 2.5rem (Desktop) / 1.75rem (Mobile)
- Buttons: Primär `--cta` filled, Sekundär transparent + white border

### Sektion 3: Trust Bar
```
┌────────┬────────┬────────┬────────┐
│  12+   │   8    │75.000m³│ DVGW   │
│Projekte│Produkte│größtes │W300+347│
└────────┴────────┴────────┴────────┘
```
- Background: `--primary`
- 4-Spalter Desktop → 2x2 Grid Mobile
- Zahlen: 2rem bold, Labels: 0.85rem

### Sektion 4: Problem (3 Cards)
- H2: "Das kennen Sie"
- 3 Cards nebeneinander (Desktop) → Stack (Mobile)
- Card 1: Substanzverlust (Icon: Warnung)
- Card 2: Hygienerisiko (Icon: Bakterie)
- Card 3: Kostendruck (Icon: Euro)
- Card-Design: `--light-gray` Background, `--card-radius`, leichter Schatten

### Sektion 5: Lösung
- H2: "Die Lösung: Ein System für jeden Arbeitsschritt"
- Grüner Callout-Banner (`--success` light background)
- Bild: Bild1Microtop.jpg rechts (Desktop), oben (Mobile)

### Sektion 6: Benefit-Grid (6 Vorteile)
- H2: "Warum MICROTOP TW?"
- 3x2 Grid (Desktop) → 2x3 (Tablet) → 1x6 (Mobile)
- Je Card: Icon + Titel + 1-2 Sätze
- Checkmark-Icons in `--secondary` Farbe

### Sektion 7: Referenzen (Herzstück)
- H2: "Bewährt in der Praxis – 12+ Projekte seit 2009"
- **3 Featured References** als große Cards:
  1. Haidberg (75.000 m³) — Systembreite
  2. Bad Nauheim (3.000 m²) — mit Foto aus 5.png
  3. Karpf (7.000 m²) — mit Foto aus 5.png
- Je Card: Tagline, Key Facts als mini-Grid, 2-3 Sätze Text
- Referenz-Links zu korodur.de Detailseiten
- **Referenz-Tabelle** als Akkordeon/Toggle: "Alle 12+ Projekte anzeigen"
- **Aktiv-Banner:** Grüner Callout "Aktuell in Sanierung (2026): 4 Projekte"

**Zwischen-CTA:** "Ihr Projekt besprechen? Benjamin Lorenz berät Sie: +49 170 3733988"

### Sektion 8: Verarbeitungsverfahren
- H2: "Ein System – drei Verfahren"
- **3-Spalter mit Bildern** (Desktop) → Tabs oder Stack (Mobile)
- Bilder aus 5.png (müssen als 3 einzelne Dateien extrahiert werden)
  - `nassspritzen.jpg` — oberer Bereich
  - `trockenspritzen.jpg` — mittlerer Bereich
  - `glaetten.jpg` — unterer Bereich
- Je Spalte: Bild oben, H3 Verfahrensname, Produktzuordnung, Kurzbeschreibung

### Sektion 9: Produktfinder
- H2: "Das richtige Produkt für Ihren Bedarf"
- **Responsive Tabelle:** Desktop = Tabelle, Mobile = Cards
- 8 Zeilen: Bedarf → Produkt → Schichtdicke → Verfahren
- Produktnamen als Links zu korodur.de Produktseiten

**Zwischen-CTA:** "Nicht sicher? Rufen Sie an: +49 170 3733988"

### Sektion 10: Dreifach-Vergleich
- H2: "Warum mineralisch? Der Systemvergleich."
- **Vergleichstabelle:** 3 Spalten (MICROTOP TW, Epoxid, Edelstahl)
- MICROTOP-Spalte visuell hervorgehoben (`--secondary` light background)
- Desktop = Tabelle, Mobile = 3 gestapelte Cards
- Fazit als Callout darunter

### Sektion 11: DVGW
- H2: "DVGW-zugelassen – ohne Kompromisse"
- Grüner Callout mit Zulassungsdetails
- Normen-Liste

### Sektion 12: FAQ (NEU — aus CRO-Empfehlung)
- H2: "Häufige Fragen"
- **Akkordeon** mit 4–6 Fragen
- `aria-expanded` für Barrierefreiheit
- Schema.org FAQPage Markup inline

### Sektion 13: CTA — Benjamin Lorenz
```
┌──────────────────────────────────────────────┐
│  ┌─────────┐                                  │
│  │  FOTO   │  Benjamin Lorenz                 │
│  │Benjamin │  Technische Vertriebsberatung    │
│  │ Lorenz  │  Trinkwasser / MICROTOP          │
│  └─────────┘                                  │
│                                               │
│  "Sie planen eine Behältersanierung?          │
│   Ich berate Sie persönlich."                 │
│                                               │
│  [📞 Jetzt anrufen]  [✉ E-Mail schreiben]   │
│                                               │
│  +49 (0) 170 3733988                         │
│  b.lorenz@korodur.de                         │
│                                               │
│  "Persönliche Beratung – kostenlos und        │
│   unverbindlich."                             │
└──────────────────────────────────────────────┘
```
- Berater-Foto: `Benjamin-Lorenz-2048x2048.jpg` (als 200x200 Circle Crop)
- Buttons: `tel:+491703733988` und `mailto:b.lorenz@korodur.de`
- Background: `--light-gray`

### Sektion 14: Footer
```
┌──────────────────────────────────────────────┐
│ KORODUR International GmbH                    │
│ Normen: DVGW W 300 · W 347 · DIN EN ...     │
│ Zementhinweis: ...                            │
│ Stand: 04.03.2026                             │
│                                               │
│ Impressum  Datenschutz  korodur.de            │
└──────────────────────────────────────────────┘
```
- Gabarito-Text "KORODUR" statt Logo-Bild
- Kompakt, dunkelblau (`--primary` Background, weiße Schrift)

### Sticky CTA (Mobile only)
```
┌──────────────────────────────────────────────┐
│  📞 Benjamin Lorenz anrufen                   │
└──────────────────────────────────────────────┘
```
- Fixiert am unteren Bildschirmrand
- Erscheint per IntersectionObserver wenn Hero aus Viewport scrollt
- `tel:+491703733988`
- Background: `--cta`, weiße Schrift

---

## 4. Bild-Integration

### Benötigte Bild-Dateien

| Datei | Quelle | Verwendung | Größe (empfohlen) |
|-------|--------|-----------|-------------------|
| `hero-bg.jpg` | 4.png (konvertiert) | Hero-Hintergrund | 1920x1080, WebP + JPG fallback |
| `behaelter-innen.jpg` | Bild1Microtop.jpg | Lösungs-Sektion | 800x600 |
| `nassspritzen.jpg` | 5.png (Crop oben) | Verfahren: Nassspritzen | 600x400 |
| `trockenspritzen.jpg` | 5.png (Crop mitte) | Verfahren: Trockenspritzen | 600x400 |
| `glaetten.jpg` | 5.png (Crop unten) | Verfahren: Glätten | 600x400 |
| `benjamin-lorenz.jpg` | Benjamin-Lorenz-2048x2048.jpg | CTA-Sektion | 400x400 (Circle Crop) |

### Bild-Aufbereitung nötig
- **5.png muss in 3 Einzelbilder geschnitten werden** (Nassspritzen, Trockenspritzen, Glätten)
- Alle Bilder in WebP konvertieren (Fallback JPG)
- Lazy Loading für Below-the-fold Bilder

---

## 5. Responsive-Verhalten

| Element | Desktop (>1024px) | Tablet (768-1024px) | Mobile (<768px) |
|---------|-------------------|--------------------|-----------------|
| Header | Sticky, Logo links, CTA rechts | Gleich | Kompakter, CTA = Icon |
| Hero | Fullwidth, große Typo | Padding reduziert | H1 kleiner, Buttons stacked |
| Trust Bar | 4-Spalter inline | 2x2 Grid | 2x2 Grid |
| Problem-Cards | 3-Spalter | 3-Spalter | Vertikal gestackt |
| Benefit-Grid | 3x2 Grid | 2x3 Grid | 1-Spalte |
| Referenz-Cards | 3-Spalter | 2+1 | Vertikal gestackt |
| Verfahren | 3-Spalter mit Bildern | 3-Spalter | Tabs oder Stack |
| Produktfinder-Tabelle | Tabelle (4 Spalten) | Tabelle (scroll) | Cards (je Produkt 1 Card) |
| Dreifach-Vergleich | Tabelle (3 Spalten) | Tabelle | 3 gestapelte Cards |
| FAQ | Akkordeon | Akkordeon | Akkordeon |
| CTA-Sektion | Foto links, Text rechts | Gleich | Foto oben, Text unten |
| Sticky CTA | Nicht sichtbar | Nicht sichtbar | Fixiert unten |

---

## 6. Sektions-Checkliste

| # | Sektion | Status | Quelle |
|---|---------|--------|--------|
| 1 | Header (sticky) | **NEU** | — |
| 2 | Hero + Gradient | **NEU** | Content: 03-content-texte.md §1 |
| 3 | Trust Bar | **NEU** | Content: 03-content-texte.md §2 |
| 4 | Problem (3 Cards) | **ANGEPASST** | Basis: page_builder.py `_build_problem()`, Content: §3 |
| 5 | Lösung | **ANGEPASST** | Basis: page_builder.py `_build_solution()`, Content: §4 |
| 6 | Benefit-Grid | **NEU** | Content: 03-content-texte.md §6 |
| 7 | Referenzen (3 Featured + Tabelle) | **NEU** | Content: 03-content-texte.md §5 |
| 8 | Verarbeitungsverfahren (3-Spalter) | **NEU** | Content: 03-content-texte.md §7 |
| 9 | Produktfinder | **ÜBERNOMMEN** | Basis: page_builder.py `_build_decision_table()`, Content: §8 |
| 10 | Dreifach-Vergleich | **NEU** | Content: 03-content-texte.md §9 |
| 11 | DVGW-Zulassungen | **ÜBERNOMMEN** | Basis: page_builder.py `_build_dvgw()`, Content: §10 |
| 12 | FAQ (Akkordeon) | **NEU** | SEO: 02-seo-analyse.md §6, CRO: 04-cro-analyse.md §6 |
| 13 | CTA — Benjamin Lorenz | **NEU** | Content: 03-content-texte.md §11 |
| 14 | Footer | **ANGEPASST** | Basis: page_builder.py `_build_footer()`, Content: §12 |
| 15 | Sticky CTA (Mobile) | **NEU** | CRO: 04-cro-analyse.md |
| 16 | Schema.org (3x JSON-LD) | **NEU** | SEO: 02-seo-analyse.md §6 |
| 17 | Meta Tags + OG | **NEU** | SEO: 02-seo-analyse.md §3 |

### Zusammenfassung:
- **5 Sektionen übernommen/angepasst** aus bestehendem Page Builder
- **12 Sektionen/Elemente NEU** zu erstellen
- **Geschätzte HTML-Größe:** ~800-1000 Zeilen (Single-File mit Inline CSS+JS)

---

## 7. Nächster Schritt: Build

Sobald der Projektleiter die CRO-Analyse (04) und dieses Umsetzungskonzept (05) freigibt:

1. **Bilder aufbereiten** — 5.png in 3 Teile schneiden, alle als WebP exportieren
2. **index.html erstellen** — Sektionen 1-17 nach diesem Bauplan
3. **Testen** — Responsive, Links, Accessibility
4. **Review** — Projektleiter prüft gegen Checkliste

---

*Erstellt von: Landing Page Builder (Agent 6) | Review durch: Projektleiter (Agent 0) ausstehend*
