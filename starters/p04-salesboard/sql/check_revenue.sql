-- Check for the Revenue measure: revenue for each year, from your star.
-- Run in salesboard/:  duckdb data/salesboard.duckdb < sql/check_revenue.sql
-- Columns: year, revenue (rounded to 2 decimals). Ordered by year.
-- fact_sales joined to dim_date on date_key. Paste the output under "## SQL Revenue".

-- TODO(task 9): SUM(f.amount) for each d.year.
