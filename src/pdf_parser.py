"""Extract product data from MicroTop TW PDF datasheets using PyMuPDF."""

from __future__ import annotations

import logging
import re
from pathlib import Path

import fitz  # PyMuPDF

from src.config import PDF_PRODUCT_MAP
from src.models import MicroTopProduct

logger = logging.getLogger(__name__)


def _clean(text: str) -> str:
    """Normalize whitespace."""
    return re.sub(r"\s+", " ", text).strip()


def _extract_sections(text: str) -> dict[str, str]:
    """Split PDF text into named sections (BESCHREIBUNG, TECHNISCHE DATEN, etc.)."""
    section_headers = [
        "BESCHREIBUNG", "ANWENDUNG", "EIGENSCHAFTEN", "TECHNISCHE DATEN",
        "VERARBEITUNG", "NACHBEHANDLUNG", "LIEFERFORM", "LAGERUNG",
        "ERGÄNZENDE HINWEISE",
    ]
    pattern = r"(?:^|\n)\s*(" + "|".join(section_headers) + r")\s*\n?"
    parts = re.split(pattern, text, flags=re.IGNORECASE)

    sections: dict[str, str] = {}
    i = 1
    while i < len(parts) - 1:
        header = parts[i].strip().upper()
        body = parts[i + 1].strip()
        sections[header] = body
        i += 2
    return sections


def _extract_properties(text: str) -> list[str]:
    """Extract bullet-point properties from EIGENSCHAFTEN section."""
    props = []
    for line in text.split("\n"):
        line = line.strip()
        if line.startswith("•") or line.startswith("·") or line.startswith("-"):
            props.append(_clean(line.lstrip("•·- ")))
        elif line and not line[0].isupper():
            props.append(_clean(line))
    return [p for p in props if p]


def _extract_tech_value(tech_text: str, key: str) -> str:
    """Extract a value for a given key from TECHNISCHE DATEN text."""
    # Try to find the key and capture text after it until the next key or end
    pattern = rf"{re.escape(key)}\s*[:\s]*(.*?)(?=\n[A-ZÄÖÜ]|\Z)"
    m = re.search(pattern, tech_text, re.IGNORECASE | re.DOTALL)
    if m:
        return _clean(m.group(1))
    return ""


def _parse_tw358_variants(text: str, sections: dict[str, str]) -> list[MicroTopProduct]:
    """Parse the TW 3/5/8 combined PDF into 3 separate products."""
    tech = sections.get("TECHNISCHE DATEN", "")
    products = []

    # Shared data
    shared = {
        "beschreibung": _clean(sections.get("BESCHREIBUNG", "")),
        "anwendung": _clean(sections.get("ANWENDUNG", "")),
        "eigenschaften": _extract_properties(sections.get("EIGENSCHAFTEN", "")),
        "qualitaet": "C 30/37",
        "temperatur": "≥ 5 °C",
        "wz_wert": "≤ 0,5",
        "dvgw": "Typ Klasse 1, W 300, W 347",
        "verfahren": "Trockenspritzverfahren (Dünnstrom)",
        "stand": "08/2020",
        "hat_zementhinweis": True,
        "lieferform": "25 kg Papierspezialverpackung",
        "lagerung": "Trocken lagern, wie Zement. Haltbarkeitsdauer ca. 12 Monate.",
        "pdf_file": "MICROTOP_TW_3_5_8_de.pdf",
    }

    # Verarbeitung sections
    verarb_text = sections.get("VERARBEITUNG", "")
    untergrund = ""
    verarbeitung = ""
    if "Untergrund" in verarb_text:
        parts = verarb_text.split("Verarbeitung", 1) if "Verarbeitung" in verarb_text else [verarb_text]
        untergrund = _clean(parts[0].replace("Untergrund", "", 1))
        if len(parts) > 1:
            verarbeitung = _clean(parts[1])
    nachbehandlung = _clean(sections.get("NACHBEHANDLUNG", ""))

    variants = [
        {
            "name": "MICROTOP TW 3",
            "subtitle": "Microsilica-Spritzmörtel Körnung 0 - 3 mm",
            "koernung": "0 - 3 mm",
            "farbe": "natur, weiß",
            "dichte": "ca. 2,24 kg/l",
            "wasserzugabe": "ca. 2,5 l/25 kg Gebinde",
            "schichtstaerke": "ca. 9 - 20 mm",
        },
        {
            "name": "MICROTOP TW 5",
            "subtitle": "Microsilica-Spritzmörtel Körnung 0 - 5 mm",
            "koernung": "0 - 5 mm",
            "farbe": "natur",
            "dichte": "ca. 2,25 kg/l",
            "wasserzugabe": "ca. 2,3 l/25 kg Gebinde",
            "schichtstaerke": "ca. 14 - 30 mm",
        },
        {
            "name": "MICROTOP TW 8",
            "subtitle": "Microsilica-Spritzbeton Körnung 0 - 8 mm",
            "koernung": "0 - 8 mm",
            "farbe": "natur",
            "dichte": "ca. 2,27 kg/l",
            "wasserzugabe": "ca. 2,2 l/25 kg Gebinde",
            "schichtstaerke": "≥ 25 mm",
        },
    ]

    for v in variants:
        p = MicroTopProduct(**shared)
        for k, val in v.items():
            setattr(p, k, val)
        p.untergrund = untergrund
        p.verarbeitung = verarbeitung
        p.nachbehandlung = nachbehandlung
        products.append(p)

    return products


def _parse_single_product(
    name: str,
    text: str,
    sections: dict[str, str],
    pdf_file: str,
) -> MicroTopProduct:
    """Parse a single-product PDF into a MicroTopProduct."""
    tech = sections.get("TECHNISCHE DATEN", "")

    p = MicroTopProduct(name=name)
    p.pdf_file = pdf_file
    p.beschreibung = _clean(sections.get("BESCHREIBUNG", ""))
    p.anwendung = _clean(sections.get("ANWENDUNG", ""))
    p.eigenschaften = _extract_properties(sections.get("EIGENSCHAFTEN", ""))
    p.lieferform = _clean(sections.get("LIEFERFORM", ""))
    p.lagerung = _clean(sections.get("LAGERUNG", ""))
    p.nachbehandlung = _clean(sections.get("NACHBEHANDLUNG", ""))

    # Verarbeitung split
    verarb_text = sections.get("VERARBEITUNG", "")
    if "Untergrund" in verarb_text and "Verarbeitung" in verarb_text:
        parts = verarb_text.split("Verarbeitung", 1)
        p.untergrund = _clean(parts[0].replace("Untergrund", "", 1))
        p.verarbeitung = _clean(parts[1])
    elif verarb_text:
        p.verarbeitung = _clean(verarb_text)

    # Product-specific tech data
    if name == "MICROTOP TW NSM":
        p.subtitle = "Microsilica-Spritzmörtel für das Nassspritzverfahren"
        p.qualitaet = "C 30/37"
        p.koernung = "0 - 3 mm"
        p.farbe = "natur, weiß, blau"
        p.temperatur = "≥ 5 °C"
        p.wz_wert = "ca. 0,14 - 0,15"
        p.wasserzugabe = "ca. 3,6 l/25 kg Gebinde"
        p.schichtstaerke = "ca. 20 mm (einlagig)"
        p.dvgw = "Typ Klasse 1, W 300, W 347"
        p.verfahren = "Nassspritzverfahren (Dichtstrom)"
        p.stand = "08/2020"
        p.hat_zementhinweis = True

    elif name == "MICROTOP TW BM":
        p.subtitle = "Beschichtungsmörtel für Trinkwasserrohre und -behälter"
        p.qualitaet = "C 30/37"
        p.koernung = "0 - 1 mm"
        p.farbe = "natur"
        p.dichte = "ca. 2,11 kg/l"
        p.druckfestigkeit = "≥ 35 N/mm²"
        p.biegezugfestigkeit = "≥ 6 N/mm²"
        p.temperatur = "≥ 5 °C"
        p.wz_wert = "≤ 0,5"
        p.wasserzugabe = "ca. 5 - 6,25 l/25 kg Gebinde"
        p.schichtstaerke = "ca. 5 - 8 mm"
        p.dvgw = "Typ Klasse 1, W 300, W 347"
        p.verfahren = "Schleuder-, Spritz- und Handauftrag"
        p.stand = "08/2020"
        p.hat_zementhinweis = True

    elif name == "MICROTOP TW VSM":
        p.subtitle = "Vorspritzmörtel für Trinkwasserbehälter"
        p.qualitaet = "C 12/15"
        p.koernung = "0 - 2 mm"
        p.farbe = "natur"
        p.dichte = "ca. 1,98 kg/l"
        p.temperatur = "≥ 5 °C"
        p.wz_wert = "≤ 0,5"
        p.wasserzugabe = "ca. 3,75 l/25 kg Gebinde"
        p.schichtstaerke = "ca. 15 - 20 mm"
        p.ergiebigkeit = "ca. 14 l/25 kg Gebinde"
        p.dvgw = "Typ Klasse 1, W 347"
        p.verfahren = "Spritz-/Handauftrag"
        p.stand = "08/2020"
        p.hat_zementhinweis = True

    elif name == "MICROTOP TW Mineral":
        p.subtitle = "Flüssige Oberflächenvergütung auf Silikatbasis"
        p.form = "flüssig"
        p.farbe = "transparent"
        p.dichte = "1,14 g/cm³"
        p.viskositaet = "ca. 100 mPas"
        p.ph_wert = "ca. 11,3"
        p.materialverbrauch = "ca. 150 - 250 g/m²"
        p.dvgw = "DVGW-geeignet"
        p.verfahren = "Pinsel / Niederdruck-Spritzgerät"
        p.stand = "11/2020"
        p.hat_zementhinweis = False
        p.lieferform = "20 kg Kunststoffgebinde"
        p.lagerung = "Trocken und frostfrei im verschlossenen Originalgebinde lagern. Haltbarkeitsdauer ca. 12 Monate."

    elif name == "MICROTOP TW 02":
        p.subtitle = "Korrosionsschutz, Haftbrücke und Spachtel"
        p.qualitaet = "C 30/37"
        p.koernung = "0 - 0,2 mm"
        p.farbe = "natur"
        p.dichte = "ca. 2,04 kg/l"
        p.temperatur = "≥ 5 °C"
        p.wz_wert = "≤ 0,4 - ≤ 0,5"
        p.wasserzugabe = "ca. 5 - 6,25 l/25 kg Gebinde"
        p.schichtstaerke = "ca. 2 - 5 mm"
        p.dvgw = "Typ Klasse 1, W 300, W 347"
        p.verfahren = "Nassspritzdichtstrom / Spachteltechnik"
        p.stand = "09/2021"
        p.hat_zementhinweis = True

    return p


def parse_pdf(pdf_path: Path) -> list[MicroTopProduct]:
    """Parse a MicroTop TW PDF and return product data."""
    filename = pdf_path.name
    if filename not in PDF_PRODUCT_MAP:
        logger.warning(f"Unknown PDF: {filename}")
        return []

    product_names = PDF_PRODUCT_MAP[filename]
    logger.info(f"Parsing {filename} -> {product_names}")

    doc = fitz.open(str(pdf_path))
    text = ""
    for page in doc:
        text += page.get_text() + "\n"
    doc.close()

    sections = _extract_sections(text)
    logger.debug(f"  Sections found: {list(sections.keys())}")

    # Multi-variant PDF (TW 3/5/8)
    if len(product_names) > 1:
        return _parse_tw358_variants(text, sections)

    # Single-product PDF
    return [_parse_single_product(product_names[0], text, sections, filename)]


def parse_all_pdfs(pdf_dir: Path) -> dict[str, MicroTopProduct]:
    """Parse all PDFs in directory, return dict keyed by product name."""
    products: dict[str, MicroTopProduct] = {}

    for pdf_file in sorted(pdf_dir.glob("*.pdf")):
        for product in parse_pdf(pdf_file):
            products[product.name] = product
            logger.info(f"  OK {product.name}: Koernung={product.koernung}, "
                        f"Schicht={product.schichtstaerke}, DVGW={product.dvgw}")

    logger.info(f"Parsed {len(products)} products from {len(list(pdf_dir.glob('*.pdf')))} PDFs")
    return products
