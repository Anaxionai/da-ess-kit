# Guided starters

Every project has three levels. **Core** students start from an empty folder. **Guided** students start from a starter in this folder. **Stretch** students do Core plus the module's Stretch goals. Your mentor tells you your level.

A starter removes the set-up that is not the point of the project: the folder layout, the project files, the headings of the Markdown files the tasks ask for, and a first worked piece to copy the style from. **It never holds the answers**: every formula, query, measure and finding a task grades is yours, and each file shows where with a `TODO(task NN)` line, NN being the task's number in that module.

| Starter | Project | Copy it in | What is half-done |
|---|---|---|---|
| [`p01-salesdesk`](p01-salesdesk/STARTER.md) | P1 SalesDesk (Excel), weeks 2 and 3 | task 8 | The Markdown files with their table headers, and a workbook with no data that lists every column each task adds and the labels of the Checks sheet |
| [`p02-shopquery`](p02-shopquery/STARTER.md) | P2 ShopQuery (SQL on DuckDB), weeks 4 and 5 | task 7 | The loader (`01_create.sql`, `02_load.sql`) and three solved queries; every other SQL file with its question and a TODO |
| [`p03-matchstats`](p03-matchstats/STARTER.md) | P3 MatchStats (Python and pandas), week 6 | task 7 | The uv project and `analysis.py` with both loads done (`balls` and `matches`); the analysis cells are empty |
| [`p04-salesboard`](p04-salesboard/STARTER.md) | P4 SalesBoard (Power BI), week 7 | task 8 | The folders, the `fact_sales` view, every SQL check file with its header, the first two DAX measures (`Revenue`, `Units`) and the Markdown headings. No `.pbix` |

Copy a starter with the command in the project's first build task, for example:

```bash
cp -r ~/da-ess-kit/starters/p02-shopquery shopquery
```

Each starter's `STARTER.md` says what is included, how to run it, and lists every TODO with its task. After the first task, copy your own project folder forward from task to task, as the briefs say; never copy the starter again.

No starter holds data. The data stays on your laptop, outside your repository: `~/salesdesk-work/`, `~/shopquery-data/`, `~/matchstats-data/`, and the star's Parquet files in `salesboard/data/`, which Git ignores.
