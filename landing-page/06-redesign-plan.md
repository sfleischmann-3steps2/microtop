# Redesign-Plan: MICROTOP TW Landingpage v2

**Datum:** 04.03.2026
**Ziel:** Corporate Design-Angleichung an ARM Landing Page + User-Feedback umsetzen

---

## 1. Design-System: Was sich ändern muss

### CSS Variables — ARM übernehmen
| Variable | Aktuell (MICROTOP) | ARM (Ziel) |
|----------|-------------------|------------|
| `--light-gray` | `#f5f6f7` | `#ececed` |
| `--max-width` | `1140px` | `1200px` → `--max-w` |
| `--shadow` | fehlt | `0 2px 12px rgba(0,45,89,.08)` |
| `--text` | `#333` (body) | `var(--primary)` = `#002d59` |
| Font weights | 400–700 | **400, 700, 800, 900** |

### Typografie — ARM übernehmen
- H1: `font-weight: 900`, `text-transform: uppercase`, `clamp(2rem, 5vw, 3.2rem)`
- H2: `font-weight: 900`, `text-transform: uppercase`, `clamp(1.6rem, 3.5vw, 2.4rem)`
- H3: `font-weight: 700`, `clamp(1.1rem, 2vw, 1.4rem)`
- `.subline`: `font-weight: 800`, `text-transform: uppercase`
- Body: `color: var(--text)` (dunkelblau statt #333)

### Button-Klassen — ARM übernehmen
- `btn--primary` → `btn-primary`
- `btn--secondary` → `btn-ghost`
- Button-Styling: `padding: 16px 32px`, `border: 2px solid transparent`

### Utility-Klassen — ARM übernehmen
- `bg-white`, `bg-gray`, `bg-dark`
- `.section-intro` Klasse
- `.micro-copy` Klasse

---

## 2. Sektions-Änderungen (Feedback + ARM-Angleichung)

### 2.1 Header → ARM-Style
**Aktuell:** Dunkelblauer Header mit Text-Logo "KORODUR MICROTOP TW"
**Ziel:** Weißer sticky Header mit Logo-Bild, Nav-Links, Mobile Hamburger

```
┌────────────────────────────────────────────────────┐
│ [LOGO img 72px]         Produkt  Referenzen  Kontakt  │
│                                        [☰] (mobile)   │
└────────────────────────────────────────────────────┘
```

- **WARTEN AUF:** User liefert Logo-Bild
- Fallback: KORODUR Text-Logo in Gabarito (wie ARM-Header)
- Klassen: `.logo img { height: 72px }`, `header nav a`, `.mobile-menu-btn`
- Border-bottom: `1px solid var(--mid-gray)`

### 2.2 Hero → ARM-Style (heller Gradient statt dunkles Overlay)
**Aktuell:** Dunkles Vollbild-Foto mit Overlay
**Ziel:** Heller Gradient-Hintergrund + Key-Figures in weißen Cards

```
┌─────────────────────────────────────────────────────┐
│  H1: TRINKWASSERBEHÄLTER SANIEREN –                   │
│      MIT DEM MINERALISCHEN KOMPLETTSYSTEM             │
│  (uppercase, weight 900)                               │
│                                                        │
│  Subline: 8 DVGW-zugelassene Produkte...              │
│                                                        │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐ │
│  │   12+    │ │    8     │ │ 75.000m³ │ │  DVGW    │ │
│  │ Projekte │ │ Produkte │ │ größtes  │ │ W300+347 │ │
│  └──────────┘ └──────────┘ └──────────┘ └──────────┘ │
│                                                        │
│  [Jetzt beraten lassen]  [Referenzen ansehen]         │
│                                                        │
│ ┌────────────────────────────────────────────────────┐│
│ │ ✓ 12+ Referenzprojekte  ✓ Seit 2009  ✓ DVGW      ││
│ └────────────────────────────────────────────────────┘│
└─────────────────────────────────────────────────────┘
```

- Background: `linear-gradient(135deg, var(--light-gray) 0%, var(--white) 100%)`
- Hero-Bild als `::before` pseudo-element (rechts, opacity .28) — statt Vollbild-Overlay
- Key-Figures: weiße Cards mit `--card-radius` + `--shadow`
- Mini Trust Bar: `bg-dark` am unteren Rand des Hero (INSIDE hero section)

### 2.3 Problem-Sektion → Section-Toggle (ARM-Pattern)
**Aktuell:** Problem-Cards direkt sichtbar
**Ziel:** Kurztext + "Details anzeigen" Toggle-Button → Problem-Cards + Bridge

- H2 + `.section-intro` sichtbar
- `section-toggle` Button: "Details anzeigen: Warum herkömmliche Methoden scheitern"
- Problem-Cards IN toggle-content (eingeklappt by default)
- `.section-bridge` nach den Cards
- Problem-Card Styling: border-top Eskalation (mid-gray → mid-gray → secondary), letzte Card `scale(1.03)`

### 2.4 Lösung → Full-Width (User-Feedback)
**Aktuell:** Solution-Box mit max-width 800px
**Ziel:** Volle Container-Breite, kein max-width Constraint

### 2.5 Benefit-Grid → Bleibt (User: "gut")
Keine Änderung. Nur CSS-Feintuning auf ARM-Shadows und Farben.

### 2.6 Referenzen → 3-4 Links + Toggle-Liste (User-Feedback)
**Änderungen:**
1. Referenz-Cards im ARM `ref-grid` Style (2-Spalter statt 3-Spalter)
2. Badge-Pills: `.ref-card-badge` + `.ref-card-highlight`
3. **Mehr Links zu korodur.de** — aktuell nur 2, braucht 3-4:
   - Haidberg: `korodur.de/referenzen/sanierung-trinkwasser-hochbehalter-haidberg/` ✅
   - Bad Nauheim: `korodur.de/en/references/drinking-water-reservoir-bad-nauheim/` ✅
   - **Räcknitz: `korodur.de/referenzen/hochbehalter-racknitz/`** ← NEU
   - **Puchheim: `korodur.de/en/references/drinking-water-reservoir-puchheim/`** ← NEU
4. **"Aktuell in Sanierung" in die Toggle-Liste verschieben** (nicht als separater Banner)
5. Toggle-Button: ARM `.section-toggle` Style (statt eigenem `ref-table-toggle`)

### 2.7 Verfahren → Bilder austauschbar machen
**WARTEN AUF:** User liefert neue Verfahren-Bilder
- "Ein System – drei Verfahren" H2: **full-width fix** (Bug: spannt nicht volle Breite)
- Platzhalter-Bilder beibehalten bis User neue liefert

### 2.8 Produktfinder → Produkte mit Datenblättern verlinken (User-Feedback)
**Änderungen:**
- Produktnamen in der Tabelle werden Links zu technischen Datenblättern
- Datenblatt-URLs: `data/pdfs/` Dateien oder korodur.de Produktseiten
- ARM comparison-table Styling übernehmen

### 2.9 Dreifach-Vergleich → ARM comparison-table + Mobile Cards
**Aktuell:** Eigene `compare-table` + `compare-fazit` Klassen
**Ziel:** ARM `.comparison-table` + `.comparison-cards` (Mobile)

**Änderungen:**
- MICROTOP TW Spalte hervorgehoben (`th:nth-child(2)` = `--secondary`)
- **MICROTOP TW immer fett** im Fazit-Text (User-Feedback)
- Fazit-Text prominenter gestalten: `comparison-summary` Klasse
- Mobile: `comparison-cards` statt Tabelle

### 2.10 DVGW → Prominenter (User-Feedback)
**Aktuell:** Kleine grüne Box
**Ziel:** Größer, mehr Präsenz

- Volle Container-Breite
- Größerer Padding
- H2 statt H3 intern
- Eventuell eigener `bg-gray` Hintergrund für die ganze Section

### 2.11 FAQ → ARM faq-item Style
**Aktuell:** Eigene FAQ-Styles
**Ziel:** ARM `.faq-item`, `.faq-question`, `.faq-answer` Klassen

- Question: `active` State mit `bg-dark` + weiß
- Answer: `max-height` Transition
- `::after` content: "+" / "−"

### 2.12 CTA-Sektion → Zweigeteilt (User-Feedback)
**User-Feedback:** Benjamin Lorenz nur für konkrete Projekte / tiefe technische Fragen. Allgemeine Anfragen → allgemeiner KORODUR-Kontakt.

**Ziel:** ARM Berater-Style mit 2 Kontakt-Optionen

```
┌─────────────────────────────────────────────────────┐
│  bg-dark                                              │
│  H2: SPRECHEN SIE MIT UNSEREM TEAM                    │
│                                                        │
│  ┌────────────────────┐  ┌────────────────────┐      │
│  │ [Foto Benjamin]    │  │ [KORODUR Logo/Icon]│      │
│  │ Benjamin Lorenz    │  │ KORODUR Zentrale   │      │
│  │ Techn. Beratung TW │  │ Allgemeine Anfragen│      │
│  │ Für: Projektplanung│  │ +49 9621 4759-0    │      │
│  │ +49 170 3733988    │  │ info@korodur.de    │      │
│  │ [Anrufen]          │  │ [Kontakt]          │      │
│  └────────────────────┘  └────────────────────┘      │
└─────────────────────────────────────────────────────┘
```

- ARM `.berater-grid` / `.berater-card` Klassen
- `.berater-img` 120px circle, `border: 3px solid var(--secondary)`
- Benjamin Lorenz: "Für konkrete Projekte und technische Fragen"
- KORODUR Zentrale: "Allgemeine Produktinformationen und Beratung"

### 2.13 Footer → Vereinfacht (User-Feedback)
**ENTFERNEN:**
- Normen-Zeile
- Zementhinweis
- Stand/Datenquelle

**Beibehalten (ARM-Style):**
```
┌─────────────────────────────────────────────────────┐
│ KORODUR                                               │
│ KORODUR International GmbH                            │
│ Wernher-von-Braun-Str. 4 · 92224 Amberg              │
│                                                        │
│ Impressum  Datenschutz  MICROTOP  korodur.de          │
└─────────────────────────────────────────────────────┘
```

- `.footer-compact` Layout
- `.footer-brand` in uppercase, weight 900

### 2.14 Sticky CTA (Mobile) → Bleibt
- Benjamin Lorenz Nummer für Mobile Sticky
- ARM Cookie Banner hinzufügen

### 2.15 Cookie Banner → NEU (von ARM übernehmen)
```
┌────────────────────────────────────────────────────┐
│ Diese Seite verwendet Cookies...  [Akzeptieren] [Ablehnen] │
└────────────────────────────────────────────────────┘
```

---

## 3. Inline-CTAs → ARM-Style anpassen
**Aktuell:** Eigene `.inline-cta` Klasse
**Ziel:** Beibehalten aber CTA-Text anpassen

- Nach Referenzen: "Ihr Projekt besprechen? Rufen Sie uns an: +49 9621 4759-0" (allgemeiner Kontakt)
- Nach Produktfinder: "Nicht sicher? Wir helfen: +49 9621 4759-0"
- Benjamin Lorenz NUR in der Berater-Sektion

---

## 4. Wartet auf User-Input

| Element | Status | Aktion |
|---------|--------|--------|
| Header-Logo (Bild-Datei) | AUSSTEHEND | User liefert Logo-PNG/SVG |
| 3 Verfahren-Bilder (neu) | AUSSTEHEND | User liefert bessere Fotos |

**Kann sofort umgesetzt werden:** Alles andere (15 von 17 Änderungen)

---

## 5. Umsetzungsreihenfolge

1. **CSS komplett neu** → ARM Design-System übernehmen (Variables, Reset, Typo, Buttons, Utility-Klassen)
2. **Header** → ARM-Style (Text-Logo als Fallback bis Bild kommt)
3. **Hero** → Heller Gradient + Key-Figures Cards + Mini Trust Bar
4. **Problem** → Section-Toggle Pattern
5. **Lösung** → Full-width
6. **Benefits** → CSS-Update (ARM Shadows/Farben)
7. **Referenzen** → 2-Spalter, mehr Links, Toggle-Liste mit "aktuell in Sanierung"
8. **Verfahren** → H2 full-width fix, Platzhalter-Bilder
9. **Produktfinder** → Datenblatt-Links, ARM table styling
10. **Vergleich** → ARM comparison-table + Mobile Cards
11. **DVGW** → Prominenter
12. **FAQ** → ARM FAQ Style
13. **CTA** → Zweigeteilt (Benjamin + KORODUR Zentrale), ARM berater-cards
14. **Footer** → Vereinfacht, ARM-Style
15. **Cookie Banner** → NEU
16. **JS** → Section-Toggle, FAQ, Ref-Toggle, Sticky CTA, Cookie, Mobile Menu

---

## 6. Zusammenfassung der Änderungen

| Kategorie | Anzahl |
|-----------|--------|
| Design-System (CSS) | Komplett neu nach ARM |
| Struktur-Änderungen | 6 (Header, Hero, Problem-Toggle, CTA-Split, Footer, Cookie) |
| Content-Änderungen | 4 (mehr Ref-Links, Produktfinder-Links, CTA-Text, MICROTOP fett) |
| Bug-Fixes | 2 (Verfahren H2 Breite, Lösung full-width) |
| Wartet auf User | 2 (Logo-Bild, Verfahren-Fotos) |

**Geschätzter Umfang:** ~900-1100 Zeilen HTML (Single-File, komplett neu geschrieben nach ARM-Vorlage)
