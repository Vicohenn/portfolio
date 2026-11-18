-- =============================================================
-- 05_export_powerbi.sql
-- Exporta duas tabelas prontas para o Power BI, com os mesmos
-- recortes e regras das queries 01 a 04.
--
--   pbi_pedidos.parquet  -> 1 linha por PEDIDO (vendas, entrega, nota, cliente)
--   pbi_itens.parquet    -> 1 linha por PEDIDO + CATEGORIA (faturamento por categoria)
--
-- No Power BI: relacionar pbi_itens[order_id] -> pbi_pedidos[order_id]
-- (muitos para um). Os arquivos são gerados na pasta de onde o
-- DuckDB foi aberto, em Parquet: o Power BI lê direto (Obter Dados >
-- Parquet), com os tipos preservados e sem problema de separador
-- decimal, que no CSV faria '39.9' virar 399 no Power BI em português.
-- =============================================================

COPY (
    WITH avaliacao AS (
        SELECT order_id, review_score
        FROM order_reviews
        QUALIFY ROW_NUMBER() OVER (PARTITION BY order_id ORDER BY review_answer_timestamp DESC) = 1
    ),
    valores AS (
        SELECT order_id, SUM(price) AS faturamento, SUM(freight_value) AS frete, COUNT(*) AS qtd_itens
        FROM order_items
        GROUP BY order_id
    )
    SELECT
        o.order_id,
        c.customer_unique_id,
        c.customer_state                                   AS uf_cliente,
        o.order_status                                     AS status_pedido,
        o.order_purchase_timestamp::DATE                   AS data_compra,
        v.faturamento,
        v.frete,
        v.qtd_itens,
        CASE
            WHEN o.order_status <> 'delivered' OR o.order_delivered_customer_date IS NULL THEN NULL
            WHEN o.order_delivered_customer_date::DATE > o.order_estimated_delivery_date::DATE THEN 'Atrasado'
            WHEN o.order_delivered_customer_date::DATE < o.order_estimated_delivery_date::DATE THEN 'Adiantado'
            ELSE 'No dia'
        END                                                AS status_entrega,
        DATE_DIFF('day', o.order_purchase_timestamp, o.order_delivered_customer_date) AS dias_entrega,
        a.review_score                                     AS nota
    FROM orders o
    JOIN customers c     ON c.customer_id = o.customer_id
    JOIN valores v       ON v.order_id = o.order_id
    LEFT JOIN avaliacao a ON a.order_id = o.order_id
    WHERE o.order_status NOT IN ('canceled', 'unavailable')
      AND o.order_purchase_timestamp >= DATE '2017-01-01'
      AND o.order_purchase_timestamp <  DATE '2018-09-01'
) TO 'pbi_pedidos.parquet' (FORMAT parquet);

COPY (
    SELECT
        oi.order_id,
        COALESCE(p.product_category_name, 'sem_categoria') AS categoria,
        SUM(oi.price)                                      AS faturamento,
        COUNT(*)                                           AS qtd_itens
    FROM order_items oi
    JOIN orders o        ON o.order_id = oi.order_id
    LEFT JOIN products p ON p.product_id = oi.product_id
    WHERE o.order_status NOT IN ('canceled', 'unavailable')
      AND o.order_purchase_timestamp >= DATE '2017-01-01'
      AND o.order_purchase_timestamp <  DATE '2018-09-01'
    GROUP BY oi.order_id, categoria
) TO 'pbi_itens.parquet' (FORMAT parquet);
