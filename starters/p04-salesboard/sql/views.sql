-- SalesBoard: one DuckDB view per Parquet file of your ShopQuery star.
-- Run in salesboard/:  duckdb data/salesboard.duckdb < sql/views.sql
-- The Parquet files live in data/star/ (Git ignores data/). Copy them from shopquery/data/ first.

-- Done for you, as the example in the brief:
CREATE OR REPLACE VIEW fact_sales AS FROM 'data/star/fact_sales.parquet';

-- TODO(task 8): one view for each dimension, in the same way: dim_date, dim_product, dim_customer.
