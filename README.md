# Data Analytics Essentials: course kit

The course kit for **Data Analytics Essentials: Excel, SQL, Python and Power BI** (9 weeks).
It holds what your tasks need beyond your own work: the laptop setup guide, the course datasets and the scripts that make your own copies of them, the Guided starters, and the case-study briefs.
Your task briefs link to files in this kit.

## Get the kit

Run this once, in Git Bash (Launchpad task 14, "Finish the laptop, part 2"):

```bash
cd ~ && git clone https://github.com/Anaxionai/da-ess-kit.git
```

This makes the folder `~/da-ess-kit`, which is `C:\Users\<your name>\da-ess-kit` on Windows.
Keep it next to your course repository, never inside it.

Check it: `ls ~/da-ess-kit` lists `README.md`, `VERSIONS.md`, `setup`, `data`, `starters` and `capstone`.

Before that, you need no clone: download single files from GitHub with the **Download raw file** button, as the Launchpad briefs say.

## Update the kit

When a task says "Run `git pull` in `~/da-ess-kit`", run:

```bash
cd ~/da-ess-kit
git pull
```

Do not change the kit's files. Copy a file into your own folder first, then change your copy.
If `git pull` says your local changes would be overwritten, run `git restore .` in the kit folder, then `git pull` again.

Every command in the kit is written for **Git Bash** in VS Code. [`setup/windows.md`](setup/windows.md) sets it up.

## What is in the kit

| Path | What it is | Used in |
|---|---|---|
| `README.md` | This file | the whole course |
| `VERSIONS.md` | The version of every tool and library the course uses, and which Excel you need | the whole course |
| `LICENSE` | The MIT licence for the kit's code and text | — |
| `setup/windows.md` | Windows laptop setup: Git Bash in VS Code, uv with Python 3.12, the DuckDB command-line tool, VS Code's Python and Jupyter extensions, Power BI Desktop, the Excel version check | Launchpad, P3, P4 |
| `try-it.md` | Free sites where you practise each new idea in the browser | learn cards |
| `data/sheets/` | One month of shop sales, and a weekly report whose total is wrong | Launchpad, Days 1 and 2 |
| `data/ipl/` | One IPL season, one row per ball (`season.csv`), and `get_matches.py`, which downloads every match's details | Launchpad Day 3, P3 MatchStats |
| `data/retail/` | `get_retail.py`: downloads two years of the shop's sales (UCI Online Retail II) | P1, P2 ShopQuery |
| `data/salesdesk/` | `make_exports.py`: your own messy monthly exports; the `products.csv` and `countries.csv` lookup tables; a sample of two months | P1 SalesDesk |
| `starters/` | The Guided starters, one per project | P1 to P4 |
| `capstone/` | How the case study works, the plan template, three case-study briefs and their data scripts | Case study, weeks 8 and 9 |

## Folders on your laptop

Data never goes into your course repository. The kit's scripts save it here, next to the kit:

| Folder | What lives there | Made in |
|---|---|---|
| `~/da-ess-kit` | This kit | Launchpad |
| `~/salesdesk-work` | Your monthly exports and SalesDesk workbooks | P1 |
| `~/shopquery-data` | The shop's sales CSV and your DuckDB database | P2 |
| `~/matchstats-data` | Cricsheet's match files | P3 |
| `casestudy/data/` inside your task folder | Your case-study data (Git ignores it) | Case study |

## Running the kit's Python scripts

Run them with `uv run`, from the folder your task names, for example:

```bash
uv run ~/da-ess-kit/data/retail/get_retail.py --out ~/shopquery-data
```

A script that needs a library says so in its first lines (between `# /// script` and `# ///`), and `uv run` installs it in a separate place, so your own projects are not changed. Every script prints `--help`.

## Line endings

The kit's `.gitattributes` makes Git check out every text file with LF line endings, on Windows too, and treats `.xlsx` and other binary files as binary. Do not convert the files to CRLF.

## Licence and attribution

- **The kit's own work** (scripts, guides, starters, briefs) is under the MIT licence: see [`LICENSE`](LICENSE).
- **Datasets keep their own licences.** Credit the source whenever you publish a result, chart or table made from them, with the credit line in the dataset's README:

| Dataset | Source | Licence | Credit line in |
|---|---|---|---|
| Online Retail II (the shop's sales: `data/sheets/`, `data/retail/`, `data/salesdesk/`) | Chen, D. (2012), UCI Machine Learning Repository, https://doi.org/10.24432/C5CG6D | CC BY 4.0, https://creativecommons.org/licenses/by/4.0/ | [`data/retail/README.md`](data/retail/README.md) |
| IPL ball-by-ball data (`data/ipl/`) | Cricsheet, https://cricsheet.org/ | Open Data Commons Attribution License 1.0, https://opendatacommons.org/licenses/by/1-0/ | [`data/ipl/NOTICE.md`](data/ipl/NOTICE.md) |
| Individual Household Electric Power Consumption (case study "Energy use", downloaded by `capstone/data/get_energy.py`) | Hebrail, G. and Berard, A. (2006), UCI Machine Learning Repository, https://doi.org/10.24432/C58K54 | CC BY 4.0 | [`capstone/briefs/energy-use.md`](capstone/briefs/energy-use.md) |

- **Changed data.** The kit cuts, reshapes and, for practice, deliberately damages copies of the Online Retail II data (the wrong weekly total, the messy exports). Those changes are the kit's doing, not the publisher's; each README says what changed.
- **Invented data.** The "Returns" and "Staff turnover" case studies use data that the kit's scripts make up. Every person, product and company in them is invented.
- **Tools** keep their own licences: DuckDB (MIT), pandas (BSD 3-Clause), matplotlib (its PSF-based licence), uv (MIT or Apache 2.0). Microsoft Excel and Power BI Desktop are Microsoft products under Microsoft's terms; Power BI Desktop is free to download.
- No publisher named here is connected with the course or endorses it. Company and product names belong to their owners.
