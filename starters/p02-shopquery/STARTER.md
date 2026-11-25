# ShopQuery Guided starter (P2)

A half-built `shopquery/` folder for Guided students: a working DuckDB loader, three solved queries to copy the style from, and every other SQL file of the project with its question as a header and a `TODO` where your query goes.
It holds **no data and no database**: they live in `~/shopquery-data/`, outside your repository.

## Copy it in (task 7)

In Git Bash, inside task 7's folder:

```bash
cp -r ~/da-ess-kit/starters/p02-shopquery shopquery
```

This file comes with it as `shopquery/STARTER.md`; delete it when you no longer need it. From task 8 on, copy your own `shopquery/` folder forward as each brief says.

## What is included

| Path | What it is |
|---|---|
| `.gitignore` | `data/` and DuckDB files stay out of Git |
| `sql/01_create.sql`, `sql/02_load.sql` | **The loader, done:** the typed `sales_raw` table with its key, and the load from the CSV with a row count |
| `sql/03_checks.sql` | **Solved:** rows and dates per worksheet, and the overlap of 1 to 9 December 2010 |
| `sql/profile/p1_cancellations.sql` | **Solved:** cancellation rows and invoices |
| `sql/questions/q01_revenue_by_year.sql` | **Solved:** invoices and revenue per year |
| `sql/04_sales.sql`, `05_sales_clean.sql`, `06_lookups.sql` | Headers and TODOs |
| `sql/profile/p2` to `p5`, `sql/questions/q02` to `q10` | One file per question, with the question as a comment |
| `sql/windows/`, `sql/cohort/`, `sql/rfm/`, `sql/star/` | One file per query the later tasks ask for |
| `sql/before/` | Empty: task 11 puts the old versions of three queries here |
| `docs/*.md`, `MEMO.md` | The headings each task asks for |

## Run it

```bash
mkdir -p ~/shopquery-data
uv run ~/da-ess-kit/data/retail/get_retail.py --out ~/shopquery-data
cd shopquery
duckdb ~/shopquery-data/shopquery.duckdb < sql/01_create.sql
duckdb ~/shopquery-data/shopquery.duckdb < sql/02_load.sql
duckdb -markdown ~/shopquery-data/shopquery.duckdb < sql/03_checks.sql
```

`02_load.sql` prints `1067371`. `03_checks.sql` prints the rows per worksheet, then `22523` rows and `1088` invoices in each worksheet for 1 to 9 December 2010.
`p1_cancellations.sql` needs your `sales` table (task 7), and `q01_revenue_by_year.sql` needs your `sales_clean` view (task 8).

Checked on 24 November 2026 with DuckDB 2.0.1 on the published file: the loader gives 1,067,371 rows, `p1_cancellations.sql` gives 19,165 rows on 8,292 invoices, and `q01_revenue_by_year.sql` gives 825,685.760 (2009), 9,865,099.754 (2010) and 9,831,894.344 (2011).

## Every TODO

| Task | Files |
|---|---|
| 7 | `sql/04_sales.sql` |
| 8 | `sql/05_sales_clean.sql`, `sql/profile/p2_missing_customers.sql` to `p5_grain.sql`, `docs/profile.md` |
| 10 | `sql/06_lookups.sql`, `sql/questions/q02_top_countries.sql` to `q10_biggest_invoices.sql`, `docs/questions.md` |
| 11 | `docs/rewrites.md` (and copies in `sql/before/`) |
| 18 | `sql/windows/w1_monthly_revenue.sql` to `w5_days_between_orders.sql`, `docs/windows.md` |
| 19 | `sql/cohort/retention.sql`, `retention_grid.sql`, `hand_check.sql`, `docs/cohort.md` |
| 20 | `sql/rfm/rfm.sql`, `docs/rfm.md` |
| 21 | `sql/star/build_star.sql`, `checks.sql`, `export_star.sql`, `docs/star.md` |
| 22 | `MEMO.md` |

Task 9's `practice/` files sit in task 9's own folder, not in `shopquery/`. Task 20's `sql/rfm/rfm_ai.sql` is the chat AI's answer, saved unchanged, and task 23's `README.md` is yours to write.

## What you still do yourself

Every query with a `TODO`, every number in `evidence.md`, and every Markdown answer. Read the three solved files first: one question per file, the question as a comment on line 1, keywords in capitals, one clause per line.
