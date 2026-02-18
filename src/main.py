"""Orchestrator: Parse PDFs, update Notion DB, build comparison page."""

from __future__ import annotations

import argparse
import json
import logging
import os
import sys
from pathlib import Path

from dotenv import load_dotenv
from notion_client import Client

from src.config import ALL_PRODUCTS, PARENT_PAGE_ID, PRODUCT_PAGES
from src.models import MicroTopProduct
from src.notion_reader import read_all_products
from src.notion_updater import update_products
from src.page_builder import build_comparison_page
from src.pdf_parser import parse_all_pdfs

logger = logging.getLogger(__name__)


def _setup_logging(verbose: bool = False) -> None:
    import io
    level = logging.DEBUG if verbose else logging.INFO
    # Force UTF-8 on Windows to avoid cp1252 encoding errors
    stream = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
    logging.basicConfig(
        level=level,
        format="%(levelname)-8s %(message)s",
        stream=stream,
    )


def run_extract(pdf_dir: Path, dry_run: bool = False) -> dict[str, MicroTopProduct]:
    """Phase 2: Parse PDFs and update Notion DB."""
    logger.info("=== Phase 1: Parsing PDFs ===")
    products = parse_all_pdfs(pdf_dir)

    if not products:
        logger.error("No products parsed from PDFs!")
        return {}

    logger.info(f"\n=== Phase 2: Reading Notion DB ===")
    existing = read_all_products()

    logger.info(f"\n=== Phase 2: Updating Notion DB ===")
    update_products(products, existing, dry_run=dry_run)

    return products


def run_build_page(
    products: dict[str, MicroTopProduct],
    dry_run: bool = False,
) -> str | None:
    """Phase 3: Build and create the comparison page in Notion."""
    logger.info("\n=== Phase 3: Building comparison page ===")

    # Ensure we have all products
    missing = [n for n in ALL_PRODUCTS if n not in products]
    if missing:
        logger.warning(f"Missing products (will show '—' in tables): {missing}")

    blocks = build_comparison_page(products)
    logger.info(f"Generated {len(blocks)} blocks")

    if dry_run:
        logger.info("[DRY-RUN] Page blocks preview:")
        for i, block in enumerate(blocks):
            btype = block.get("type", "?")
            # Summarize block content
            if btype == "callout":
                texts = block["callout"]["rich_text"]
                preview = "".join(t.get("text", {}).get("content", "")[:50] for t in texts[:2])
                logger.info(f"  [{i:3d}] {btype}: {preview}...")
            elif btype in ("heading_2", "heading_3"):
                texts = block[btype]["rich_text"]
                preview = texts[0].get("text", {}).get("content", "") if texts else ""
                logger.info(f"  [{i:3d}] {btype}: {preview}")
            elif btype == "table":
                nrows = len(block["table"]["children"])
                ncols = block["table"]["table_width"]
                logger.info(f"  [{i:3d}] {btype}: {nrows} rows × {ncols} cols")
            elif btype == "divider":
                logger.info(f"  [{i:3d}] ────────")
            else:
                logger.info(f"  [{i:3d}] {btype}")

        # Also dump JSON for debugging
        json_path = Path("data/page_blocks.json")
        json_path.parent.mkdir(parents=True, exist_ok=True)
        with open(json_path, "w", encoding="utf-8") as f:
            json.dump(blocks, f, ensure_ascii=False, indent=2)
        logger.info(f"\nFull JSON written to {json_path}")
        return None

    # Create page in Notion
    token = os.environ.get("NOTION_TOKEN")
    if not token:
        raise ValueError("NOTION_TOKEN not set")

    notion = Client(auth=token)
    title = "MICROTOP TW — Produktvergleich Trinkwasserbeschichtungen"

    # Batch blocks (max 100 per request)
    first_batch = blocks[:100]
    remaining = blocks[100:]

    logger.info(f"Creating page: {title}")
    logger.info(f"  Parent: {PARENT_PAGE_ID}")
    logger.info(f"  Blocks: {len(blocks)} ({len(first_batch)} + {len(remaining)} remaining)")

    page = notion.pages.create(
        parent={"page_id": PARENT_PAGE_ID},
        properties={"title": [{"text": {"content": title}}]},
        children=first_batch,
    )

    page_id = page["id"]

    # Append remaining blocks
    while remaining:
        batch = remaining[:100]
        remaining = remaining[100:]
        logger.info(f"  Appending {len(batch)} blocks...")
        notion.blocks.children.append(block_id=page_id, children=batch)

    page_url = page.get("url", f"https://notion.so/{page_id.replace('-', '')}")
    logger.info(f"\nOK Page created: {page_url}")
    return page_url


def main() -> None:
    parser = argparse.ArgumentParser(description="MicroTop TW — Notion comparison page builder")
    parser.add_argument("--extract", action="store_true", help="Parse PDFs and update Notion DB")
    parser.add_argument("--build-page", action="store_true", help="Build comparison page in Notion")
    parser.add_argument("--all", action="store_true", help="Run extract + build-page")
    parser.add_argument("--dry-run", action="store_true", help="Preview without writing to Notion")
    parser.add_argument("--verbose", "-v", action="store_true", help="Debug logging")
    parser.add_argument("--pdf-dir", type=Path, default=Path("data/pdfs"),
                        help="Directory containing PDF files")
    args = parser.parse_args()

    _setup_logging(args.verbose)
    load_dotenv()

    if not (args.extract or args.build_page or args.all):
        parser.print_help()
        return

    products: dict[str, MicroTopProduct] = {}

    if args.extract or args.all:
        products = run_extract(args.pdf_dir, dry_run=args.dry_run)

    if args.build_page or args.all:
        # If we didn't extract, parse PDFs anyway for the page builder
        if not products:
            logger.info("=== Parsing PDFs for page builder ===")
            products = parse_all_pdfs(args.pdf_dir)

        # Assign Notion page IDs
        for name, product in products.items():
            if name in PRODUCT_PAGES:
                product.notion_page_id = PRODUCT_PAGES[name]

        run_build_page(products, dry_run=args.dry_run)


if __name__ == "__main__":
    main()
