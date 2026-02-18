"""Build the MicroTop TW comparison page as Notion blocks (v2)."""

from __future__ import annotations

import logging
from datetime import datetime

from src.config import (
    ALL_PRODUCTS,
    CEMENT_PRODUCTS,
    GROUP_KOERNUNG,
    GROUP_SPEZIALPRODUKTE,
    GROUP_SPEZIALVERFAHREN,
    PRODUCT_PAGES,
)
from src.models import MicroTopProduct

logger = logging.getLogger(__name__)


# ── Notion Block Helpers ──────────────────────────────────────────────

def _rt(content: str, **annotations) -> dict:
    """Create a rich text element."""
    rt: dict = {"type": "text", "text": {"content": content}}
    if annotations:
        rt["annotations"] = annotations
    return rt


def _mention_page(page_id: str) -> dict:
    """Create a page mention rich text element."""
    return {
        "type": "mention",
        "mention": {"type": "page", "page": {"id": page_id}},
    }


def _cell(*rich_texts) -> list:
    """Create a table cell (list of rich text elements)."""
    return list(rich_texts)


def _heading2(text: str) -> dict:
    return {
        "object": "block",
        "type": "heading_2",
        "heading_2": {"rich_text": [_rt(text)]},
    }


def _heading3(text: str) -> dict:
    return {
        "object": "block",
        "type": "heading_3",
        "heading_3": {"rich_text": [_rt(text)]},
    }


def _paragraph(*rich_texts) -> dict:
    return {
        "object": "block",
        "type": "paragraph",
        "paragraph": {"rich_text": list(rich_texts)},
    }


def _bullet(text: str, **annotations) -> dict:
    return {
        "object": "block",
        "type": "bulleted_list_item",
        "bulleted_list_item": {"rich_text": [_rt(text, **annotations)]},
    }


def _callout(rich_texts: list[dict], emoji: str, color: str) -> dict:
    return {
        "object": "block",
        "type": "callout",
        "callout": {
            "rich_text": rich_texts,
            "icon": {"type": "emoji", "emoji": emoji},
            "color": color,
        },
    }


def _divider() -> dict:
    return {"object": "block", "type": "divider", "divider": {}}


def _table(width: int, rows: list[dict], has_header: bool = True) -> dict:
    return {
        "object": "block",
        "type": "table",
        "table": {
            "table_width": width,
            "has_column_header": has_header,
            "has_row_header": False,
            "children": rows,
        },
    }


def _table_row(cells: list[list]) -> dict:
    return {"type": "table_row", "table_row": {"cells": cells}}


def _toggle_heading3(text: str, children: list[dict]) -> dict:
    return {
        "object": "block",
        "type": "heading_3",
        "heading_3": {
            "rich_text": [_rt(text)],
            "is_toggleable": True,
            "children": children,
        },
    }


def _image_placeholder(label: str) -> dict:
    """Callout placeholder for an image to be added manually later."""
    return _callout(
        [_rt(f"[BILD: {label}]\n", bold=True),
         _rt("Hier manuell Produktfoto / Anwendungsbild einfügen.", italic=True, color="gray")],
        "📷", "gray_background",
    )


# ── Section Builders ──────────────────────────────────────────────────

def _build_hero() -> list[dict]:
    """Section 1: Hero with image placeholder."""
    return [
        _image_placeholder("MICROTOP TW Produktfamilie — Gebinde-Übersicht"),
        _callout(
            [
                _rt("MICROTOP TW\n", bold=True),
                _rt("Beschichtungsmörtel & Oberflächenschutz für Trinkwasseranlagen\n\n", italic=True),
                _rt("8 DVGW-zugelassene Produkte für Behälter, Rohre und Flächen — "
                     "von der Vorspritzung über den Hauptauftrag bis zur Oberflächenvergütung."),
            ],
            "💧", "blue_background",
        ),
    ]


def _build_problem() -> list[dict]:
    """Section 2: Problem statement."""
    return [
        _heading2("DAS KENNEN SIE"),
        _callout(
            [
                _rt("Korrodierte Trinkwasserbehälter. Abblätternde Beschichtungen. "
                     "Hygienische Beanstandungen bei der Trinkwasserprüfung. "
                     "Aufwändige Sanierungen mit langen Ausfallzeiten — "
                     "und die Frage: Welches Material ist das richtige?"),
            ],
            "⚠️", "orange_background",
        ),
    ]


def _build_solution() -> list[dict]:
    """Section 3: Solution statement."""
    return [
        _heading2("DIE LÖSUNG"),
        _callout(
            [
                _rt("MICROTOP TW — ", bold=True),
                _rt("ein System aus 8 aufeinander abgestimmten Produkten. "
                     "Alle DVGW-zugelassen nach W 300 / W 347. "
                     "Für jeden Arbeitsschritt das richtige Produkt: "
                     "vom Vorspritzen über den Hauptauftrag bis zur Oberflächenvergütung."),
            ],
            "✅", "green_background",
        ),
    ]


# FIX 1: Schichtdicke-Spalte in Entscheidungstabelle
def _build_decision_table(products: dict[str, MicroTopProduct]) -> list[dict]:
    """Section 4: Decision helper with Schichtdicke column."""
    blocks = [_heading2("DAS RICHTIGE PRODUKT FINDEN")]

    rows = [
        _table_row([
            _cell(_rt("Ihr Bedarf", bold=True)),
            _cell(_rt("Produkt", bold=True)),
            _cell(_rt("Schichtdicke", bold=True)),
            _cell(_rt("Verfahren", bold=True)),
        ]),
        _table_row([
            _cell(_rt("Hauptbeschichtung (dünn, fein)")),
            _cell(_rt("TW 3", bold=True)),
            _cell(_rt("9 – 20 mm")),
            _cell(_rt("Trockenspritzen")),
        ]),
        _table_row([
            _cell(_rt("Hauptbeschichtung (mittel)")),
            _cell(_rt("TW 5", bold=True)),
            _cell(_rt("14 – 30 mm")),
            _cell(_rt("Trockenspritzen")),
        ]),
        _table_row([
            _cell(_rt("Reprofilierung (stark, dick)")),
            _cell(_rt("TW 8", bold=True)),
            _cell(_rt("≥ 25 mm")),
            _cell(_rt("Trockenspritzen")),
        ]),
        _table_row([
            _cell(_rt("Hauptbeschichtung, staubarm")),
            _cell(_rt("TW NSM", bold=True)),
            _cell(_rt("ca. 20 mm")),
            _cell(_rt("Nassspritzen")),
        ]),
        _table_row([
            _cell(_rt("Rohre + Behälter auskleiden")),
            _cell(_rt("TW BM", bold=True)),
            _cell(_rt("5 – 8 mm")),
            _cell(_rt("Schleudern / Spritzen / Hand")),
        ]),
        _table_row([
            _cell(_rt("Vorspritzen (Haftgrund)")),
            _cell(_rt("TW VSM", bold=True)),
            _cell(_rt("15 – 20 mm")),
            _cell(_rt("Spritzen / Hand")),
        ]),
        _table_row([
            _cell(_rt("Korrosionsschutz / Haftbrücke")),
            _cell(_rt("TW 02", bold=True)),
            _cell(_rt("2 – 5 mm")),
            _cell(_rt("Spritzen / Spachteln")),
        ]),
        _table_row([
            _cell(_rt("Oberflächenvergütung")),
            _cell(_rt("TW Mineral", bold=True)),
            _cell(_rt("150 – 250 g/m²")),
            _cell(_rt("Pinsel / Sprühen")),
        ]),
    ]

    blocks.append(_table(4, rows))
    return blocks


# FIX 5: Headings ohne repetitives "VERGLEICH:" Prefix
def _build_comparison_koernung(products: dict[str, MicroTopProduct]) -> list[dict]:
    """Section 5: Comparison table for TW 3/5/8."""
    blocks = [_heading2("Körnungsvarianten (TW 3 · TW 5 · TW 8)")]
    blocks.append(_paragraph(
        _rt("Trockenspritz-Mörtel für die Hauptbeschichtung — "
            "drei Körnungen für unterschiedliche Schichtdicken.", italic=True),
    ))
    blocks.append(_image_placeholder("Anwendungsfoto Trockenspritzverfahren im Behälter"))

    header = _table_row([
        _cell(_rt("Eigenschaft", bold=True)),
        _cell(_rt("TW 3", bold=True)),
        _cell(_rt("TW 5", bold=True)),
        _cell(_rt("TW 8", bold=True)),
    ])

    def _val(name: str, field: str) -> str:
        p = products.get(name)
        return getattr(p, field, "—") if p else "—"

    rows = [header]
    specs = [
        ("Körnung", "koernung"),
        ("Qualität", "qualitaet"),
        ("Schichtdicke", "schichtstaerke"),
        ("Farbe", "farbe"),
        ("Dichte", "dichte"),
        ("DVGW", "dvgw"),
    ]
    for label, field in specs:
        rows.append(_table_row([
            _cell(_rt(label, bold=True)),
            *[_cell(_rt(_val(n, field) or "—")) for n in GROUP_KOERNUNG],
        ]))

    blocks.append(_table(4, rows))
    return blocks


# FIX 2: Nur Zeilen mit mindestens einem echten Wert (nicht nur "—")
def _build_comparison_spezialverfahren(products: dict[str, MicroTopProduct]) -> list[dict]:
    """Section 6: Comparison table for NSM/BM/VSM."""
    blocks = [_heading2("Spezialverfahren (TW NSM · TW BM · TW VSM)")]
    blocks.append(_paragraph(
        _rt("Nassspritzen, Schleudern, Vorspritzen — "
            "drei Produkte für spezielle Anwendungen.", italic=True),
    ))
    blocks.append(_image_placeholder("Anwendungsfoto Nassspritz- oder Schleuderverfahren"))

    header = _table_row([
        _cell(_rt("Eigenschaft", bold=True)),
        _cell(_rt("TW NSM", bold=True)),
        _cell(_rt("TW BM", bold=True)),
        _cell(_rt("TW VSM", bold=True)),
    ])

    def _val(name: str, field: str) -> str:
        p = products.get(name)
        return getattr(p, field, "") if p else ""

    rows = [header]
    specs = [
        ("Verfahren", "verfahren"),
        ("Körnung", "koernung"),
        ("Qualität", "qualitaet"),
        ("Schichtdicke", "schichtstaerke"),
        ("Farbe", "farbe"),
        ("Druckfestigkeit", "druckfestigkeit"),
        ("Biegezugfestigkeit", "biegezugfestigkeit"),
        ("DVGW", "dvgw"),
    ]
    for label, field in specs:
        vals = [_val(n, field) for n in GROUP_SPEZIALVERFAHREN]
        # FIX 2: Skip rows where fewer than 2 products have values
        filled_count = sum(1 for v in vals if v)
        if filled_count < 2:
            continue
        rows.append(_table_row([
            _cell(_rt(label, bold=True)),
            *[_cell(_rt(v or "—")) for v in vals],
        ]))

    blocks.append(_table(4, rows))
    return blocks


def _build_comparison_spezialprodukte(products: dict[str, MicroTopProduct]) -> list[dict]:
    """Section 7: Comparison table for Mineral/02."""
    blocks = [_heading2("Spezialprodukte (TW Mineral · TW 02)")]
    blocks.append(_paragraph(
        _rt("Oberflächenvergütung und Korrosionsschutz — "
            "zwei Ergänzungsprodukte für besondere Anforderungen.", italic=True),
    ))

    header = _table_row([
        _cell(_rt("Eigenschaft", bold=True)),
        _cell(_rt("TW Mineral", bold=True)),
        _cell(_rt("TW 02", bold=True)),
    ])

    mineral = products.get("MICROTOP TW Mineral")
    tw02 = products.get("MICROTOP TW 02")

    rows = [header]
    rows.append(_table_row([
        _cell(_rt("Anwendung", bold=True)),
        _cell(_rt(mineral.subtitle if mineral else "—")),
        _cell(_rt(tw02.subtitle if tw02 else "—")),
    ]))
    rows.append(_table_row([
        _cell(_rt("Form / Körnung", bold=True)),
        _cell(_rt(mineral.form if mineral else "—")),
        _cell(_rt(f"Körnung {tw02.koernung}" if tw02 else "—")),
    ]))
    rows.append(_table_row([
        _cell(_rt("Verfahren", bold=True)),
        _cell(_rt(mineral.verfahren if mineral else "—")),
        _cell(_rt(tw02.verfahren if tw02 else "—")),
    ]))
    rows.append(_table_row([
        _cell(_rt("Schichtdicke / Verbrauch", bold=True)),
        _cell(_rt(mineral.materialverbrauch if mineral else "—")),
        _cell(_rt(tw02.schichtstaerke if tw02 else "—")),
    ]))
    rows.append(_table_row([
        _cell(_rt("Farbe", bold=True)),
        _cell(_rt(mineral.farbe if mineral else "—")),
        _cell(_rt(tw02.farbe if tw02 else "—")),
    ]))
    rows.append(_table_row([
        _cell(_rt("DVGW", bold=True)),
        _cell(_rt(mineral.dvgw if mineral else "—")),
        _cell(_rt(tw02.dvgw if tw02 else "—")),
    ]))

    blocks.append(_table(3, rows))
    return blocks


def _build_dvgw() -> list[dict]:
    """Section 8: DVGW certifications."""
    return [
        _heading2("DVGW-ZULASSUNGEN"),
        _callout(
            [
                _rt("Alle MICROTOP TW Produkte sind DVGW-zugelassen\n\n", bold=True),
                _rt("TW 3 · TW 5 · TW 8 · TW NSM · TW BM · TW 02", bold=True),
                _rt("  →  Typ Klasse 1, W 300, W 347\n"),
                _rt("TW VSM", bold=True),
                _rt("  →  Typ Klasse 1, W 347\n"),
                _rt("TW Mineral", bold=True),
                _rt("  →  DVGW-geeignet für Trinkwasseranlagen\n\n"),
                _rt("Die DVGW-Zulassung bestätigt die hygienische Unbedenklichkeit "
                     "und Eignung für den Kontakt mit Trinkwasser.", italic=True),
            ],
            "🏅", "green_background",
        ),
    ]


# FIX 3: Gesamtübersicht als 2 Tabellen statt einer 9-spaltigen
def _build_full_comparison(products: dict[str, MicroTopProduct]) -> list[dict]:
    """Section 9: Toggle with two comparison tables (split for readability)."""

    def _val(name: str, field: str) -> str:
        p = products.get(name)
        v = getattr(p, field, "") if p else ""
        return v or "—"

    specs = [
        ("Körnung", "koernung"),
        ("Qualität", "qualitaet"),
        ("Schichtdicke", "schichtstaerke"),
        ("Farbe", "farbe"),
        ("Dichte", "dichte"),
        ("Verfahren", "verfahren"),
        ("W/Z-Wert", "wz_wert"),
        ("DVGW", "dvgw"),
        ("Lieferform", "lieferform"),
    ]

    # Table 1: Spritz-Mörtel (TW 3, 5, 8, NSM, BM, VSM)
    group1 = GROUP_KOERNUNG + GROUP_SPEZIALVERFAHREN
    header1 = _table_row([
        _cell(_rt("", bold=True)),
        *[_cell(_rt(n.replace("MICROTOP ", ""), bold=True)) for n in group1],
    ])
    rows1 = [header1]
    for label, field in specs:
        vals = [_val(n, field) for n in group1]
        if all(v == "—" for v in vals):
            continue
        rows1.append(_table_row([
            _cell(_rt(label, bold=True)),
            *[_cell(_rt(v)) for v in vals],
        ]))
    table1 = _table(len(group1) + 1, rows1)

    # Table 2: Spezialprodukte (Mineral, 02)
    header2 = _table_row([
        _cell(_rt("", bold=True)),
        *[_cell(_rt(n.replace("MICROTOP ", ""), bold=True)) for n in GROUP_SPEZIALPRODUKTE],
    ])
    rows2 = [header2]
    specs2 = [
        ("Form / Körnung", "koernung"),
        ("Farbe", "farbe"),
        ("Dichte", "dichte"),
        ("Verfahren", "verfahren"),
        ("DVGW", "dvgw"),
        ("Lieferform", "lieferform"),
    ]
    for label, field in specs2:
        vals = [_val(n, field) for n in GROUP_SPEZIALPRODUKTE]
        if all(v == "—" for v in vals):
            continue
        rows2.append(_table_row([
            _cell(_rt(label, bold=True)),
            *[_cell(_rt(v)) for v in vals],
        ]))
    table2 = _table(len(GROUP_SPEZIALPRODUKTE) + 1, rows2)

    return [
        _toggle_heading3("Technische Gesamtübersicht — Spritz-Mörtel", [table1]),
        _toggle_heading3("Technische Gesamtübersicht — Spezialprodukte", [table2]),
    ]


# FIX 6: Leistungsmerkmale als Bullet-Liste statt dense Callout
def _build_leistungsmerkmale(products: dict[str, MicroTopProduct]) -> list[dict]:
    """Section 10: Performance features as bullet list."""
    blocks = [_heading2("LEISTUNGSMERKMALE")]
    blocks.append(_paragraph(
        _rt("Die MICROTOP TW Produktfamilie vereint:", italic=True),
    ))

    features = [
        "Microsilica-vergütet — höchste Dichtigkeit und Festigkeit",
        "Wasserundurchlässig und wasserdampfdiffusionsoffen",
        "Chloridfrei — keine Korrosionsgefahr für Bewehrung",
        "Niedriger E-Modul — rissüberbrückend und spannungsarm",
        "Geringes Porenvolumen — minimale Angriffsfläche",
        "Gute Haftung an Beton und Stahl",
        "Korrosionshemmend",
        "Abreibfähig, glättbar und maschinell spritzbar",
    ]
    for f in features:
        blocks.append(_bullet(f))

    return blocks


def _build_normen() -> list[dict]:
    """Section 11: Standards."""
    return [
        _heading2("NORMEN & REGELWERKE"),
        _paragraph(
            _rt("DVGW Arbeitsblatt W 300 · W 347 · ", bold=True),
            _rt("DIN EN 13892-2 · DIN 18551 · DIN EN 13670 / DIN 1045-3\n"),
            _rt("DIN EN ISO 9001:2015 (Zertifiziertes Qualitätsmanagementsystem)", italic=True),
        ),
    ]


def _build_product_links() -> list[dict]:
    """Section 12: Page mentions to all 8 products."""
    blocks: list[dict] = [_heading2("PRODUKTE")]

    mentions: list[dict] = []
    for name in ALL_PRODUCTS:
        page_id = PRODUCT_PAGES.get(name)
        if page_id:
            if mentions:
                mentions.append(_rt("  ·  "))
            mentions.append(_mention_page(page_id))

    blocks.append(_paragraph(*mentions))
    return blocks


def _build_cta() -> list[dict]:
    """Section 13: Call to action."""
    return [
        _divider(),
        _callout(
            [
                _rt("INTERESSE?\n\n", bold=True),
                _rt("Lassen Sie sich beraten — wir finden das richtige MICROTOP TW Produkt "
                     "für Ihr Projekt.\n\n"),
                _rt("KORODUR International GmbH\n", bold=True),
                _rt("Tel. +49 (0) 9621 4759-0 · info@korodur.de · www.korodur.de"),
            ],
            "📞", "blue_background",
        ),
    ]


# FIX 7: Footer ohne "Pipeline"-Erwähnung
def _build_footer() -> list[dict]:
    """Section 14: Footer with cement notice and date."""
    cement_names = [n.replace("MICROTOP ", "") for n in CEMENT_PRODUCTS]

    return [
        _divider(),
        _paragraph(
            _rt("Zementhinweis: ", bold=True),
            _rt(f"Die Produkte {', '.join(cement_names)} enthalten Zement und reagieren "
                "mit Feuchtigkeit/Wasser alkalisch. Haut und Augen schützen. "
                "Bei Augenkontakt Arzt aufsuchen.",
                italic=True, color="gray"),
        ),
        _paragraph(
            _rt(f"Stand: {datetime.now().strftime('%d.%m.%Y')} · "
                f"Datenquelle: KORODUR Produktdatenblätter",
                italic=True, color="gray"),
        ),
    ]


# ── Main Builder ──────────────────────────────────────────────────────

def build_comparison_page(products: dict[str, MicroTopProduct]) -> list[dict]:
    """Build all Notion blocks for the MicroTop TW comparison page (v2).

    Returns a list of Notion block objects ready for pages.create().
    """
    blocks: list[dict] = []

    blocks.extend(_build_hero())
    blocks.extend(_build_problem())
    blocks.extend(_build_solution())
    blocks.append(_divider())
    blocks.extend(_build_decision_table(products))
    blocks.append(_divider())
    blocks.extend(_build_comparison_koernung(products))
    blocks.append(_divider())
    blocks.extend(_build_comparison_spezialverfahren(products))
    blocks.append(_divider())
    blocks.extend(_build_comparison_spezialprodukte(products))
    blocks.append(_divider())
    blocks.extend(_build_dvgw())
    blocks.extend(_build_full_comparison(products))
    blocks.extend(_build_leistungsmerkmale(products))
    blocks.extend(_build_normen())
    blocks.extend(_build_product_links())
    blocks.extend(_build_cta())
    blocks.extend(_build_footer())

    logger.info(f"Built {len(blocks)} blocks for comparison page")
    return blocks
