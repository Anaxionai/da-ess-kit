# MatchStats Guided starter (P3)

A half-built `matchstats/` folder for Guided students: the uv project (`pyproject.toml`, `uv.lock`, `.python-version`) with pandas, matplotlib and ipykernel, and `analysis.py` with **both loads done**: `balls` from the kit's `season.csv`, and `matches` built from the Cricsheet match files by `match_row` and a loop.
Every analysis cell after the loads is an empty `# %%` cell with a `TODO`. No data is included.

## Copy it in (task 7)

In Git Bash, inside task 7's folder:

```bash
cp -r ~/da-ess-kit/starters/p03-matchstats matchstats
cd matchstats
uv sync
```

Then skip task 7's step 1 (the project is set up) and steps 3 to 8 (the loads are done), but **read** every line of `match_row` until you can explain it: task 12's Explain-it asks you to walk through it. This file comes with the folder as `matchstats/STARTER.md`; delete it when you no longer need it. From task 8 on, copy your own `matchstats/` folder forward, without `.venv/`, as each brief says.

## What is included

| Path | What it is |
|---|---|
| `pyproject.toml`, `uv.lock`, `.python-version` | Python 3.12 with `pandas`, `matplotlib` and `ipykernel`. `uv sync` installs exactly the locked versions (pandas 3.1.1, matplotlib 3.11.2 on 24 November 2026) |
| `.gitignore` | `.venv/` and `__pycache__/` |
| `analysis.py` | Cells `Setup`, `Balls` and `Matches` done; cells `Checks`, `Batters`, `Venues` and `Chart` with TODOs |
| `charts/`, `docs/` | Empty folders for your chart (task 10) and your screenshots (task 12) |

## Run it

```bash
uv run python ~/da-ess-kit/data/ipl/get_matches.py --out ~/matchstats-data/matches
uv run python analysis.py
```

The first command prints `Saved 1243 match files to ...` (or more, once new matches are published). The second prints `balls`' shape `(17523, 16)`, its column types, and `matches`' shape `(1243, 11)`.
Checked on 24 November 2026 with the November 2026 Cricsheet archive: all 17,523 balls find their match in `matches`; 74 matches are in season `"2026"`; 25 matches have no winner and 23 have a method (rain-shortened).

In VS Code, open `analysis.py` and select **Run Cell** above each `# %%`. Choose the project's `.venv` as the kernel when VS Code asks.

## Every TODO

| Task | Cell in `analysis.py` | What you write |
|---|---|---|
| 7 | `Checks` | Repeated keys, the runs check, totals, distinct counts, seasons, and the merge with `indicator=True` |
| 8 | `Batters` | Runs, balls faced, strike rate, the fair ranking, each team's top scorer |
| 9 | `Venues` | `batting_second`, the merge that proves it, the fair set, chase rates per ground |
| 10 | `Chart` | Runs per over for the top four teams, saved as `charts/runs_per_over.png` |

Task 9's `AI_LOG.md` entry, task 11's `FINDING.md` and task 12's `README.md` are yours to write.

## What you still do yourself

Every check, every groupby, the venue method and the chart, and every number in `evidence.md`. The loads are done; the analysis is yours.
