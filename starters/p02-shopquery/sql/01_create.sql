-- ShopQuery loader, step 1 of 2: the raw table, typed, with a key.
-- Run in shopquery/:  duckdb ~/shopquery-data/shopquery.duckdb < sql/01_create.sql
-- The columns are in the same order as online_retail_II.csv (see the kit's data/retail/README.md).

CREATE OR REPLACE TABLE sales_raw (
    invoice      VARCHAR,        -- 6 digits; starts with C for a cancellation, A for a bad-debt adjustment
    stock_code   VARCHAR,        -- a code, not a number: 85123A, POST
    description  VARCHAR,
    quantity     INTEGER,        -- negative on cancellations and stock adjustments
    invoice_date TIMESTAMP,
    price        DECIMAL(12,3),  -- pounds sterling, up to 3 decimals
    customer_id  INTEGER,        -- empty when the customer is unknown
    country      VARCHAR,
    source_sheet VARCHAR,        -- the worksheet the row came from
    source_row   INTEGER,        -- its row number in that worksheet
    PRIMARY KEY (source_sheet, source_row)
);
