# Staff turnover: why do people leave?

One of the three case-study briefs. Read the [case study README](../README.md) first.

## The request

A grocery home-delivery company employs about 1,100 people at three sites: Leeds (also the head office), Bristol and Coventry. Most work in the warehouses, on the delivery vans or in customer support. The people director sends you this message:

> "We keep losing people, and hiring and training their replacements costs us a fortune. Someone on the board said our turnover is 40 %. I don't even know if that's right. Find out who is leaving and why, and tell me what to fix first. I present to the board at the end of next week."

- **Who asked:** the people director.
- **The decision:** which one or two actions to put to the board (for example in one site, one team, or the first months of a new job), and how to measure if they work.
- **What they did not say:** what "turnover" means (every leaver, or only people who chose to leave?), over which period, or measured against what. The board's 40 % may count something you should not. Pinning that down is your first job (task 4, `## Question`).

## The data

The company's data is **made by a kit script**: every person, manager and site in it is invented, so it holds no real personal data, and every student gets a different company.
It is shaped like a real HR system's export, problems included.

Run this in your `casestudy/` folder in Git Bash (a few seconds, no internet):

```bash
uv run ~/da-ess-kit/capstone/data/make_staff.py --student <your-github-username>
```

It writes three files into `data/` and prints their row counts (about 2,400 employee rows, 500 promotions and 2,300 survey answers, different for each student):

| File | One row is | Columns |
|---|---|---|
| `employees.csv` | a person's time at the company | `employee_id`, `hire_date`, `leave_date` (empty if still there), `leave_reason` (Resigned, Dismissed, Retired, End of contract), `department`, `site`, `job_level` (1 to 3), `manager_id` (empty for managers), `contract` (Permanent, Fixed term), `age_band`, `pay_band` (A to E) |
| `promotions.csv` | a promotion | `employee_id`, `promotion_date`, `from_level`, `to_level` |
| `survey.csv` | one person's answers in the yearly staff survey (each October) | `survey_year`, `employee_id`, `engagement`, `manager_support`, `workload`, each from 1 (worst) to 5 (best) |

- **Period:** everyone who worked there at any time from 1 January 2023 to 30 June 2026.
- `job_level` and `pay_band` are the values on the day of the export; `promotions.csv` holds the history.
- **The same `--student` always gives the same files**, on any computer. Your mentor can make your files again to check your numbers.

### Licence and credit

The script is part of the course kit, under the MIT licence. The data it makes is invented and belongs to no one: you may publish it, your charts and your findings freely.
Write this line in your README and report:

```text
Data: invented HR data made with the Anaxion AI course kit (capstone/data/make_staff.py, --student <your-github-username>).
```

Say clearly in your report that the company is invented.

### Treat it as if it were real

HR data is personal data in real life. Practise as you would at work (the data ethics card, task 2):

- Never show a result for a group of fewer than 10 people. Merge small groups or leave them out, and say so.
- Report on teams, sites, levels and tenure. Do not single out a named manager on the dashboard: describe "one team in site X" and give the detail to the director only.
- `age_band` is a protected characteristic in UK law (the Equality Act 2010). You may check that your findings are not driven by it, but do not recommend anything based on age.
- Commit only samples of at most 200 rows, as always.

## What to watch for

This export was made by a busy HR team, as real exports are. Vet it before you trust it (task 5), and write every problem you find, with its count, in `DATA.md`. Look at least at:

- dates that cannot be true;
- one person on more than one row;
- the same department written in different ways;
- answers or reasons that are missing.

## What a strong answer shows

- **A turnover rate with a stated definition**: leavers in a period divided by the average headcount in that period, with the headcount worked out from hire and leave dates. It separates people who chose to leave (resigned) from contracts that ended, dismissals and retirements, and it checks the board's 40 %.
- **Rates for fair groups**: by site, department, team, tenure (for example the first 12 months against later) and level, each with the headcount next to it, so a small team's high rate is not mistaken for a pattern.
- **When people leave, not just who**: a view of leaving by months since hire shows whether the problem is in the first year.
- **The survey used with care**: a link between low scores and leaving is a clue, not proof, and the survey covers only the people who answered.
- **Problems in the data, found and handled**, each rule written down, and the reconciliation shows raw rows = clean rows + dropped rows.
- **Three tests of how it could be wrong** (task 8), at least one of them on the definition of turnover.
- **One or two actions** the director can take to the board, each with the number that would show next year whether it worked.
