# MatchStats: Python and pandas on IPL ball-by-ball data.
# Run one cell at a time in VS Code (Run Cell above each "# %%"), or the whole file with:
#     uv run python analysis.py
# Data stays out of Git: season.csv is read from the course kit, and the match files from
# ~/matchstats-data/matches (task 7, step 2, downloads them with get_matches.py).
# Match data from Cricsheet (https://cricsheet.org/), licensed under the Open Data Commons
# Attribution License 1.0 (https://opendatacommons.org/licenses/by/1-0/).

# %% Setup (done for you)
import json
from pathlib import Path

import pandas as pd

pd.set_option("display.max_columns", None)  # print every column, never "..." in place of some
DATA = Path.home() / "matchstats-data"

# %% Balls: every ball of the 2026 season (done for you)
balls = pd.read_csv(Path.home() / "da-ess-kit/data/ipl/season.csv")
print(balls.shape)
print(balls.dtypes)


# %% Matches: one row per match file (done for you)
def match_row(path):
    """One match file -> a dictionary of 11 values from its "info" block.

    A tie or a no-result has no winner, and only a rain-shortened match has a method,
    so those three come from outcome.get(...), which gives None when a key is missing.
    """
    info = json.loads(path.read_text(encoding="utf-8"))["info"]
    outcome = info["outcome"]
    return {
        "match_id": int(path.stem),
        "season": str(info["season"]),  # Cricsheet writes 2009 as a number and "2007/08" as text
        "date": info["dates"][0],
        "venue": info["venue"],
        "team1": info["teams"][0],
        "team2": info["teams"][1],
        "toss_winner": info["toss"]["winner"],
        "toss_decision": info["toss"]["decision"],
        "winner": outcome.get("winner"),
        "result": outcome.get("result"),
        "method": outcome.get("method"),
    }


rows = []
for path in sorted((DATA / "matches").glob("*.json")):
    rows.append(match_row(path))
matches = pd.DataFrame(rows)
print(matches.shape)

# %% Checks
# TODO(task 7): repeated keys (match_id, innings, over_no, ball_no); rows where runs_total is
# not runs_batter + runs_extras; total runs; distinct matches, teams and venues;
# matches["season"].value_counts().sort_index(); and how many balls find their match in
# `matches` (merge with indicator=True).

# %% Batters
# TODO(task 8): runs, balls faced, innings, fours, sixes and strike rate per batter;
# a fair ranking with a minimum number of balls; each team's top scorer.

# %% Venues
# TODO(task 9): batting_second(row) and matches["chasing_team"]; the merge that proves it;
# the fair set of matches; chase rates per ground with one_match_moves and a minimum.

# %% Chart
# TODO(task 10): runs per over for the four teams with most 2026 wins, as a rate per innings;
# save the chart as charts/runs_per_over.png.
