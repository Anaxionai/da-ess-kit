# Energy use: what does one home's meter tell us?

One of the three case-study briefs. Read the [case study README](../README.md) first.

## The request

A small energy-advice service helps households cut their electricity bills. It is about to offer customers a "meter review": the customer shares their smart-meter readings, and the service sends back advice. The head of the service sends you this message:

> "Before we sell meter reviews, I want to see what one home's data can really tell us. Here is four years of minute-by-minute readings from one house. When does it use the most? What is using it? Is anything changing over the years? And what would we actually tell this family to do? Show me something I could put in front of a customer."

- **Who asked:** the head of the energy-advice service.
- **The decision:** whether a meter review gives advice worth paying for, and what the standard review should show.
- **What they did not say:** which measure (power at a moment, or energy over a day or a month?), which period, or what "the most" is compared with. Pinning that down is your first job (task 4, `## Question`).

## The data

**Real data:** "Individual Household Electric Power Consumption", from the UCI Machine Learning Repository.

| Item | What we found (checked on 24 November 2026) |
|---|---|
| Page | https://archive.ics.uci.edu/dataset/235/individual+household+electric+power+consumption |
| Creators | Georges Hebrail and Alice Berard. Donated to the repository on 29 August 2012 |
| What it is | 2,075,259 one-minute readings from one house in Sceaux, about 7 km from Paris, France, from 16 December 2006 to 26 November 2010 (47 months) |
| Licence | Creative Commons Attribution 4.0 International (CC BY 4.0): https://creativecommons.org/licenses/by/4.0/legalcode |
| Download | https://archive.ics.uci.edu/static/public/235/individual+household+electric+power+consumption.zip (20,640,916 bytes) |
| DOI | https://doi.org/10.24432/C58K54 |

**The licence**, in the UCI page's words: "This dataset is licensed under a Creative Commons Attribution 4.0 International (CC BY 4.0) license." You may copy, change and publish the data and your results, also in a paid course and in your portfolio, if you credit the creators, link the licence and say what you changed.

**Citation** (as the UCI page gives it), for your README and report:

```text
Hebrail, G. & Berard, A. (2006). Individual Household Electric Power Consumption [Dataset]. UCI Machine Learning Repository. https://doi.org/10.24432/C58K54. Licensed under CC BY 4.0 (https://creativecommons.org/licenses/by/4.0/). Converted to CSV with the Anaxion AI course kit's get_energy.py: ISO timestamps, "?" written as an empty value.
```

The UCI page is not connected with this course and does not endorse it.

### Get the data

Run this in your `casestudy/` folder in Git Bash (about a minute on a good connection):

```bash
uv run ~/da-ess-kit/capstone/data/get_energy.py --out data
```

It writes two files into `data/` and prints `2,075,259 rows, 25,979 with a missing reading`:

| File | What it is |
|---|---|
| `household_power_consumption.txt` | The publisher's file, unchanged: semicolons between values, `Date` as `dd/mm/yyyy` and `Time` as `hh:mm:ss`, a missing reading written as `?` (127 MB) |
| `household_power.csv` | The same rows as a plain CSV for DuckDB, pandas and Power BI: commas, one `timestamp` column (`YYYY-MM-DD hh:mm:ss`), a missing reading left empty. No row is dropped and no value changes (127 MB) |

Slow internet? Download the zip once (a mentor can share it), then add `--zip <path to the zip>`.

### The columns of `household_power.csv`

| Column | Meaning (from the UCI page) | Unit |
|---|---|---|
| `timestamp` | The minute of the reading | date and time |
| `global_active_power_kw` | The household's power, averaged over the minute | kilowatts (kW) |
| `global_reactive_power_kw` | Reactive power, averaged over the minute | kilowatts |
| `voltage_v` | Voltage, averaged over the minute | volts |
| `global_intensity_a` | Current, averaged over the minute | amperes |
| `sub_metering_1_wh` | Energy used in the kitchen in that minute: mainly a dishwasher, an oven and a microwave | watt-hours (Wh) |
| `sub_metering_2_wh` | Energy used in the laundry room: a washing machine, a tumble dryer, a fridge and a light | watt-hours |
| `sub_metering_3_wh` | Energy used by an electric water heater and an air conditioner | watt-hours |

Two facts from the UCI page you will need:

- **Power and energy are different units.** A minute at `global_active_power_kw` uses `global_active_power_kw * 1000 / 60` watt-hours. A kilowatt-hour (kWh) is 1,000 Wh: the unit on a bill.
- **Not everything is sub-metered.** The page says `global_active_power*1000/60 - sub_metering_1 - sub_metering_2 - sub_metering_3` "represents the active energy consumed every minute (in watt hour) in the household by electrical equipment not measured in sub-meterings 1, 2 and 3."

## What to watch for

- **Missing readings.** The UCI page says nearly 1.25 % of rows have no values, and that a missing value is an empty field between two separators. Compare that with what the file really holds. Find out whether the gaps are scattered minutes or whole days, and decide how your daily and monthly numbers treat them.
- **The first and last months are not whole months.**
- **One house is one house.** Whatever you find describes this family, in this house, near Paris, from 2006 to 2010. It is not "French households" and not today's homes.
- **No tariff in the data.** If you turn energy into money, state the price per kWh you assume, and where it comes from, as an assumption.

## What a strong answer shows

- **Energy, not power, as the main number**: kWh per day or per month, with the conversion written out, and a stated rule for days with missing readings.
- **When**: a clear pattern by hour of the day and by day of the week, and how it changes with the seasons, with the typical day shown as a median or an average and the spread around it.
- **What**: the share of energy used by the kitchen, the laundry room, the water heater and air conditioner, and the part no sub-meter measures, adding up to 100 %.
- **Change over the years**, compared fairly: the same months against the same months, whole periods only.
- **Advice a customer can act on**, each with its size: for example how many kWh a year one change could move or save, and the assumption behind it.
- **Three tests of how it could be wrong** (task 8), at least one on the missing readings.
- **One page of dashboard** a customer understands in a minute, with a title that states the finding.
