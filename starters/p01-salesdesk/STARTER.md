# SalesDesk Guided starter (P1)

A half-built `salesdesk/` folder for Guided students: the Markdown files every SalesDesk task fills in, with their headings and table headers ready, and a workbook with no data that lists the columns each task builds.
It holds **no data, no formulas and no answers**: you import the export, write every formula and fill every table yourself.

## Copy it in (task 8, step 1)

In Git Bash, inside task 8's folder:

```bash
cp -r ~/da-ess-kit/starters/p01-salesdesk salesdesk
mkdir -p ~/salesdesk-work
mv salesdesk/salesdesk.xlsx ~/salesdesk-work/
```

The workbook lives in `~/salesdesk-work/`, next to your exports and outside your repository, as the briefs say. This file comes with the folder as `salesdesk/STARTER.md`; delete it when you no longer need it. From task 9 on, copy your own `salesdesk/` folder forward as each brief says.

## What is included

| Path | What it is |
|---|---|
| `salesdesk.xlsx` | Move it to `~/salesdesk-work/`. Sheet `Notes`: every column you add to the `Raw` table, with its task and what it holds. Sheet `Checks`: the labels of task 12's reconciliation (Rows, Quantity, Revenue, Cancelled lines, No-customer lines; Mine, Control, Difference, Check), with empty cells |
| `problems.md` | Task 8's table header: `Column | Problem | Example value | Rows | How I counted` |
| `formulas.md` | One section per task, each with the table header `Column | First cell | Formula | What it does` |
| `evidence.md` | Task 8's first three headings; each task adds its own |
| `NOTES.md` | The four sections tasks 11, 12, 19 and 21 ask for |
| `pivots.md` | The four PivotTables of task 19, with Rows, Columns, Values and Filters to fill in |
| `dashboard.md` | Task 23's sections |
| `sample/`, `queries/`, `docs/` | Empty folders for your 200-row CSV samples (tasks 9, 20), your Power Query `.pq` files (task 20) and your dashboard screenshot (task 23) |

## Run it

There is nothing to run. In task 8, open `~/salesdesk-work/salesdesk.xlsx`, then **Data > From Text/CSV**, choose `~/salesdesk-work/exports/sales-2011-03.csv`, set **Data Type Detection** to **Do not detect data types**, and **Load**. Excel adds the data on a new sheet: name its table `Raw`, as the brief says, and keep the `Notes` sheet open beside it.

## Every TODO

| Task | File | What you write |
|---|---|---|
| 8 | `problems.md`, `formulas.md` (Counting problems), `evidence.md` | Your problem list, counting formulas and the three row counts |
| 9 | `formulas.md` (Cleaning) | The seven cleaning columns |
| 10 | `formulas.md` (Lookups) | Category, CountryName, Region |
| 11 | `formulas.md` (Flags), `NOTES.md` (Flags) | The four flags, and what your first version got wrong |
| 12 | `salesdesk.xlsx` (Checks sheet), `formulas.md` (Checks), `NOTES.md` (Reconciliation) | Your numbers beside the control totals |
| 19 | `pivots.md`, `NOTES.md` (March findings) | The four PivotTables and three findings |
| 21 | `NOTES.md` (Next month) | What broke in April and your fix |
| 22 | `formulas.md` (Growth) | Change, Growth, Check and `MinBase` |
| 23 | `dashboard.md`, `formulas.md` (KPIs) | The dashboard as text |

Task 20's `queries/*.pq` and `sample/pq-march.csv`, task 22's `AI_LOG.md` entry and task 24's `README.md` are yours to create.

## What you still do yourself

Import the data, write every formula, build every PivotTable, the Power Query steps and the dashboard, and fill every Markdown table with your own numbers. Each total must match your own `control-totals.csv`.
