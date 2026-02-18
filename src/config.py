"""Configuration: Notion IDs, product mappings, PDF assignments."""

# Notion DB: Kern Produktdaten
PRODUKT_DB_ID = "2ec670e1-9e1a-8110-8100-c85e74a74750"

# Parent page for the comparison page (Produktkatalog)
PARENT_PAGE_ID = "309670e1-9e1a-80da-80b7-cd881f017bef"

# Page IDs for the 8 MicroTop TW products in the Kern Produktdaten DB
PRODUCT_PAGES = {
    "MICROTOP TW 3":       "2ec670e1-9e1a-8189-bd28-d1baeef45625",
    "MICROTOP TW 5":       "2ec670e1-9e1a-8143-876f-e95dc449086b",
    "MICROTOP TW 8":       "2ec670e1-9e1a-81ea-9af0-e735dbcf0b8a",
    "MICROTOP TW NSM":     "2ec670e1-9e1a-8193-a779-e9bc75e90fe9",
    "MICROTOP TW BM":      "2ed670e1-9e1a-8023-97dd-fb810b068c0b",
    "MICROTOP TW VSM":     "2ec670e1-9e1a-815b-b7ee-dc2edf3c3430",
    "MICROTOP TW Mineral": "2ec670e1-9e1a-8112-aef8-c384ad340915",
    "MICROTOP TW 02":      "2ec670e1-9e1a-8109-b632-d9365aaa1524",
}

# PDF file → list of product names it covers
PDF_PRODUCT_MAP = {
    "MICROTOP_TW_3_5_8_de.pdf": ["MICROTOP TW 3", "MICROTOP TW 5", "MICROTOP TW 8"],
    "MICROTOP_TW_NSM_de.pdf":   ["MICROTOP TW NSM"],
    "MICROTOP_TW_BM_de.pdf":    ["MICROTOP TW BM"],
    "MICROTOP_TW_VSM_de.pdf":   ["MICROTOP TW VSM"],
    "MICROTOP_TW_Mineral_de.pdf": ["MICROTOP TW Mineral"],
    "MICROTOP_TW_02_de.pdf":    ["MICROTOP TW 02"],
}

# Product groupings for comparison tables
GROUP_KOERNUNG = ["MICROTOP TW 3", "MICROTOP TW 5", "MICROTOP TW 8"]
GROUP_SPEZIALVERFAHREN = ["MICROTOP TW NSM", "MICROTOP TW BM", "MICROTOP TW VSM"]
GROUP_SPEZIALPRODUKTE = ["MICROTOP TW Mineral", "MICROTOP TW 02"]

# All products in display order
ALL_PRODUCTS = GROUP_KOERNUNG + GROUP_SPEZIALVERFAHREN + GROUP_SPEZIALPRODUKTE

# Products that contain cement (for Zementhinweis in footer)
CEMENT_PRODUCTS = [
    "MICROTOP TW 3", "MICROTOP TW 5", "MICROTOP TW 8",
    "MICROTOP TW NSM", "MICROTOP TW BM", "MICROTOP TW VSM", "MICROTOP TW 02",
]
