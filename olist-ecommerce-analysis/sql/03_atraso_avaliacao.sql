-- =============================================================
-- 03_atraso_avaliacao.sql
-- Pergunta 3 (parte 1): Pedidos entregues com atraso recebem
-- notas piores? Quanto a nota cai?
--
-- Regras:
--   * Período: jan/2017 a ago/2018
--   * Apenas pedidos delivered com data de entrega preenchida
--   * Comparação por DATA (::DATE): a data estimada é sempre 00:00,
--     então comparar timestamps marcaria como atrasados 1.292 pedidos
--     entregues no próprio dia previsto
--   * Uma avaliação por pedido (a respondida mais recentemente)
-- =============================================================

WITH atraso AS (
    -- Um pedido por linha, classificado pela entrega
    SELECT
        order_id,
        CASE
            WHEN order_delivered_customer_date::DATE > order_estimated_delivery_date::DATE THEN 'Atrasado'
            WHEN order_delivered_customer_date::DATE < order_estimated_delivery_date::DATE THEN 'Adiantado'
            ELSE 'No dia'
        END AS status_entrega
    FROM orders
    WHERE order_status = 'delivered'
      AND order_delivered_customer_date IS NOT NULL
      AND order_purchase_timestamp >= DATE '2017-01-01'
      AND order_purchase_timestamp <  DATE '2018-09-01'
),

avaliacao AS (
    -- Deduplica: fica só a avaliação mais recente de cada pedido
    SELECT
        order_id,
        review_score
    FROM order_reviews
    QUALIFY ROW_NUMBER() OVER (PARTITION BY order_id ORDER BY review_answer_timestamp DESC) = 1
)

SELECT
    a.status_entrega,
    COUNT(*)                                                             AS pedidos,
    ROUND(AVG(r.review_score), 2)                                        AS nota_media,
    ROUND(100.0 * COUNT(*) FILTER (WHERE r.review_score <= 2) / COUNT(*), 1) AS pct_notas_1_ou_2
FROM atraso a
JOIN avaliacao r ON r.order_id = a.order_id
GROUP BY a.status_entrega
ORDER BY nota_media;
