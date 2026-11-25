# Case study plan: <your title>

<!--
Copy this file to casestudy/PLAN.md (case study 1, task 4) and fill in every section.
Keep the six "##" headings exactly as they are: your mentor and AxReview find each part by its heading.
Replace every <...> and every line that starts with ">" with your own words.
One page is enough. Short sentences, real numbers, no filler.
-->

- **Student:** <your GitHub username>
- **Case study:** <Returns | Staff turnover | Energy use | own dataset: name>
- **Date:** <YYYY-MM-DD>
- **Mentor approval:** <approved on YYYY-MM-DD | changes asked: see PROGRESS.md>

## Request

> Who asked, in their own words, and the decision they face.

- **Asked by:** <role, for example "the head of e-commerce">
- **Their words:** "<the request, word for word from the brief, or one a real manager could make>"
- **The decision it feeds:** <what they will decide, and by when>

## Question

> One measurable question. It names the measure, the population, the period, the comparison and the decision.

**Question:** <for example: "What share of online orders arrived late in each region from January to June 2026, compared with the same months of 2025, so the logistics manager knows which courier contract to review first?">

| Part | Yours |
|---|---|
| Measure | <what you count or average, with its unit> |
| Population | <which rows: orders, staff, days, ...; what is left out> |
| Period | <from ... to ...> |
| Comparison | <against what: last year, another group, a target> |
| Decision | <what changes if the answer is A, and if it is B> |

## Data and licence

> The dataset, who publishes it, where, under which licence, and what the licence asks of you.

| Item | Yours |
|---|---|
| Dataset | <name> |
| Publisher | <organisation> |
| Link | <URL of the page you downloaded from> |
| Licence | <name and link, for example CC BY 4.0, https://creativecommons.org/licenses/by/4.0/> |
| What the licence asks | <for example: credit the source, link the licence, say what you changed> |
| Allows use in a paid course? | <yes, because ...> |
| Personal data? | <none / yes: which columns, and what you will drop or group> |
| Size | <files, rows, MB> |

**Credit line** for your README, report and dashboard:

```text
<the attribution the licence asks for>
```

## Method

> Numbered plan items. Each says what it produces, the task that delivers it, and Must or Nice.
> Cover cleaning, the main query, a Python check, three tests, the dashboard, the report and the talk.

| Item | What it produces | Task | Must or Nice |
|---|---|---|---|
| M1 | <cleaned tables and a reconciliation: raw rows = clean rows + dropped rows> | CP1 task 6 | Must |
| M2 | <the fact table and its dimensions, at the grain the main number needs> | CP1 task 6 | Must |
| M3 | <the main number in SQL> | CP1 task 7 | Must |
| M4 | <the same number in Python, and one breakdown> | CP1 task 7 | Must |
| M5 | <three checks of how the answer could be wrong> | CP1 task 8 | Must |
| M6 | <the dashboard draft> | CP1 task 9 | Must |
| M7 | <the finished dashboard with the definition of every number> | CP2 | Must |
| M8 | <the two-page report> | CP2 | Must |
| M9 | <the five-slide talk> | CP2 | Must |
| M10 | <a Nice item, for example a second breakdown> | <task> | Nice |

### Dashboard sketch

> One page, drawn in words (or a photo of a paper sketch in `dashboard/`). The question at the top.

- **Title (the finding as a sentence):** <...>
- **Main number card:** <the measure>
- **Comparison chart:** <chart type, what against what>
- **Breakdown:** <by what>
- **Slicer (at most one):** <field>

## Main number

> The one number that answers the question.

- **Name:** <for example "late-delivery rate">
- **Definition:** <numerator / denominator, in words>
- **What counts:** <rows included>
- **What is left out, and why:** <rows excluded>
- **Unit:** <%, GBP, kWh per day, ...>
- **My guess before I look at the data:** <a number>

## How it could be wrong

> Three ways, and how you will test each one.

| # | Kind | How it could be wrong | How I will test it |
|---|---|---|---|
| 1 | The data | <for example: orders with no region are dropped by the export> | <count rows with and without a region, per month> |
| 2 | The method | <for example: an average pulled up by a few very large values> | <compare the mean with the median> |
| 3 | Reading the result | <for example: a high rate on very few rows> | <show the count next to every rate; set a minimum count> |
