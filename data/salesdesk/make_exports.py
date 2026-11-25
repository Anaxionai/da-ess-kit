#!/usr/bin/env python3
# /// script
# requires-python = ">=3.12"
# dependencies = ["openpyxl>=3.1"]
# ///
"""Make your own monthly sales exports for SalesDesk (P1): messy on purpose.

A shop exports last month's sales as a CSV file every month. The exports are messy:
stray spaces, mixed capitals, prices with "GBP" after them, dates in three layouts, and in
April one column with a new name. This script cuts March, April and May 2011 from UCI
Online Retail II and makes them messy, differently for each student.

    uv run ~/da-ess-kit/data/salesdesk/make_exports.py --student <your-github-username> --out ~/salesdesk-work/exports

It writes sales-2011-03.csv, sales-2011-04.csv, sales-2011-05.csv and control-totals.csv
into --out, and prints one line per file. The same --student always gives the same files.

Where the source data comes from (the script works offline once it has the file):
  1. --source <path to online_retail_II.csv>, if you give it;
  2. otherwise ~/salesdesk-work/online_retail_II.csv, or ~/shopquery-data/online_retail_II.csv;
  3. otherwise it runs the kit's data/retail/get_retail.py once, which downloads about
     45 MB into ~/salesdesk-work/ (add --zip <path> to use a zip your mentor gave you).

README.md in this folder lists every kind of mess and the control totals.
Source: Chen, D. (2012). Online Retail II [Dataset]. UCI Machine Learning Repository.
https://doi.org/10.24432/C5CG6D  Licence: CC BY 4.0. The exports are a changed copy:
values rewritten as text in other layouts, and one column renamed in April.
"""

import argparse
import csv
import datetime as dt
import hashlib
import importlib.util
import random
import sys
from pathlib import Path

COLUMNS = ["Invoice", "StockCode", "Description", "Quantity", "InvoiceDate", "Price", "Customer ID", "Country"]
MONTHS = ["2011-03", "2011-04", "2011-05"]
RENAME_MONTH = "2011-04"
RENAMES = [("Price", "UnitPrice"), ("Quantity", "Qty"), ("Customer ID", "CustomerID")]
CACHE = Path.home() / "salesdesk-work"
KNOWN_COPIES = [CACHE / "online_retail_II.csv", Path.home() / "shopquery-data" / "online_retail_II.csv"]
MONTH_NAMES = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]

# Each mess has a rate: the share of rows it touches. Each student gets rates a little
# above or below these, so every student's files differ.
RATES = {
    "date_day_first": 0.25,       # 01/03/2011 09:47   (DD/MM/YYYY HH:MM)
    "date_month_name": 0.15,      # 01-Mar-2011        (DD-Mon-YYYY, no time)
    "price_gbp": 0.04,            # 2.55 GBP
    "quantity_spaces": 0.03,      # " 12" or "12 "
    "description_spaces": 0.08,   # extra spaces at the start, at the end or inside
    "country_spaces": 0.05,       # "France "
    "country_case": 0.03,         # "france", "FRANCE"
    "customer_space": 0.10,       # an unknown customer written as one space, not empty
}


def seed_for(student: str) -> int:
    """The same id gives the same number on every computer and Python version."""
    key = "da-ess/salesdesk/" + student.strip().lower()
    return int.from_bytes(hashlib.sha256(key.encode("utf-8")).digest()[:8], "big")


def find_source(given: str | None, zip_path: str | None) -> Path:
    if given:
        path = Path(given).expanduser()
        if not path.exists():
            sys.exit(f"Cannot find {path}. Check the path, or leave out --source.")
        return path
    for path in KNOWN_COPIES:
        if path.exists():
            print(f"Using {path.as_posix()}")
            return path
    # Download once with the kit's own script, into ~/salesdesk-work/.
    script = Path(__file__).resolve().parent.parent / "retail" / "get_retail.py"
    spec = importlib.util.spec_from_file_location("get_retail", script)
    get_retail = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(get_retail)
    CACHE.mkdir(parents=True, exist_ok=True)
    get_retail.main(["--out", str(CACHE)] + (["--zip", zip_path] if zip_path else []))
    return KNOWN_COPIES[0]


def read_months(path: Path) -> dict[str, list[dict]]:
    """The rows of March, April and May 2011, in the file's own order."""
    found: dict[str, list[dict]] = {m: [] for m in MONTHS}
    with path.open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        if reader.fieldnames is None or not set(COLUMNS) <= set(reader.fieldnames):
            sys.exit(f"{path} does not have the columns of online_retail_II.csv. Run get_retail.py again.")
        for row in reader:
            month = row["InvoiceDate"][:7]
            if month in found:
                found[month].append(row)
    for month, rows in found.items():
        if not rows:
            sys.exit(f"{path} has no rows for {month}. Run get_retail.py again.")
    return found


def spaces(text: str, rng: random.Random) -> str:
    kind = rng.randrange(3)
    if kind == 0:
        return text + rng.choice([" ", "  "])
    if kind == 1:
        return " " + text
    words = text.split(" ")
    if len(words) > 1:
        i = rng.randrange(1, len(words))
        words[i] = " " + words[i]  # a double space inside
    return " ".join(words)


def messy_row(row: dict, rates: dict, rng: random.Random) -> list[str]:
    stamp = dt.datetime.strptime(row["InvoiceDate"], "%Y-%m-%d %H:%M:%S")
    r = rng.random()
    if r < rates["date_day_first"]:
        date = stamp.strftime("%d/%m/%Y %H:%M")
    elif r < rates["date_day_first"] + rates["date_month_name"]:
        date = f"{stamp.day:02d}-{MONTH_NAMES[stamp.month - 1]}-{stamp.year}"  # English, whatever the locale
    else:
        date = stamp.strftime("%Y-%m-%d %H:%M")

    quantity = row["Quantity"]
    if rng.random() < rates["quantity_spaces"]:
        quantity = rng.choice([" " + quantity, quantity + " "])
    price = row["Price"]
    if rng.random() < rates["price_gbp"]:
        price = f"{price} GBP"
    description = row["Description"]
    if description and rng.random() < rates["description_spaces"]:
        description = spaces(description, rng)
    country = row["Country"]
    if rng.random() < rates["country_spaces"]:
        country = country + " "
    elif rng.random() < rates["country_case"]:
        country = rng.choice([country.lower(), country.upper()])
    customer = row["Customer ID"]
    if not customer and rng.random() < rates["customer_space"]:
        customer = " "
    return [row["Invoice"], row["StockCode"], description, quantity, date, price, customer, country]


def control(rows: list[dict]) -> dict:
    """The true totals of a month, from the source values (before any mess)."""
    revenue = sum(int(r["Quantity"]) * float(r["Price"]) for r in rows)
    return {
        "rows": len(rows),
        "quantity": sum(int(r["Quantity"]) for r in rows),
        "revenue": f"{revenue:.2f}",
        "cancelled_lines": sum(1 for r in rows if r["Invoice"].startswith("C")),
        "no_customer_lines": sum(1 for r in rows if not r["Customer ID"].strip()),
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Make messy monthly sales exports for SalesDesk (P1).")
    parser.add_argument("--student", required=True, help="your GitHub username: it chooses your mess")
    parser.add_argument("--out", default="exports", help="folder for the exports (default: exports)")
    parser.add_argument("--source", default=None, help="an online_retail_II.csv you already have")
    parser.add_argument("--zip", default=None, help="a downloaded online+retail+ii.zip, used only if no CSV is found")
    args = parser.parse_args(argv)
    if not args.student.strip():
        sys.exit("--student must not be empty. Use your GitHub username.")

    data = read_months(find_source(args.source, args.zip))
    rng = random.Random(seed_for(args.student))
    rates = {k: v * rng.uniform(0.7, 1.3) for k, v in RATES.items()}
    old, new = rng.choice(RENAMES)
    out = Path(args.out).expanduser()
    out.mkdir(parents=True, exist_ok=True)

    totals = []
    for month in MONTHS:
        rows = data[month]
        header = [new if (month == RENAME_MONTH and c == old) else c for c in COLUMNS]
        path = out / f"sales-{month}.csv"
        # utf-8-sig writes a byte-order mark: Excel and Power Query then read the file as UTF-8.
        with path.open("w", newline="", encoding="utf-8-sig") as handle:
            writer = csv.writer(handle, lineterminator="\n")
            writer.writerow(header)
            for row in rows:
                writer.writerow(messy_row(row, rates, rng))
        totals.append({"month": month, **control(rows)})
        print(f"Wrote {path.as_posix()}: {len(rows):,} rows")
    path = out / "control-totals.csv"
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(totals[0]), lineterminator="\n")
        writer.writeheader()
        writer.writerows(totals)
    print(f"Wrote {path.as_posix()}: {len(totals)} months")
    return 0


if __name__ == "__main__":
    sys.exit(main())
