-- =============================================================
-- 02_taxa_recompra.sql
-- Pergunta 2: Qual a porcentagem de clientes que compram mais de
-- uma vez, e quanto tempo levam para voltar?
--
-- Regras:
--   * Período: jan/2017 a ago/2018
--   * Exclui pedidos canceled e unavailable
--   * Cliente = customer_unique_id (customer_id muda a cada pedido)
--   * Recompra = nova compra em OUTRO dia. Pedidos do mesmo dia são
--     tratados como uma única compra (867 casos que inflariam a taxa
--     de 2,17% para 3,04%).
-- =============================================================

WITH pedidos AS (
    -- Uma linha por cliente por dia de compra
    SELECT DISTINCT
        c.customer_unique_id,
        o.order_purchase_timestamp::DATE AS data_compra
    FROM orders o
    JOIN customers c ON c.customer_id = o.customer_id
    WHERE o.order_status NOT IN ('canceled', 'unavailable')
      AND o.order_purchase_timestamp >= DATE '2017-01-01'
      AND o.order_purchase_timestamp <  DATE '2018-09-01'
),

compras_numeradas AS (
    SELECT
        customer_unique_id,
        data_compra,
        ROW_NUMBER() OVER (PARTITION BY customer_unique_id ORDER BY data_compra) AS num_compra,
        LEAD(data_compra) OVER (PARTITION BY customer_unique_id ORDER BY data_compra) AS proxima_compra
    FROM pedidos
)

-- num_compra = 1 deixa uma linha por cliente; proxima_compra é a 2ª compra
SELECT
    COUNT(*)                                                                       AS total_clientes,
    COUNT(*) FILTER (WHERE proxima_compra IS NOT NULL)                             AS clientes_recompra,
    ROUND(100.0 * COUNT(*) FILTER (WHERE proxima_compra IS NOT NULL) / COUNT(*), 2) AS taxa_recompra_pct,
    ROUND(AVG(DATE_DIFF('day', data_compra, proxima_compra)), 1)                   AS dias_ate_recompra_media,
    MEDIAN(DATE_DIFF('day', data_compra, proxima_compra))                          AS dias_ate_recompra_mediana
FROM compras_numeradas
WHERE num_compra = 1;
