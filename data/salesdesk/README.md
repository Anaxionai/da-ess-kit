# SalesDesk: the shop's monthly exports (P1)

Every month the shop exports last month's sales as one CSV file, and every month the file is messy. In SalesDesk you clean March with formulas, then rebuild the cleaning in Power Query so April and May refresh with no manual fix.
This folder holds the script that makes **your own** exports, two lookup tables, and a sample of two months.

| File | What it is |
|---|---|
| `make_exports.py` | Makes your three monthly exports and their control totals. Each student gets different mess |
| `products.csv` | Lookup table: `StockCode`, `Category` |
| `countries.csv` | Lookup table: `Country`, `Region` |
| `sample/` | March and April 2011 made with `--student sample`, and their `control-totals.csv`: for the learn cards, the practice task, and as a fallback when the download fails |
| `make_lookups.py` | How the course team built the two lookup tables. You never need to run it |

Your exports and workbooks live in `~/salesdesk-work/`, outside your repository: Power Query remembers a folder's full path, and data stays out of Git.

## Make your exports

In Git Bash:

```bash
mkdir -p ~/salesdesk-work
uv run ~/da-ess-kit/data/salesdesk/make_exports.py --student <your GitHub username> --out ~/salesdesk-work/exports
```

`<your GitHub username>` chooses your mess: the same username always gives the same files, on any computer, so your mentor can make your files again to check your numbers. Capital letters and spaces around it do not matter.

**The first run downloads the shop's data once** (about 45 MB, 2 to 3 minutes): the script runs the kit's [`../retail/get_retail.py`](../retail/README.md), which saves `online_retail_II.csv` in `~/salesdesk-work/`. After that the script works **offline**: it reads that file, or `~/shopquery-data/online_retail_II.csv` if you have it, or any copy you name with `--source <path>`.
Slow or no internet? Ask your mentor for the zip, and add `--zip <path to online+retail+ii.zip>`. Download failed and no zip? Use the kit's sample for now: `mkdir -p ~/salesdesk-work/exports && cp ~/da-ess-kit/data/salesdesk/sample/* ~/salesdesk-work/exports/`, and tell your mentor.

You see one line per file:

```text
Wrote C:/Users/<you>/salesdesk-work/exports/sales-2011-03.csv: 36,748 rows
Wrote C:/Users/<you>/salesdesk-work/exports/sales-2011-04.csv: 29,916 rows
Wrote C:/Users/<you>/salesdesk-work/exports/sales-2011-05.csv: 37,030 rows
Wrote C:/Users/<you>/salesdesk-work/exports/control-totals.csv: 3 months
```

## The exports

Three files, `sales-2011-03.csv`, `sales-2011-04.csv` and `sales-2011-05.csv`: **every** line the shop recorded in that month, in the shop's own order, sales, cancellations and adjustments alike. They are UTF-8 with a byte-order mark (so Excel and Power Query read the `£` in some names correctly), with commas between values and one header line:

| Column | What it holds |
|---|---|
| `Invoice` | The invoice number: 6 digits. Starts with `C` for a cancellation, `A` for a bad-debt adjustment |
| `StockCode` | The product code, such as `85123A`. Some codes are services, not products, such as `POST` (postage) |
| `Description` | The product's name |
| `Quantity` | Units on the line. Negative on cancellations and stock adjustments |
| `InvoiceDate` | When the invoice was made |
| `Price` | Price of one unit, in pounds sterling (£) |
| `Customer ID` | The customer's number. Empty when the shop did not know the customer |
| `Country` | The country the customer lives in, as the shop writes it (`EIRE` is Ireland, `RSA` South Africa) |

### `control-totals.csv`

The true totals of each month, worked out by the script from the shop's values before any mess. They are your reference: when your cleaned numbers match them, your cleaning is right.

| Column | What it is |
|---|---|
| `month` | `2011-03`, `2011-04` or `2011-05` |
| `rows` | Lines in the file (not counting the header) |
| `quantity` | Sum of `Quantity`, cancellations included (so they subtract) |
| `revenue` | Sum of `Quantity` x `Price` over every line, cancellations included, rounded to 2 decimals |
| `cancelled_lines` | Lines whose invoice starts with `C` |
| `no_customer_lines` | Lines with no customer |

Read the list of mess below **after** you have made your own list (SalesDesk task 8).

## Every kind of mess

How many rows each kind touches differs from student to student.

| Column | The mess | Example |
|---|---|---|
| `InvoiceDate` | Three layouts in one column: `YYYY-MM-DD HH:MM`, `DD/MM/YYYY HH:MM` (day first) and `DD-Mon-YYYY` (an English month name, no time) | `2011-03-01 08:30`, `01/03/2011 08:30`, `01-Mar-2011` |
| `Price` | ` GBP` after the number in some rows | `2.55 GBP` |
| `Quantity` | A space before or after the number | ` 12`, `12 ` |
| `Description` | Spaces at the start or the end, or two spaces between words (the shop's own data has some too) | ` HEART T-LIGHT HOLDER`, `RED  RETROSPOT CUP` |
| `Country` | A space at the end, or all small or all capital letters | `France `, `germany`, `UNITED KINGDOM` |
| `Customer ID` | An unknown customer written as one space instead of nothing | ` ` |
| The header, **April only** | One column has a new name. Which one depends on your username: `Price` becomes `UnitPrice`, **or** `Quantity` becomes `Qty`, **or** `Customer ID` becomes `CustomerID`. The order and number of columns stay the same | `Invoice,StockCode,Description,Qty,InvoiceDate,...` |

And the mess that is real, from the shop itself (Online Retail II, below):

- **Cancellations**: invoices starting with `C`, with negative quantities.
- **Adjustments**: invoices starting with `A` (bad debt; the shop has none from March to May 2011, but your rule must still handle them), and lines with a negative quantity or a price of 0 that are not cancellations (stock written off, with notes such as "damaged" as the description).
- **Missing customers**: about a quarter of the lines have no customer.
- **Codes that are not products**: `POST`, `DOT`, `M` (manual), `C2` (carriage), `BANK CHARGES`, `AMAZONFEE` and others.
- **The same product in two spellings**: some codes appear in capitals and small letters (`85123A`, `85123a`).

`Invoice` and `StockCode` are never changed by the script.

## The lookup tables

**`products.csv`** has two columns, `StockCode` and `Category`, and one row for every code the shop sold **before 1 March 2011**, written in capitals.

- Codes first sold in March 2011 or later are **missing on purpose**: your lookups will find some `Not in list` rows, and SalesDesk asks you to explain them.
- Service codes (`POST`, `DOT`, `M`, `C2`, `BANK CHARGES`, `AMAZONFEE`, gift vouchers and the like) have the category `Service`.
- The shop's data has no categories. The kit chose one for each product from words in its name (`CANDLE` is Lighting and candles, `MUG` is Kitchen and dining, and so on), so a few are odd. 12 categories: 11 for products and `Service`.

**`countries.csv`** has two columns, `Country` and `Region`, and one row for every country name in the data, spelled as the data spells it (`USA`, `EIRE`, `RSA`, `Unspecified`). The regions are `United Kingdom`, `Europe`, `Asia Pacific`, `Middle East`, `Americas`, `Africa` and `Unknown` (for `Unspecified`).

Import both with **Data > From Text/CSV** and **Do not detect data types**, so that codes such as `21955` stay text, as in your exports.

## The sample

`sample/` holds `sales-2011-03.csv` and `sales-2011-04.csv` made with `--student sample` (its April renames `Price` to `UnitPrice`), and their `control-totals.csv`:

| month | rows | quantity | revenue | cancelled_lines | no_customer_lines |
|---|---|---|---|---|---|
| 2011-03 | 36,748 | 351,872 | 683,267.08 | 699 | 8,926 |
| 2011-04 | 29,916 | 289,098 | 493,207.12 | 559 | 6,718 |

Everyone who uses the sample gets the same numbers, so the learn cards and the practice task can be checked against one key.

## Source and licence

- **Dataset:** "Online Retail II", UCI Machine Learning Repository: https://archive.ics.uci.edu/dataset/502/online+retail+ii
- **Creator:** Daqing Chen. **DOI:** https://doi.org/10.24432/C5CG6D
- **Licence:** Creative Commons Attribution 4.0 International (CC BY 4.0): https://creativecommons.org/licenses/by/4.0/
- **What the kit changes:** the exports are March, April and May 2011 from the published file, with the mess above added on purpose (spaces, capitals, ` GBP`, date layouts, one renamed column). No value is changed in meaning. The categories in `products.csv` and the regions in `countries.csv` are the kit's own.

Copy this into your `salesdesk/README.md`:

```text
Sales data: Chen, D. (2012). Online Retail II [Dataset]. UCI Machine Learning Repository. https://doi.org/10.24432/C5CG6D. Licensed under CC BY 4.0 (https://creativecommons.org/licenses/by/4.0/). Monthly exports cut and made messy on purpose by the Anaxion AI course kit (data/salesdesk/make_exports.py); categories and regions added by the kit.
```
