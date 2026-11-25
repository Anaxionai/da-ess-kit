#!/usr/bin/env python3
# /// script
# requires-python = ">=3.12"
# dependencies = []
# ///
"""Make the data for the case study "Staff turnover" (capstone/briefs/staff-turnover.md).

A home-delivery grocery company with three sites. The data is made up: every person,
manager and site in it is invented, so it holds no real personal data. It is shaped like
a real HR export, with the problems a real export has, and each student gets different data.

Run it in your case-study folder in Git Bash (a few seconds, no internet needed):

    uv run ~/da-ess-kit/capstone/data/make_staff.py --student <your-github-username>

It writes three CSV files into data/ (change it with --out):

    employees.csv   employee_id, hire_date, leave_date, leave_reason, department, site,
                    job_level, manager_id, contract, age_band, pay_band
    promotions.csv  employee_id, promotion_date, from_level, to_level
    survey.csv      survey_year, employee_id, engagement, manager_support, workload

Everyone who worked there at any time from 1 January 2023 to 30 June 2026.
The same --student always gives the same files. Uses only the Python standard library.
The kit's code is under the MIT licence; the data it makes is yours to use and publish.
"""

import argparse
import csv
import datetime as dt
import hashlib
import random
import sys
from pathlib import Path

START, END = dt.date(2023, 1, 1), dt.date(2026, 6, 30)
SITES = [("Leeds", 0.40), ("Bristol", 0.35), ("Coventry", 0.25)]
DEPARTMENTS = [  # name, share of staff, yearly leaving risk at the start
    ("Warehouse", 0.38, 0.22), ("Delivery", 0.27, 0.26), ("Customer Support", 0.15, 0.20),
    ("Buying", 0.06, 0.10), ("Technology", 0.07, 0.12), ("Finance", 0.03, 0.08),
    ("People", 0.02, 0.09), ("Marketing", 0.02, 0.11),
]
AGE_BANDS = [("16-24", 0.22), ("25-34", 0.34), ("35-44", 0.22), ("45-54", 0.14), ("55+", 0.08)]
SPELLINGS = {"Customer Support": ["Cust Support", "Customer support", "Customer Support "],
             "Warehouse": ["warehouse", "Warehouse "], "Delivery": ["Deliveries"]}


def seed_for(student: str) -> int:
    key = "da-ess/capstone/staff/" + student.strip().lower()
    return int.from_bytes(hashlib.sha256(key.encode("utf-8")).digest()[:8], "big")


def pick(rng: random.Random, weighted):
    return rng.choices([w[0] for w in weighted], weights=[w[1] for w in weighted])[0]


def random_day(rng: random.Random, first: dt.date, last: dt.date) -> dt.date:
    return first + dt.timedelta(days=rng.randint(0, (last - first).days))


def build(rng: random.Random) -> dict:
    # The hidden story, different for each student.
    hot_site = rng.choice(["Leeds", "Bristol", "Coventry"])         # one site's first-year staff leave fast
    hot_manager_dept = rng.choice(["Customer Support", "Warehouse"])  # one manager in this team loses people
    manager_site = rng.choice([s for s in ("Leeds", "Bristol", "Coventry") if s != hot_site])  # ... at another site
    people, promotions, survey = [], [], []
    managers: dict[tuple[str, str], list[str]] = {}
    next_id = 10001

    def new_person(hire: dt.date, dept: str, site: str, level: int) -> dict:
        nonlocal next_id
        person = {"employee_id": f"E{next_id}", "hire_date": hire, "leave_date": None, "leave_reason": "",
                  "department": dept, "site": site, "job_level": level, "manager_id": "",
                  "contract": "Fixed term" if dept in ("Warehouse", "Delivery") and rng.random() < 0.18 else "Permanent",
                  "age_band": pick(rng, AGE_BANDS), "pay_band": "ABCDE"[min(4, level - 1 + (rng.random() < 0.3))]}
        next_id += rng.randint(1, 4)
        return person

    # Managers first: level 3 and 4 people, a few per department and site.
    for dept, share, _ in DEPARTMENTS:
        for site, _ in SITES:
            if dept in ("Buying", "Technology", "Finance", "People", "Marketing") and site != "Leeds":
                continue  # head-office teams sit in Leeds
            count = max(1, round(share * 14))
            for _ in range(count):
                m = new_person(random_day(rng, dt.date(2012, 1, 1), dt.date(2022, 6, 30)), dept, site, 3)
                people.append(m)
                managers.setdefault((dept, site), []).append(m["employee_id"])
    hot_manager = rng.choice(managers[(hot_manager_dept, manager_site)])

    # Staff at the start, then hires to replace leavers and to grow.
    def place(hire: dt.date) -> dict:
        dept = pick(rng, [(d, s) for d, s, _ in DEPARTMENTS])
        site = "Leeds" if dept in ("Buying", "Technology", "Finance", "People", "Marketing") else pick(rng, SITES)
        p = new_person(hire, dept, site, 1 if rng.random() < 0.8 else 2)
        p["manager_id"] = rng.choice(managers[(dept, site)])
        if (dept, site) == (hot_manager_dept, manager_site) and rng.random() < 0.35:
            p["manager_id"] = hot_manager
        return p

    staff = [place(random_day(rng, dt.date(2015, 1, 1), dt.date(2022, 12, 31))) for _ in range(1000)]
    risk = {d: r for d, _, r in DEPARTMENTS}
    day = START
    active = list(staff)
    people.extend(staff)
    while day <= END:
        # Each month: who leaves, who is promoted, who is hired.
        next_month = (day.replace(day=28) + dt.timedelta(days=4)).replace(day=1)
        leavers = 0
        for p in list(active):
            tenure = (day - p["hire_date"]).days / 365
            monthly = risk[p["department"]] / 12
            if tenure < 1:
                monthly *= 1.8 if p["site"] != hot_site else 3.2
            if p["manager_id"] == hot_manager:
                monthly *= 2.4
            if (day - p.get("_last_up", p["hire_date"])).days > 3 * 365 and p["job_level"] < 3:
                monthly *= 1.5
            if p["contract"] == "Fixed term" and tenure >= 1 and rng.random() < 0.25:
                p["leave_date"], p["leave_reason"] = random_day(rng, day, next_month - dt.timedelta(days=1)), "End of contract"
            elif rng.random() < monthly:
                p["leave_date"] = random_day(rng, day, next_month - dt.timedelta(days=1))
                if p["age_band"] == "55+" and rng.random() < 0.3:
                    p["leave_reason"] = "Retired"
                elif rng.random() < 0.1:
                    p["leave_reason"] = "Dismissed"
                else:
                    p["leave_reason"] = "Resigned"
            elif rng.random() < 0.012 and p["job_level"] < 3:
                when = random_day(rng, day, next_month - dt.timedelta(days=1))
                promotions.append({"employee_id": p["employee_id"], "promotion_date": when,
                                   "from_level": p["job_level"], "to_level": p["job_level"] + 1})
                p["_last_up"] = when
                p["job_level"] += 1
                p["pay_band"] = "ABCDE"[min(4, p["job_level"])]
            if p["leave_date"] and p["leave_date"] > END:
                p["leave_date"], p["leave_reason"] = None, ""
            if p["leave_date"]:
                active.remove(p)
                leavers += 1
        growth = 1.004 if day < dt.date(2025, 1, 1) else 1.0
        hires = max(0, round(leavers * growth + rng.gauss(2, 2)))
        for _ in range(hires):
            p = place(random_day(rng, day, next_month - dt.timedelta(days=1)))
            people.append(p)
            active.append(p)
        day = next_month

    # The yearly staff survey, every October: about 70 % answer.
    for year in (2023, 2024, 2025):
        survey_day = dt.date(year, 10, 15)
        for p in people:
            if p["hire_date"] > survey_day or (p["leave_date"] and p["leave_date"] < survey_day):
                continue
            if rng.random() > 0.7:
                continue
            leaves_soon = p["leave_date"] and (p["leave_date"] - survey_day).days < 300
            workload = min(5, max(1, round(rng.gauss(3.0 - (0.7 if leaves_soon else 0), 0.9))))
            support = min(5, max(1, round(rng.gauss(2.2 if p["manager_id"] == hot_manager else 3.4, 0.8))))
            engage = min(5, max(1, round(rng.gauss(3.5 - (0.5 if leaves_soon else 0), 0.9))))
            survey.append({"survey_year": year, "employee_id": p["employee_id"], "engagement": engage,
                           "manager_support": support, "workload": workload})

    # The problems a real export has.
    leavers = [p for p in people if p["leave_date"]]
    for p in rng.sample(leavers, k=len(leavers) // 40):
        p["leave_reason"] = ""                                   # reason not recorded
    for p in rng.sample(leavers, k=6):
        p["leave_date"] = p["hire_date"] - dt.timedelta(days=rng.randint(1, 30))  # leave date before hire
    for p in rng.sample(people, k=len(people) // 60):
        if p["department"] in SPELLINGS:
            p["department"] = rng.choice(SPELLINGS[p["department"]])  # one team, several spellings
    rehires = [dict(p) for p in rng.sample([p for p in leavers if p["leave_reason"] == "Resigned"], k=8)]
    for p in rehires:                                             # rehired under the same id: two rows
        p["hire_date"] = p["leave_date"] + dt.timedelta(days=rng.randint(60, 300))
        p["leave_date"], p["leave_reason"] = None, ""
        if p["hire_date"] <= END:
            people.append(p)
    for row in rng.sample(survey, k=len(survey) // 100):
        row["workload"] = ""                                     # question skipped
    people.sort(key=lambda p: (p["employee_id"], p["hire_date"]))
    promotions.sort(key=lambda x: (x["promotion_date"], x["employee_id"]))
    return {"employees": people, "promotions": promotions, "survey": survey}


def write(path: Path, rows: list[dict]) -> None:
    with path.open("w", newline="", encoding="utf-8") as handle:
        fields = [k for k in rows[0] if not k.startswith("_")]  # "_last_up" is working data only
        writer = csv.DictWriter(handle, fieldnames=fields, lineterminator="\n", extrasaction="ignore")
        writer.writeheader()
        for row in rows:
            writer.writerow({k: (v.isoformat() if isinstance(v, dt.date) else ("" if v is None else v))
                             for k, v in row.items()})


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Make the Staff turnover case-study data.")
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
