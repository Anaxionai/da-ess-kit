#!/usr/bin/env python3
# /// script
# requires-python = ">=3.12"
# dependencies = []
# ///
"""Build products.csv and countries.csv, the two lookup tables for SalesDesk (P1).

For the course team. Students never need to run it: both files are in the kit.

    uv run ~/da-ess-kit/data/salesdesk/make_lookups.py --source data/online_retail_II.csv --out ~/da-ess-kit/data/salesdesk

products.csv   StockCode, Category: every code sold before 1 March 2011, in capitals.
               Codes first sold from March on are missing ON PURPOSE (SalesDesk task 10).
               Service codes (POST, DOT, M, C2, BANK CHARGES, ...) have Category "Service".
               The shop gave no categories: the kit chose one from words in the product name.
countries.csv  Country, Region: every country name in the data, spelled as in the data.

category() is also used by ../sheets/make_sheets.py.

Uses only the Python standard library.
Source: Chen, D. (2012). Online Retail II [Dataset]. UCI Machine Learning Repository.
https://doi.org/10.24432/C5CG6D  Licence: CC BY 4.0.
"""

import argparse
import csv
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

PRODUCT = re.compile(r"^(\d{5}[A-Z]{0,2}|DCGS\w+)$")

# First match wins, so the order matters: a CHRISTMAS LIGHT is Christmas, not Lighting.
CATEGORIES = [
    ("Christmas", r"CHRISTMAS|XMAS|ADVENT|SANTA|REINDEER|NATIVITY|BAUBLE|TREE DECORATION"),
    ("Bags and purses", r"\bBAGS?\b|PURSE|SHOPPER|TOTE|WALLET|HOLDALL"),
    ("Lighting and candles", r"CANDLE|T-LIGHT|TEA ?LIGHT|LANTERN|\bLIGHTS?\b|\bLAMP|NIGHTLIGHT|\bLED\b"),
    ("Kitchen and dining", r"\bMUGS?\b|\bCUPS?\b|SAUCER|PLATE|BOWL|TEAPOT|TEA TOWEL|CAKE|BAKING|\bJARS?\b|"
                           r"\bTINS?\b|NAPKIN|CUTLERY|KITCHEN|LUNCH BOX|BOTTLE|SPOON|\bTRAY|APRON|EGG|"
                           r"BEAKER|GLASS|JUG|COASTER|PLACEMAT|STRAWS|CHOPSTICK|CAKESTAND|DOILY|BREAD"),
    ("Paper and cards", r"\bCARDS?\b|\bWRAP|PAPER|NOTEBOOK|NOTE BOOK|\bPENS?\b|PENCIL|STICKER|ENVELOPE|"
                              r"TISSUES?|RIBBON|GIFT TAG|CHALK|DIARY|JOURNAL|ERASER|RUBBER|STATIONERY|"
                              r"CALENDAR|BUNTING|CONFETTI|BOOK"),
    ("Toys and games", r"\bTOYS?\b|\bGAMES?\b|\bDOLLS?\b|PUZZLE|JIGSAW|BLOCKS|SPACEBOY|SNAP|PLAYHOUSE|"
                       r"CHILDRENS|CHILDREN'S|CHILDS|FELTCRAFT|PAINT SET|ROCKING HORSE|DOMINO|SKIPPING|SPINNING|KIDS|TEDDY|BALLOON|CRAYON|COLOURING"),
    ("Bath and beauty", r"SOAP|\bBATH|SPONGE|INCENSE|LIP GLOSS|NAIL|COSMETIC|MAKE UP|TOILETRY|WASH BAG|"
                        r"PERFUME|SCENTED|OIL BURNER|HAND WARMER"),
    ("Garden and outdoor", r"GARDEN|\bPLANT|WATERING|BIRD ?HOUSE|BIRD FEEDER|FLOWER POT|PLANTER|PICNIC|"
                           r"\bPARASOL|UMBRELLA|HAMMOCK|SEED"),
    ("Jewellery and accessories", r"NECKLACE|NECKL|BRACELET|EARRING|\bRING\b|HAIR|SCARF|CHARM|BROOCH|"
                                  r"KEY ?RING|JEWEL|DIAMANTE|BEAD|GLOVES|HAT\b|SLIPPER"),
    ("Home decor", r"FRAME|CLOCK|CUSHION|\bSIGN\b|MIRROR|\bHOOKS?\b|DOORSTOP|DOOR STOP|VASE|WALL|DOOR|"
                   r"HANGING|DECORATION|HEART|\bBOX\b|BOXES|STORAGE|BASKET|DRAWER|CABINET|SHELF|"
                   r"THROW|BLANKET|QUILT|RUG|ORNAMENT|WREATH|GARLAND|CHIME|PHOTO|LOVE"),
]
OTHER = "Gifts and other"
SERVICE = "Service"
CUTOFF = "2011-03-01"  # products.csv lists only codes sold before March 2011, on purpose

# Country name in the data -> (standard name, region, market)
COUNTRIES = {
    "United Kingdom": ("United Kingdom", "United Kingdom", "Home"),
    "EIRE": ("Ireland", "Europe", "Export"),
    "Channel Islands": ("Channel Islands", "Europe", "Export"),
    "Germany": ("Germany", "Europe", "Export"),
    "France": ("France", "Europe", "Export"),
    "Netherlands": ("Netherlands", "Europe", "Export"),
    "Spain": ("Spain", "Europe", "Export"),
    "Switzerland": ("Switzerland", "Europe", "Export"),
    "Belgium": ("Belgium", "Europe", "Export"),
    "Portugal": ("Portugal", "Europe", "Export"),
    "Italy": ("Italy", "Europe", "Export"),
    "Sweden": ("Sweden", "Europe", "Export"),
    "Norway": ("Norway", "Europe", "Export"),
    "Cyprus": ("Cyprus", "Europe", "Export"),
    "Finland": ("Finland", "Europe", "Export"),
    "Austria": ("Austria", "Europe", "Export"),
    "Denmark": ("Denmark", "Europe", "Export"),
    "Greece": ("Greece", "Europe", "Export"),
    "Poland": ("Poland", "Europe", "Export"),
    "Malta": ("Malta", "Europe", "Export"),
    "Iceland": ("Iceland", "Europe", "Export"),
    "Lithuania": ("Lithuania", "Europe", "Export"),
    "Czech Republic": ("Czech Republic", "Europe", "Export"),
    "European Community": ("European Community", "Europe", "Export"),
    "Australia": ("Australia", "Asia Pacific", "Export"),
    "Japan": ("Japan", "Asia Pacific", "Export"),
    "Hong Kong": ("Hong Kong", "Asia Pacific", "Export"),
    "Singapore": ("Singapore", "Asia Pacific", "Export"),
    "Korea": ("South Korea", "Asia Pacific", "Export"),
    "Thailand": ("Thailand", "Asia Pacific", "Export"),
    "United Arab Emirates": ("United Arab Emirates", "Middle East", "Export"),
    "Israel": ("Israel", "Middle East", "Export"),
    "Bahrain": ("Bahrain", "Middle East", "Export"),
    "Lebanon": ("Lebanon", "Middle East", "Export"),
    "Saudi Arabia": ("Saudi Arabia", "Middle East", "Export"),
    "USA": ("United States", "Americas", "Export"),
    "Canada": ("Canada", "Americas", "Export"),
    "Brazil": ("Brazil", "Americas", "Export"),
    "Bermuda": ("Bermuda", "Americas", "Export"),
    "West Indies": ("West Indies", "Americas", "Export"),
    "RSA": ("South Africa", "Africa", "Export"),
    "Nigeria": ("Nigeria", "Africa", "Export"),
    "Unspecified": ("Unspecified", "Unknown", "Unknown"),
}


def category(name: str) -> str:
    for label, pattern in CATEGORIES:
        if re.search(pattern, name):
            return label
    return OTHER


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Build products.csv and countries.csv for SalesDesk.")
    parser.add_argument("--source", required=True, help="path to online_retail_II.csv (from get_retail.py)")
    parser.add_argument("--out", default=".", help="folder to write the two files into (default: .)")
    args = parser.parse_args(argv)

    names: dict[str, Counter] = defaultdict(Counter)
    sold_before: set[str] = set()
    countries = set()
    with Path(args.source).open(newline="", encoding="utf-8") as handle:
        for row in csv.DictReader(handle):
            countries.add(row["Country"])
            code = row["StockCode"].strip().upper()
            name = " ".join(row["Description"].split()).upper()
            sale = not row["Invoice"].startswith(("C", "A")) and int(row["Quantity"]) > 0
            if sale and row["InvoiceDate"] < CUTOFF:
                sold_before.add(code)
            # Names come only from real sales: adjustment rows carry notes such as "damages".
            if sale and float(row["Price"]) > 0 and name and not name.isdigit():
                names[code][name] += 1

    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)
    counts = Counter()
    with (out / "products.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle, lineterminator="\n")
        writer.writerow(["StockCode", "Category"])
        for code in sorted(sold_before):
            if PRODUCT.match(code):
                name = min(names[code].items(), key=lambda kv: (-kv[1], kv[0]))[0] if names[code] else ""
                label = category(name)
            else:
                label = SERVICE  # POST, DOT, M, C2, BANK CHARGES, AMAZONFEE and the like
            counts[label] += 1
            writer.writerow([code, label])
    print(f"products.csv: {sum(counts.values()):,} codes sold before {CUTOFF[:10]}")
    for label, n in counts.most_common():
        print(f"  {label}: {n:,}")

    missing = countries - set(COUNTRIES)
    if missing:
        sys.exit(f"Countries with no region yet: {sorted(missing)}. Add them to COUNTRIES.")
    with (out / "countries.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle, lineterminator="\n")
        writer.writerow(["Country", "Region"])
        for name in sorted(COUNTRIES):
            writer.writerow([name, COUNTRIES[name][1]])
    print(f"countries.csv: {len(COUNTRIES)} countries")
    return 0


if __name__ == "__main__":
    sys.exit(main())
