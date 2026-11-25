-- Solved for you. Question: how many invoices, and how much revenue, in each year?
-- Run in shopquery/:  duckdb -markdown ~/shopquery-data/shopquery.duckdb < sql/questions/q01_revenue_by_year.sql
-- Reads sales_clean, so cancellations and adjustments are left out.
-- 2009 holds only December, and 2011 ends on 9 December: neither is a full year.

SELECT year(invoice_date)          AS year,
       COUNT(DISTINCT invoice)     AS invoices,
       SUM(quantity * price)       AS revenue
FROM sales_clean
GROUP BY year(invoice_date)
ORDER BY year;
