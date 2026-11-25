#!/usr/bin/env python3
# /// script
# requires-python = ">=3.12"
# dependencies = []
# ///
"""Download the data for the case study "Energy use" (capstone/briefs/energy-use.md).

The dataset is "Individual Household Electric Power Consumption" from the UCI Machine
Learning Repository: one reading a minute from one house near Paris, December 2006 to
November 2010. Licence: CC BY 4.0. The brief has the citation and the credit line.

Run it in your casestudy/ folder in Git Bash (about a minute on a good connection):

    uv run ~/da-ess-kit/capstone/data/get_energy.py --out data

It downloads the published zip (about 20 MB) and writes two files into --out:

    household_power_consumption.txt   the publisher's file, unchanged (about 127 MB):
                                      semicolons between values, dates as dd/mm/yyyy,
                                      a missing reading written as "?"
    household_power.csv               the same rows as a plain CSV (about 120 MB):
                                      commas, one ISO timestamp column, lower-case
                                      column names with units, a missing reading left empty

Nothing else changes: no row is dropped, no value is rounded. The script prints how many
rows have a missing reading, so you can check your own count.

Slow internet? Get the zip once (a mentor can share it), then add --zip <path to the zip>.
Uses only the Python standard library.
"""

import argparse
import csv
import io
import sys
import urllib.error
import urllib.request
import zipfile
from pathlib import Path

URL = "https://archive.ics.uci.edu/static/public/235/individual+household+electric+power+consumption.zip"
RAW = "household_power_consumption.txt"
OUT = "household_power.csv"
RAW_HEADER = ["Date", "Time", "Global_active_power", "Global_reactive_power", "Voltage",
              "Global_intensity", "Sub_metering_1", "Sub_metering_2", "Sub_metering_3"]
HEADER = ["timestamp", "global_active_power_kw", "global_reactive_power_kw", "voltage_v",
          "global_intensity_a", "sub_metering_1_wh", "sub_metering_2_wh", "sub_metering_3_wh"]
EXPECTED_ROWS = 2_075_259
USER_AGENT = "da-ess-course-kit/1.0 (capstone/data/get_energy.py)"


def download(url: str) -> bytes:
    print(f"Downloading {url} (about 20 MB) ...", flush=True)
    request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    try:
        with urllib.request.urlopen(request, timeout=300) as response:
            return response.read()
    except urllib.error.HTTPError as problem:
        sys.exit(f"Download failed: the UCI site answered HTTP {problem.code}. "
                 "Try again later, or ask your mentor for the zip and use --zip.")
    except (urllib.error.URLError, TimeoutError, OSError) as problem:
        sys.exit(f"Download failed: could not reach the UCI site ({problem}). "
                 "Check your internet connection, or ask your mentor for the zip and use --zip.")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Download the household power data for the Energy use case study.")
    parser.add_argument("--out", default="data", help="folder to write into (default: data)")
    parser.add_argument("--zip", default=None, help="use an already downloaded zip instead of downloading")
    args = parser.parse_args(argv)

    if args.zip:
        try:
            blob = Path(args.zip).read_bytes()
        except OSError as problem:
            sys.exit(f"Cannot read the zip file {args.zip}: {problem}")
    else:
        blob = download(URL)
    try:
        raw = zipfile.ZipFile(io.BytesIO(blob)).read(RAW)
    except (zipfile.BadZipFile, KeyError):
        sys.exit(f"The zip does not hold {RAW}. Download it again, or ask your mentor.")

    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)
    (out / RAW).write_bytes(raw)

    rows = missing = 0
    lines = io.TextIOWrapper(io.BytesIO(raw), encoding="ascii", newline="")
    reader = csv.reader(lines, delimiter=";")
    if next(reader) != RAW_HEADER:
        sys.exit("The file's columns are not the ones this script knows. The publisher may have changed it; tell your mentor.")
    part = out / (OUT + ".part")
    with part.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle, lineterminator="\n")
        writer.writerow(HEADER)
        for row in reader:
            day, month, year = row[0].split("/")
            values = ["" if v in ("?", "") else v for v in row[2:]]
            if "" in values:
                missing += 1
            writer.writerow([f"{year}-{int(month):02d}-{int(day):02d} {row[1]}"] + values)
            rows += 1
    part.replace(out / OUT)
    print(f"Wrote {(out / RAW).as_posix()} (the publisher's file) and {(out / OUT).as_posix()}: "
          f"{rows:,} rows, {missing:,} with a missing reading")
    if rows != EXPECTED_ROWS:
        print(f"WARNING: expected {EXPECTED_ROWS:,} rows. The publisher may have changed the file; tell your mentor.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
