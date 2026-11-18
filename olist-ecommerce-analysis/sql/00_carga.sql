-- =============================================================
-- 00_carga.sql
-- Carrega os CSVs da Olist em tabelas do DuckDB.
-- Executar a partir da pasta olist-ecommerce-analysis/:
--   duckdb olist.duckdb < sql/00_carga.sql
-- =============================================================

CREATE OR REPLACE TABLE orders               AS SELECT * FROM read_csv_auto('data/raw/olist_orders_dataset.csv');
CREATE OR REPLACE TABLE order_items          AS SELECT * FROM read_csv_auto('data/raw/olist_order_items_dataset.csv');
CREATE OR REPLACE TABLE order_payments       AS SELECT * FROM read_csv_auto('data/raw/olist_order_payments_dataset.csv');
CREATE OR REPLACE TABLE order_reviews        AS SELECT * FROM read_csv_auto('data/raw/olist_order_reviews_dataset.csv');
CREATE OR REPLACE TABLE customers            AS SELECT * FROM read_csv_auto('data/raw/olist_customers_dataset.csv');
CREATE OR REPLACE TABLE sellers              AS SELECT * FROM read_csv_auto('data/raw/olist_sellers_dataset.csv');
CREATE OR REPLACE TABLE products             AS SELECT * FROM read_csv_auto('data/raw/olist_products_dataset.csv');
CREATE OR REPLACE TABLE geolocation          AS SELECT * FROM read_csv_auto('data/raw/olist_geolocation_dataset.csv');
CREATE OR REPLACE TABLE category_translation AS SELECT * FROM read_csv_auto('data/raw/product_category_name_translation.csv');

-- Conferência: quantidade de linhas por tabela
SELECT 'orders' AS tabela, COUNT(*) AS linhas FROM orders
UNION ALL SELECT 'order_items',          COUNT(*) FROM order_items
UNION ALL SELECT 'order_payments',       COUNT(*) FROM order_payments
UNION ALL SELECT 'order_reviews',        COUNT(*) FROM order_reviews
UNION ALL SELECT 'customers',            COUNT(*) FROM customers
UNION ALL SELECT 'sellers',              COUNT(*) FROM sellers
UNION ALL SELECT 'products',             COUNT(*) FROM products
UNION ALL SELECT 'geolocation',          COUNT(*) FROM geolocation
UNION ALL SELECT 'category_translation', COUNT(*) FROM category_translation;
