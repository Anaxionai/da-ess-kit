# Sales sheets for the Launchpad

Two small sheets of real shop sales for week 1: one to sort, filter and add up, and one whose published total is wrong.
Both come from the same online shop as the rest of the course (UCI Online Retail II, below). Money is in pounds sterling (£, GBP).

| File | What it is | Rows | Used in |
|---|---|---|---|
| `month-sales.xlsx` | One month of sales, March 2011, as an Excel workbook (sheet `Sales`) | 2,005 invoice lines | Launchpad Day 1 and Day 2 |
| `month-sales.csv` | The same rows as a CSV file | 2,005 | the same, for any other tool |
| `published-total.xlsx` | A weekly sales report for 1 to 7 April 2011: sheet `Summary` with the published numbers, sheet `Lines` with the invoice lines it was made from | 528 lines | Launchpad Day 2 |
| `published-total.csv` | The `Lines` sheet as a CSV file | 528 | the same |

Download a file from GitHub with the **Download raw file** button, then open the `.xlsx` in Excel.
If you open a `.csv` file instead, use **Data > From Text/CSV** rather than a double-click, so Excel reads the dates and numbers as the file means them.
Keep these files out of your course repository: data stays out of Git.

## `month-sales`: one month of sales

Each row is one product on one invoice. One invoice is one order.

| Column | Letter | What it holds | Example |
|---|---|---|---|
| `Invoice` | A | The invoice number | `545225` |
| `InvoiceDate` | B | Date and time of the invoice | `2011-03-01 09:22` |
| `StockCode` | C | The product code | `22053` |
| `Description` | D | The product's name | `EMPIRE DESIGN ROSETTE` |
| `Category` | E | The product's category, such as `Home decor` or `Kitchen and dining` (11 categories). The kit chose it from words in the name | `Home decor` |
| `Quantity` | F | Units sold on this line | `100` |
| `UnitPrice` | G | Price of one unit, in £ | `1.06` |
| `Revenue` | H | `Quantity` x `UnitPrice`, rounded to the penny, in £ | `106.00` |
| `CustomerID` | I | The customer's number. **Empty** when the shop did not know the customer | `12971` |
| `Country` | J | The country the customer lives in. `EIRE` is Ireland | `United Kingdom` |

To keep the sheet short and varied, the kit took whole invoices of up to 12 lines each, chosen at random, until it had about 2,000 lines. It left out cancellations, postage and other charges that are not products, and exact copies of a row. So every row is a real sale.

Numbers to check your own work against:

| What | Value |
|---|---|
| Rows (invoice lines) | 2,005 |
| Invoices | 353 |
| Customers (different `CustomerID` values) | 280 |
| Rows with no `CustomerID` | 67 |
| Countries | 12 (1,802 rows from the United Kingdom) |
| Days with sales | 26 (no Saturdays, and no lines on Sunday 13 March in this sample) |
| First and last invoice | 1 March 2011 09:03 and 31 March 2011 19:20 |
| Units (`SUM` of `Quantity`) | 51,198 |
| Revenue (`SUM` of `Revenue`) | £86,867.84 |

## `published-total`: a total that is wrong

**What was published.** The shop's weekly report, on the `Summary` sheet, gives the number of invoice lines, the week's total sales and the sales of each category for 1 to 7 April 2011. Its author made every number by adding up the `Revenue` column of the `Lines` sheet, as it stands.

**The `Lines` sheet** has the columns of `month-sales` plus two more:

| Column | What it holds |
|---|---|
| `LineID` (column A) | The line's own number, `L0001` onwards. Every invoice line has one `LineID`, so a `LineID` must appear only once |
| `Status` | `Completed` for a sale, `Cancelled` for a line the customer cancelled |

**How a correct total is counted:**

1. Each invoice line counts once. A line that appears twice (the same `LineID`) counts once.
2. Only `Completed` lines are sales. A `Cancelled` line does not count.
3. Every `Revenue` value counts, as a number.

**The published total is wrong**, and so are some of its category numbers. A few rows in `Lines` make them wrong. Your task is to find those rows, say what is wrong with each one, and work out the true total.

## Source and licence

- **Dataset:** "Online Retail II", UCI Machine Learning Repository: https://archive.ics.uci.edu/dataset/502/online+retail+ii
- **Creator:** Daqing Chen. **DOI:** https://doi.org/10.24432/C5CG6D
- **Licence:** Creative Commons Attribution 4.0 International (CC BY 4.0): https://creativecommons.org/licenses/by/4.0/
- **What the kit changed:** it chose the rows described above, added the `Category`, `Revenue`, `LineID` and `Status` columns, and trimmed spaces from names. In `published-total` it also changed and repeated a few rows on purpose: the wrong total is the kit's doing, not the publisher's.

When you publish a result from these sheets, for example on your GitHub profile, add this credit line:

```text
Sales data: Chen, D. (2012). Online Retail II [Dataset]. UCI Machine Learning Repository. https://doi.org/10.24432/C5CG6D. Licensed under CC BY 4.0. Sample cut and changed by the Anaxion AI course kit.
```
