# SalesBoard Guided starter (P4)

A half-built `salesboard/` folder for Guided students: the folders, the Git ignore rules, every SQL check file with its header, the first two DAX measures, and the headings of the Markdown files the tasks ask for.
It holds **no data, no `.pbix` and no answers**: you still build the model, write the measures and checks, and design the pages.

## Copy it in (task 8, step 1)

In Git Bash, inside task 8's folder:

```bash
cp -r ~/da-ess-kit/starters/p04-salesboard salesboard
```

This file comes with it as `salesboard/STARTER.md`; delete it when you no longer need it. From task 9 on, copy your own `salesboard/` folder forward as each brief says.

## What is included

| Path | What it is |
|---|---|
| `.gitignore` | `data/` and `*.pbix`: the star, the DuckDB file and the report stay on your laptop |
| `sql/views.sql` | The `fact_sales` view done as the brief's example; the three dimension views are yours |
| `sql/row_counts.sql` | Header only |
| `sql/check_*.sql` | Seven check files with their header: what to compute, the columns and where to paste the output |
| `measures/base.dax` | A DAX query with `Revenue` and `Units` done, and the place for the other three measures |
| `measures/time.dax` | Header only |
| `model.md`, `report.md`, `rls.md`, `definitions.md` | The headings the tasks ask for |
| `exports/`, `report/`, `screenshots/` | Empty folders (each holds a `.gitkeep` so Git keeps it) |

`evidence.md`, `AI_LOG.md` and `EXPLAIN.md` sit in each task's folder, next to `salesboard/`, as the briefs say: they are not in the starter.

## Run it

1. Copy your star's four Parquet files from `shopquery/data/` (P2 task 21) into `salesboard/data/star/`.
2. Finish `sql/views.sql`, then in `salesboard/` run:

   ```bash
   mkdir -p data
   duckdb data/salesboard.duckdb < sql/views.sql
   duckdb data/salesboard.duckdb < sql/row_counts.sql
   ```

3. In Power BI Desktop, turn off Autodetect new relationships and Auto date/time (task 8, step 5), then load the four Parquet files with **Get data > More > Parquet** and save the report as `report/SalesBoard.pbix`.
4. Open **DAX query view**, paste `measures/base.dax`, and select **Run**. You see `Revenue` and `Units` for each year. Check both against `check_revenue.sql` and `check_units.sql` before you add the rest.

If your star uses other table or column names than the course default (`fact_sales`, `dim_date`, `dim_product`, `dim_customer`, `amount`, `quantity`, `date_key`), change the names in these files to yours, the same way everywhere.

## Every TODO

| Task | File | What you write |
|---|---|---|
| 8 | `sql/views.sql` | Views for `dim_date`, `dim_product`, `dim_customer` |
| 8 | `sql/row_counts.sql` | The four row counts with `UNION ALL` |
| 8 | `model.md` | Grains, the Mermaid diagram, the filter path |
| 9 | `sql/check_revenue.sql`, `check_units.sql`, `check_orders.sql`, `check_customers.sql` | The four SQL checks |
| 9 | `measures/base.dax` | `Orders`, `Customers` (the AI move, via `measures/ai_customers.dax`), `Average Order Value`, and their columns in `EVALUATE` |
| 10 | `sql/check_revenue_ytd.sql`, `check_revenue_ly.sql` | The running total and the last-year comparison |
| 10 | `measures/time.dax` | `Revenue YTD`, `Revenue LY`, `Revenue YoY %` |
| 11 | `report.md` | The three pages: visuals, measures, answers |
| 12 | `sql/check_rls.sql`, `rls.md` | The France and Germany check, the role and its tests |
| 13 | `definitions.md` | The definition of every number |

Task 12's `country_manager.csv`, task 13's `measures/model.dax` and task 14's `README.md` are yours to create.

## What you still do yourself

Load the star in Power BI Desktop, set the three relationships, write every check and the last three base measures, the time measures, the pages, the security role, and every Markdown answer. Each number must match your own SQL.
