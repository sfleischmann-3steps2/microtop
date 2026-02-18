"""Read existing MicroTop product data from Notion DB."""

from __future__ import annotations

import logging
import os

from notion_client import Client

from src.config import PRODUCT_PAGES

logger = logging.getLogger(__name__)


def _get_text_prop(props: dict, key: str) -> str:
    """Extract text from a rich_text property."""
    prop = props.get(key, {})
    ptype = prop.get("type", "")
    if ptype == "rich_text":
        parts = prop.get("rich_text", [])
        return "".join(p.get("plain_text", "") for p in parts)
    if ptype == "title":
        parts = prop.get("title", [])
        return "".join(p.get("plain_text", "") for p in parts)
    if ptype == "number":
        val = prop.get("number")
        return str(val) if val is not None else ""
    if ptype == "select":
        sel = prop.get("select")
        return sel.get("name", "") if sel else ""
    return ""


def read_all_products(notion_token: str | None = None) -> dict[str, dict]:
    """Read all 8 MicroTop products from Notion DB.

    Returns dict keyed by product name with their current property values.
    """
    token = notion_token or os.environ.get("NOTION_TOKEN")
    if not token:
        raise ValueError("NOTION_TOKEN not set")

    notion = Client(auth=token)
    results: dict[str, dict] = {}

    for name, page_id in PRODUCT_PAGES.items():
        try:
            page = notion.pages.retrieve(page_id=page_id)
            props = page.get("properties", {})

            data = {
                "page_id": page_id,
                "properties": {},
            }

            # Extract all known properties
            for prop_name in props:
                val = _get_text_prop(props, prop_name)
                if val:
                    data["properties"][prop_name] = val

            results[name] = data
            filled = len(data["properties"])
            logger.info(f"  {name}: {filled} properties filled")

        except Exception as e:
            logger.error(f"  Failed to read {name} ({page_id}): {e}")

    logger.info(f"Read {len(results)}/{len(PRODUCT_PAGES)} products from Notion")
    return results
