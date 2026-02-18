"""Update MicroTop product properties in Notion DB."""

from __future__ import annotations

import logging
import os

from notion_client import Client

from src.config import PRODUCT_PAGES
from src.models import MicroTopProduct

logger = logging.getLogger(__name__)

# Mapping: MicroTopProduct field -> Notion property name (actual DB schema)
# Properties are rich_text unless noted otherwise
FIELD_TO_RICH_TEXT = {
    "koernung": "Koernung",
    "dichte": "Dichte",
    "druckfestigkeit": "Druckfestigkeit",
    "biegezugfestigkeit": "Biegezugfestigkeit",
    "materialverbrauch": "Materialverbrauch",
    "qualitaet": "Qualitaet (Norm)",
    "stand": "Stand",
    "beschreibung": "Produktbeschreibung",
    "dvgw": "Prüfzeugnisse und Zertifikate",
}

# These properties exist but are already filled for most products, skip them:
# Farbe (techn.) = select type, not rich_text
# Lieferform, Lagerung, Nachbehandlung = already filled


def _make_rich_text_prop(value: str) -> dict:
    return {"rich_text": [{"type": "text", "text": {"content": value}}]}


def update_products(
    products: dict[str, MicroTopProduct],
    existing: dict[str, dict],
    dry_run: bool = False,
    notion_token: str | None = None,
) -> int:
    """Update Notion DB entries with data from PDFs.

    Only updates properties that are currently empty in Notion.
    Returns number of properties updated.
    """
    token = notion_token or os.environ.get("NOTION_TOKEN")
    if not token:
        raise ValueError("NOTION_TOKEN not set")

    notion = Client(auth=token) if not dry_run else None
    total_updates = 0

    for name, product in products.items():
        page_id = PRODUCT_PAGES.get(name)
        if not page_id:
            logger.warning(f"  No Notion page ID for {name}, skipping")
            continue

        existing_props = existing.get(name, {}).get("properties", {})
        updates: dict[str, dict] = {}

        for field_name, notion_prop in FIELD_TO_RICH_TEXT.items():
            value = getattr(product, field_name, "")
            if not value:
                continue
            # Only update if the property is currently empty
            if existing_props.get(notion_prop):
                continue
            updates[notion_prop] = _make_rich_text_prop(value)

        if not updates:
            logger.info(f"  {name}: nothing to update")
            continue

        logger.info(f"  {name}: updating {len(updates)} properties: {list(updates.keys())}")
        total_updates += len(updates)

        if dry_run:
            for prop, val in updates.items():
                text = val["rich_text"][0]["text"]["content"]
                logger.info(f"    [DRY-RUN] {prop} = {text}")
        else:
            try:
                notion.pages.update(page_id=page_id, properties=updates)
                logger.info(f"    OK Updated in Notion")
            except Exception as e:
                logger.error(f"    FAIL: {e}")

    logger.info(f"Total: {total_updates} property updates")
    return total_updates
