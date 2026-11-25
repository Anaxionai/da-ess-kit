# Versions

The tools and libraries the course uses, and the version of each.
Briefs never name versions: when a version matters, a task points here.
**Checked on 24 November 2026** against each vendor's own page: python.org, the uv and DuckDB release pages on GitHub, PyPI, the Microsoft Download Center and Microsoft Support. The links are in the last section.

How to read the tables:

- **Course version** means: install this version. A newer patch release (the last number) is fine.
- **Minimum** means: this version or any newer one.
- **Tested** means: the version the course team ran the kit's scripts with. Your project's lock file (`uv.lock`) pins the exact version you get.

## On your laptop (Windows)

[`setup/windows.md`](setup/windows.md) installs these.

| Tool | Version | Kind | Notes |
|---|---|---|---|
| Windows | 10 or 11 | minimum | Power BI Desktop runs on Windows 10 or later. Windows 11 is better |
| Git for Windows (Git Bash) | 2.56.1 | course version | Any 2.45 or newer works |
| VS Code | the newest | — | It updates itself. Add the **Python** and **Jupyter** extensions from Microsoft: they run the `# %%` cells in your `.py` files |
| uv | 0.13.9 | course version | 0.12 or newer. Run `uv python pin --global 3.12` once, so uv never picks a newer Python |
| Python | 3.12.16 | course version | Any 3.12 release, installed with `uv python install 3.12`. Each project pins it with `uv python pin 3.12` (a `.python-version` file) |
| DuckDB command-line tool | 2.0.1 | course version | DuckDB 2.0 is a long-term support (LTS) release. Install it with DuckDB's own script (`setup/windows.md`, Step 7). `winget` still offers only 1.5.6: do not use it |
| Microsoft Excel | Microsoft 365, or Excel 2024 | course version | See "Which Excel?" below |
| Power BI Desktop | the newest (2.160.1151.0 on 23 November 2026) | — | Free. Install it from the Microsoft Store so it updates itself. Microsoft supports only the newest version, and releases one every month |

No Docker and no database server: DuckDB runs inside the command-line tool and inside Python.

## Which Excel?

Every Excel task runs in **Microsoft 365** (the subscription) or **Excel 2024**, on Windows. Older versions miss functions the course uses:

| Feature | Microsoft 365 | Excel 2024 | Excel 2021 | Excel 2016 or 2019 |
|---|---|---|---|---|
| Power Query (Data > Get & Transform) | yes | yes | yes | yes |
| `XLOOKUP` | yes | yes | yes | **no** |
| `TEXTSPLIT` | yes | yes | **no** | **no** |
| PivotTables, slicers, charts | yes | yes | yes | yes |

- Microsoft Support's `XLOOKUP` page says: "XLOOKUP is not available in Excel 2016 and Excel 2019". Use `INDEX` with `MATCH` there.
- Microsoft Support's `TEXTSPLIT` page lists only Excel for Microsoft 365, Excel for the web and Excel 2024. On Excel 2021, use `LEFT`, `MID`, `FIND` or Flash Fill.
- Power Query on **Excel for Mac** needs Microsoft 365; Excel 2016 and 2019 for Mac have none. The course expects Windows.
- **Check your version:** in Excel, select File, then Account, then **About Excel**. The first line names the version.

If your laptop has only Excel 2016, 2019 or 2021, tell your mentor in week 1.

## Python libraries

Add them to a project with `uv add`, for example `uv add "pandas==3.1.1"` to pin one.
The kit's own scripts list what they need at their top, and `uv run` installs it for them.

| Package | Course version | Released | Notes |
|---|---|---|---|
| `duckdb` | 2.0.1 | 20 November 2026 | The same DuckDB as the command-line tool. In DuckDB 2.0 some words are reserved: `days` cannot be a column alias, so write `n_days` (tested 24 November 2026) |
| `pandas` | 3.1.1 | 4 November 2026 | |
| `matplotlib` | 3.11.2 | 11 September 2026 | |
| `pyarrow` | 26.0.1 | 3 November 2026 | Reads and writes Parquet from pandas. See "Smart App Control" in `setup/windows.md` if it fails to import |
| `openpyxl` | 3.1.5 | 28 June 2024 | Reads and writes `.xlsx` files. Used by the kit's `get_retail.py` and `make_sheets.py` |
| `ipykernel` | the newest | — | VS Code asks to install it the first time you run a `# %%` cell. Say yes |

## Tested with the kit's scripts

On 24 November 2026, on Windows 11 in Git Bash, with uv 0.13.x and Python 3.12:

- `data/sheets/make_sheets.py`, `data/salesdesk/make_lookups.py` and `data/salesdesk/make_exports.py`, from the published Online Retail II file;
- `capstone/data/make_returns.py` and `capstone/data/make_staff.py`;
- reading every CSV in the kit with `duckdb` 2.0.1.

## Where each version was checked (24 November 2026)

| What | Page |
|---|---|
| Python 3.12.16 (released 25 October 2026) | https://www.python.org/downloads/ |
| uv 0.13.9 (17 November 2026) | https://github.com/astral-sh/uv/releases |
| DuckDB 2.0.1 (20 November 2026), install script and winget version | https://github.com/duckdb/duckdb/releases and https://duckdb.org/docs/installation/ |
| Python packages | https://pypi.org/project/duckdb/, https://pypi.org/project/pandas/, https://pypi.org/project/matplotlib/, https://pypi.org/project/pyarrow/, https://pypi.org/project/openpyxl/ |
| Git for Windows 2.56.1 (10 November 2026) | https://github.com/git-for-windows/git/releases |
| Power BI Desktop 2.160.1151.0 (23 November 2026) and its requirements | https://www.microsoft.com/download/details.aspx?id=58494 and https://learn.microsoft.com/power-bi/fundamentals/desktop-get-the-desktop |
| `XLOOKUP` availability | https://support.microsoft.com/office/xlookup-function-b7fd680e-6d10-43e6-84f9-88eae8bf5929 |
| `TEXTSPLIT` availability | https://support.microsoft.com/office/textsplit-function-b1ca414e-4c21-4ca0-b1b7-bdecace8a6e7 |
| Power Query in Excel versions | https://support.microsoft.com/office/about-power-query-in-excel-7104fbee-9e62-4cb9-a02e-5bfb1a6c536a |
