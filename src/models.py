"""Product data model for MicroTop TW products."""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class MicroTopProduct:
    """All technical data for one MicroTop TW product."""

    name: str = ""
    subtitle: str = ""          # Kurzbeschreibung from PDF header
    beschreibung: str = ""
    anwendung: str = ""

    # Technische Daten
    qualitaet: str = ""         # e.g. "C 30/37"
    koernung: str = ""          # e.g. "0 - 3 mm"
    farbe: str = ""             # e.g. "natur, weiß"
    dichte: str = ""            # e.g. "ca. 2,24 kg/l"
    druckfestigkeit: str = ""   # e.g. "≥ 35 N/mm²"
    biegezugfestigkeit: str = ""
    temperatur: str = ""        # e.g. "≥ 5 °C"
    wz_wert: str = ""           # Wasser/Zementwert
    wasserzugabe: str = ""
    schichtstaerke: str = ""    # e.g. "ca. 9 - 20 mm"
    materialverbrauch: str = "" # for Mineral
    ergiebigkeit: str = ""      # for VSM
    viskositaet: str = ""       # for Mineral
    ph_wert: str = ""           # for Mineral
    form: str = ""              # for Mineral: "flüssig"

    # Verfahren
    verfahren: str = ""         # Trockenspritz, Nassspritz, Schleuder, etc.

    # Normen / Zulassungen
    dvgw: str = ""              # e.g. "Typ Klasse 1, W 300, W 347"
    normen: list[str] = field(default_factory=list)

    # Eigenschaften (bullet points)
    eigenschaften: list[str] = field(default_factory=list)

    # Verarbeitung
    untergrund: str = ""
    verarbeitung: str = ""
    nachbehandlung: str = ""

    # Lieferform / Lagerung
    lieferform: str = ""
    lagerung: str = ""

    # Metadata
    stand: str = ""             # e.g. "08/2020"
    hat_zementhinweis: bool = False
    pdf_file: str = ""
    notion_page_id: str = ""
