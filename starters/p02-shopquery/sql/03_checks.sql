-- Solved for you: is the load complete, and where do the two worksheets overlap?
-- Run in shopquery/:  duckdb -markdown ~/shopquery-data/shopquery.duckdb < sql/03_checks.sql

-- Rows and first and last invoice date per worksheet.
SELECT source_sheet,
       COUNT(*)          AS rows,
       MIN(invoice_date) AS first_invoice,
       MAX(invoice_date) AS last_invoice
FROM sales_raw
GROUP BY source_sheet
ORDER BY source_sheet;

-- Rows and distinct invoices per worksheet from 1 to 9 December 2010, the days both sheets hold.
SELECT source_sheet,
       COUNT(*)                AS rows,
       COUNT(DISTINCT invoice) AS invoices
FROM sales_raw
WHERE invoice_date >= '2010-12-01' AND invoice_date < '2010-12-10'
GROUP BY source_sheet
ORDER BY source_sheet;
