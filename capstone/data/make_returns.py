#!/usr/bin/env python3
# /// script
# requires-python = ">=3.12"
# dependencies = []
# ///
"""Make the data for the case study "Returns" (capstone/briefs/returns.md).

An online shop that sells clothes, shoes and homeware. The data is made up: every
customer, product and supplier in it is invented. It is shaped like a real shop's
export, with the problems a real export has, and each student gets different data.

Run it in your case-study folder in Git Bash (a few seconds, no internet needed):

    uv run ~/da-ess-kit/capstone/data/make_returns.py --student <your-github-username>

It writes four CSV files into data/ (change it with --out):

    products.csv     product_id, product_name, category, supplier, list_price
    orders.csv       order_id, order_date, customer_id, channel, region, promo_code, delivery_days
    order_lines.csv  order_id, line_no, product_id, quantity, unit_price
    returns.csv      return_id, order_id, line_no, return_date, quantity, reason, refund

18 months of orders, from 1 January 2025 to 30 June 2026. Money is in pounds (GBP).
The same --student always gives the same files. Uses only the Python standard library.
The kit's code is under the MIT licence; the data it makes is yours to use and publish.
"""

import argparse
import csv
import datetime as dt
import hashlib
import math
import random
import sys
from pathlib import Path

START, END = dt.date(2025, 1, 1), dt.date(2026, 6, 30)
CHANNELS = [("web", 0.55), ("app", 0.30), ("marketplace", 0.15)]
REGIONS = [("London", 0.22), ("South East", 0.16), ("North West", 0.12), ("Midlands", 0.14),
           ("Scotland", 0.09), ("South West", 0.10), ("North East", 0.07), ("Wales", 0.05),
           ("Northern Ireland", 0.05)]
# category: (share of lines, base return rate, price range, sizes matter)
CATEGORIES = {
    "Dresses": (0.14, 0.24, (25, 90), True),
    "Tops": (0.20, 0.13, (8, 35), True),
    "Jeans": (0.12, 0.18, (30, 75), True),
    "Shoes": (0.12, 0.17, (35, 110), True),
    "Coats": (0.06, 0.15, (60, 180), True),
    "Bags": (0.08, 0.06, (15, 80), False),
    "Homeware": (0.18, 0.05, (5, 60), False),
    "Beauty": (0.10, 0.03, (4, 30), False),
}
SUPPLIERS = ["Arden Textiles", "Bramley & Co", "Calder Footwear", "Dunmore Goods", "Elmstead Home",
             "Fenwick Studio", "Granger Leather", "Holloway Works"]
WORDS = {
    "Dresses": ["Wrap", "Midi", "Maxi", "Shirt", "Slip", "Tea", "Smock", "Jersey"],
    "Tops": ["Linen", "Striped", "Ribbed", "Oversized", "Cotton", "Cropped", "Silk", "Henley"],
    "Jeans": ["Straight", "Slim", "Wide", "Bootcut", "Tapered", "Mom", "Relaxed", "Skinny"],
    "Shoes": ["Leather", "Canvas", "Suede", "Chunky", "Ballet", "Running", "Loafer", "Chelsea"],
    "Coats": ["Wool", "Puffer", "Trench", "Rain", "Borg", "Quilted", "Duffle", "Parka"],
    "Bags": ["Tote", "Crossbody", "Backpack", "Clutch", "Weekend", "Bucket", "Saddle", "Shopper"],
    "Homeware": ["Ceramic", "Linen", "Rattan", "Glass", "Oak", "Woven", "Enamel", "Marble"],
    "Beauty": ["Rose", "Citrus", "Lavender", "Vanilla", "Mint", "Cedar", "Neroli", "Fig"],
}
NOUNS = {"Dresses": "Dress", "Tops": "Top", "Jeans": "Jeans", "Shoes": "Shoes", "Coats": "Coat",
         "Bags": "Bag", "Homeware": ["Vase", "Bowl", "Throw", "Cushion", "Lamp", "Mug set"],
         "Beauty": ["Hand cream", "Candle", "Body wash", "Lip balm", "Bath salts"]}
COLOURS = ["Black", "Navy", "Cream", "Green", "Rust", "Grey", "Pink", "Blue"]
SIZE_REASONS = ["Too small", "Too big"]
OTHER_REASONS = ["Not as described", "Damaged", "Changed mind", "Arrived late", "Wrong item sent"]


def seed_for(student: str) -> int:
    key = "da-ess/capstone/returns/" + student.strip().lower()
    return int.from_bytes(hashlib.sha256(key.encode("utf-8")).digest()[:8], "big")


def pick(rng: random.Random, weighted):
    return rng.choices([w[0] for w in weighted], weights=[w[1] for w in weighted])[0]


def build(rng: random.Random) -> dict:
    # The hidden story, different for each student.
    problem_supplier = rng.choice(["Calder Footwear", "Granger Leather"])  # its shoes run small
    late_from = rng.choice([5, 6])            # deliveries this slow are returned more
    dresses_push = rng.choice([(2025, 10), (2025, 11)])  # a marketing push on dresses starts here
    products = []
    pid = 1000
    for category, (share, _, (low, high), _) in CATEGORIES.items():
        count = max(8, round(share * 260))
        for _ in range(count):
            pid += rng.randint(1, 7)
            noun = NOUNS[category]
            noun = rng.choice(noun) if isinstance(noun, list) else noun
            name = f"{rng.choice(WORDS[category])} {noun.lower() if category in ('Homeware', 'Beauty') else noun} {rng.choice(COLOURS).lower()}"
            supplier = rng.choice(SUPPLIERS[:4] if category in ("Dresses", "Tops", "Jeans", "Coats") else
                                  ["Calder Footwear", "Granger Leather"] if category == "Shoes" else
                                  ["Dunmore Goods", "Granger Leather", "Fenwick Studio"] if category == "Bags" else
                                  ["Elmstead Home", "Holloway Works", "Fenwick Studio"])
            price = round(rng.uniform(low, high)) - 0.01
            products.append({"product_id": f"P{pid}", "product_name": name[0].upper() + name[1:],
                             "category": category, "supplier": supplier, "list_price": price})
    by_cat: dict[str, list[dict]] = {}
    for p in products:
        by_cat.setdefault(p["category"], []).append(p)

    orders, lines, returns = [], [], []
    customers = [f"C{n:06d}" for n in rng.sample(range(100000, 999999), 9000)]
    oid, rid = 500000, 1
    day = START
    while day <= END:
        season = 1 + 0.35 * math.cos((day.timetuple().tm_yday - 340) / 365 * 2 * math.pi)  # busier before Christmas
        weekend = 1.15 if day.weekday() >= 5 else 1.0
        n_orders = int(rng.gauss(36 * season * weekend, 5))
        push = (day.year, day.month) >= dresses_push
        for _ in range(max(n_orders, 5)):
            oid += rng.randint(1, 3)
            channel = pick(rng, CHANNELS)
            promo = rng.random() < (0.30 if day.month in (11, 1, 7) else 0.12)
            delivery = max(1, min(12, round(rng.gauss(3.2 if channel != "marketplace" else 4.6, 1.6))))
            order = {"order_id": oid, "order_date": day, "customer_id": rng.choice(customers),
                     "channel": channel, "region": pick(rng, REGIONS),
                     "promo_code": rng.choice(["SALE20", "WELCOME10", "FLASH30"]) if promo else "",
                     "delivery_days": delivery}
            orders.append(order)
            for line_no in range(1, 1 + min(6, 1 + int(rng.expovariate(0.9)))):
                weights = {c: v[0] * (2.2 if push and c == "Dresses" else 1) for c, v in CATEGORIES.items()}
                category = rng.choices(list(weights), weights=list(weights.values()))[0]
                product = rng.choice(by_cat[category])
                qty = 1 if rng.random() < 0.85 else rng.randint(2, 3)
                discount = {"SALE20": 0.2, "WELCOME10": 0.1, "FLASH30": 0.3}.get(order["promo_code"], 0)
                unit = round(product["list_price"] * (1 - discount), 2)
                lines.append({"order_id": oid, "line_no": line_no, "product_id": product["product_id"],
                              "quantity": qty, "unit_price": unit})

                # Does this line come back?
                base = CATEGORIES[category][1]
                rate = base
                if category == "Shoes" and product["supplier"] == problem_supplier:
                    rate *= 2.1
                if delivery >= late_from:
                    rate *= 1.6
                if channel == "marketplace":
                    rate *= 1.25
                if discount >= 0.3:
                    rate *= 1.3
                if rng.random() < min(rate, 0.9):
                    sized = CATEGORIES[category][3]
                    if category == "Shoes" and product["supplier"] == problem_supplier and rng.random() < 0.7:
                        reason = "Too small"
                    elif delivery >= late_from and rng.random() < 0.35:
                        reason = "Arrived late"
                    elif sized and rng.random() < 0.55:
                        reason = rng.choice(SIZE_REASONS)
                    else:
                        reason = rng.choices(OTHER_REASONS, weights=[3, 2, 4, 1, 1])[0]
                    back = qty if rng.random() < 0.8 else rng.randint(1, qty)
                    ret_day = day + dt.timedelta(days=delivery + max(1, int(rng.gauss(9, 5))))
                    if ret_day > END + dt.timedelta(days=30):
                        continue
                    returns.append({"return_id": f"R{rid:06d}", "order_id": oid, "line_no": line_no,
                                    "return_date": ret_day, "quantity": back, "reason": reason,
                                    "refund": round(back * unit, 2)})
                    rid += 1
        day += dt.timedelta(days=1)

    # The problems a real export has.
    for r in rng.sample(returns, k=len(returns) // 25):
        r["reason"] = ""                                    # reason not recorded
    for r in rng.sample(returns, k=len(returns) // 300):
        r["return_date"] = r["return_date"] - dt.timedelta(days=rng.randint(40, 90))  # dated before the order
    for r in rng.sample(returns, k=len(returns) // 200):
        r["refund"] = round(r["refund"] * 10, 2)            # a slipped decimal point
    dupes = [dict(r) for r in rng.sample(returns, k=len(returns) // 150)]
    returns.extend(dupes)                                   # the same return keyed twice
    outage = (2026, 2)                                      # the returns system lost most of a month
    returns = [r for r in returns if (r["return_date"].year, r["return_date"].month) != outage
               or r["return_date"].day <= 9 or rng.random() < 0.2]
    for r in rng.sample(returns, k=len(returns) // 120):
        r["reason"] = r["reason"].upper() or r["reason"]   # same reason, other capitals
    returns.sort(key=lambda r: (r["return_date"], r["return_id"]))
    return {"products": products, "orders": orders, "order_lines": lines, "returns": returns}


def write(path: Path, rows: list[dict]) -> None:
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]), lineterminator="\n")
        writer.writeheader()
        for row in rows:
            writer.writerow({k: (v.isoformat() if isinstance(v, dt.date) else v) for k, v in row.items()})


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Make the Returns case-study data.")
    parser.add_argument("--student", required=True, help="your GitHub username: it chooses your data")
    parser.add_argument("--out", default="data", help="folder for the CSV files (default: data)")
    args = parser.parse_args(argv)
    if not args.student.strip():
        sys.exit("--student must not be empty. Use your GitHub username.")
    tables = build(random.Random(seed_for(args.student)))
    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)
    for name, rows in tables.items():
        write(out / f"{name}.csv", rows)
        print(f"Wrote {(out / f'{name}.csv').as_posix()}: {len(rows):,} rows")
    return 0


if __name__ == "__main__":
    sys.exit(main())
