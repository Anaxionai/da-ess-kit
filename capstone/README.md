# The case study

The last two weeks of the course are one piece of analysis that is all yours: a vague request from a manager, a real or realistic dataset, a measurable question, a careful answer, a dashboard, a two-page report and a five-minute talk.
It is the project you show in interviews, so pick a question you can explain with pleasure.

## The two weeks

| Week | Module | What happens | Gate |
|---|---|---|---|
| 8 | Case study 1: question, data and analysis | Two learn cards and a concept check (Monday morning), then **your plan, approved by your mentor on day 1**. Then the data, the cleaning and the model, the main number in SQL and Python, three checks of how it could be wrong, the dashboard draft, and a milestone review with your mentor | |
| 9 | Case study 2: dashboard, report and talk | The finished dashboard with the definition of every number, the two-page report with a recommendation, a five-slide talk, the timed SQL and Excel tests, your portfolio, and Demo Day | G3, the case study defence |

## What each task delivers

Every task works in one folder, `casestudy/`, which you copy forward from task to task, as you did with your project folders.

| Task (week 8) | What it adds to `casestudy/` |
|---|---|
| 4. Choose a case study or your own dataset, and write PLAN.md | `PLAN.md` from [`PLAN-template.md`](PLAN-template.md), `PROGRESS.md`, and `.gitignore` with `data/` |
| 5. Get and vet the data | `DATA.md` (source, licence and credit, size and coverage, what is missing, how it was collected, personal data), the profile in `evidence.md`, and `sample/` with at most 200 rows per file |
| 6. Clean and model the data | `CLEANING.md`, `sql/01_load.sql` onwards, the reconciliation (raw rows = clean rows + dropped rows), and the model's Parquet files in `data/model/` |
| 7. Answer the main question | the main number in SQL and the same number in Python (`analysis/answer.py`), and `FINDINGS.md` |
| 8. Check your findings | `CHECKS.md` with three checks, `sql/check_1.sql` to `check_3.sql`, and your weakest point |
| 9. Draft the dashboard | `dashboard/dashboard.md`, `dashboard/measures.dax`, `dashboard/exports/main.csv` |
| 10. Milestone review | your mentor's notes, and the changes you make |

| Task (week 9) | What it adds to `casestudy/` |
|---|---|
| 4. Finish the dashboard | the changes from the feedback, `dashboard/definitions.md` (every number defined) and a `///` description on every measure |
| 5. Write the two-page report | `REPORT.md`: Summary, Question, Data and method, Findings, Limits and Recommendation, with a source for every number |
| 6. Build the deck and rehearse | `talk.md`: five slides and three timed rehearsals |
| 10. Final wrap-up | `README.md` (question, answer, recommendation, how to rerun, data credit, talk video) and `## Plan against delivery` in `PROGRESS.md` |

Week 9's timed SQL and Excel tests and your portfolio sit in their own folders, outside `casestudy/`.
In every task, `PROGRESS.md` gets a section that names the plan items (`M1`, `M2` and so on, from your plan's `## Method`) the task delivers.

## Choose a brief, or bring your own dataset

| Brief | The request | Data |
|---|---|---|
| [Returns](briefs/returns.md) | "Returns are eating our margin. What is going on?" from the head of an online clothes and homeware shop | Made by a kit script, different for every student: orders, order lines, products and returns over 18 months |
| [Staff turnover](briefs/staff-turnover.md) | "We keep losing people. Find out why and tell me what to fix." from the people director of a grocery delivery company | Made by a kit script, different for every student: about 2,400 staff records, promotions and three staff surveys |
| [Energy use](briefs/energy-use.md) | "Our customers want to cut their electricity bills. Show me what one home's meter tells us." from the head of an energy-advice service | Real: four years of one-minute meter readings from one house, UCI Machine Learning Repository, CC BY 4.0 |

Each brief gives the manager's request, the data and how to get it, the data's licence, and what a strong answer shows.

### Your own dataset: the tests

You may bring your own public dataset instead, if it passes **all** of these tests. Check them before task 4, and show your mentor on day 1.

1. **The licence allows use in a paid course**, and you can quote it from the publisher's own page: for example CC0, CC BY 4.0, ODC-By, ODbL or the UK Open Government Licence. A "non-commercial" (NC) licence fails. A dataset with no licence, or one copied onto another website (a Kaggle upload of someone else's data, say), fails unless the original publisher's licence allows it.
2. **No personal data about people who can be identified**: no names, emails, phone numbers, exact addresses or free-text notes about people. Data about people is fine when it is grouped or made up.
3. **At most about 1 GB**, and it opens on your laptop with DuckDB in a few minutes.
4. **It can answer a decision.** It has the measure, a time range and at least one way to compare groups. A real manager could ask the question.
5. **You can reach it today**: a direct download or a documented API, with no sign-in that other people cannot get.

If your dataset fails a test, pick a kit brief. Two weeks are too short to fight the data's terms.

## Rules that do not change

- **Data stays out of Git.** Raw and downloaded data lives in `casestudy/data/`, which `.gitignore` ignores. Commit queries, scripts, Markdown, samples of at most 200 rows, exported measures and Power Query code.
- **Evidence is text.** AxReview reads text files only: Markdown, SQL, `.py`, `.dax`, `.pq` and CSV samples. A `.pbix` or `.xlsx` may be committed for people to open, but never as the only proof.
- **Chat AI may help**, as in the projects, and every use goes in `AI_LOG.md`: what you asked, what you kept, and how you checked it. Concept checks, Explain-it answers and gate answers are yours alone, without AI.
- **Credit the data** in your README, your report and your dashboard, with the credit line from your brief.

## The data scripts

The briefs' data comes from scripts in [`data/`](data/). Run them inside your `casestudy/` folder in Git Bash; each writes into `data/`:

| Script | For | Internet? |
|---|---|---|
| `data/make_returns.py --student <your-github-username>` | Returns | No |
| `data/make_staff.py --student <your-github-username>` | Staff turnover | No |
| `data/get_energy.py` | Energy use | Yes, once (about 20 MB) |

For example: `uv run ~/da-ess-kit/capstone/data/make_returns.py --student asha-k`.
The same username always gives the same data, so your mentor can make your files again to check your numbers.
