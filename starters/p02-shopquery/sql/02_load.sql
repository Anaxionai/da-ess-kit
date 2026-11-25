-- ShopQuery loader, step 2 of 2: load the CSV into sales_raw and count the rows.
-- First run:  uv run ~/da-ess-kit/data/retail/get_retail.py --out ~/shopquery-data
-- Then, in shopquery/:  duckdb ~/shopquery-data/shopquery.duckdb < sql/02_load.sql
-- Expected count: 1067371.

INSERT INTO sales_raw
SELECT * FROM read_csv('~/shopquery-data/online_retail_II.csv', header = true);

SELECT COUNT(*) AS rows_loaded FROM sales_raw;
