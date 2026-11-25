-- SalesBoard: the row count of every table of the star, in one result.
-- Run in salesboard/:  duckdb data/salesboard.duckdb < sql/row_counts.sql
-- Paste the output into evidence.md under "## DuckDB".
-- Columns: table_name, row_count. One row per table: fact_sales, dim_date, dim_product, dim_customer.

-- TODO(task 8): four SELECTs joined with UNION ALL.
