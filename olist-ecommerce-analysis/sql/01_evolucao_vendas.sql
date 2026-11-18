-- =============================================================
-- 01_evolucao_vendas.sql
-- Pergunta 1: Como evoluíram o faturamento, o número de pedidos
-- e o ticket médio mês a mês? Existe sazonalidade ou pico pontual?
--
-- Regras:
--   * Período: jan/2017 a ago/2018
--   * Faturamento = soma de price (sem frete)
--   * Exclui pedidos canceled e unavailable
-- =============================================================

WITH pedidos_validos AS (
    -- Um registro por pedido, já no recorte de período e status
    SELECT
        order_id,
        DATE_TRUNC('month', order_purchase_timestamp) AS mes
    FROM orders
    WHERE order_status NOT IN ('canceled', 'unavailable')
      AND order_purchase_timestamp >= DATE '2017-01-01'
      AND order_purchase_timestamp <  DATE '2018-09-01'
),

faturamento_pedido AS (
    -- Valor de cada pedido = soma dos itens (um pedido pode ter vários)
    SELECT
        p.mes,
        p.order_id,
        SUM(i.price) AS valor_pedido
    FROM pedidos_validos p
    JOIN order_items i ON i.order_id = p.order_id
    GROUP BY p.mes, p.order_id
),

mensal AS (
    SELECT
        mes,
        COUNT(*)          AS pedidos,
        SUM(valor_pedido) AS faturamento
    FROM faturamento_pedido
    GROUP BY mes
)

SELECT
    STRFTIME(mes, '%Y-%m')                     AS mes,
    pedidos,
    ROUND(faturamento, 2)                      AS faturamento,
    ROUND(faturamento / pedidos, 2)            AS ticket_medio,
    -- Crescimento em relação ao mês anterior
    ROUND(100.0 * (faturamento / LAG(faturamento) OVER (ORDER BY mes) - 1), 1)
                                               AS cresc_faturamento_pct
FROM mensal
ORDER BY mes;
