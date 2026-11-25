-- Solved for you. Question: how many rows and invoices are cancellations (invoice starts with C)?
-- Run in shopquery/:  duckdb -markdown ~/shopquery-data/shopquery.duckdb < sql/profile/p1_cancellations.sql
-- Reads the sales table (without the overlap), not sales_raw.

SELECT COUNT(*)                AS cancellation_rows,
       COUNT(DISTINCT invoice) AS cancelled_invoices
FROM sales
WHERE invoice LIKE 'C%';
