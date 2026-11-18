-- =============================================================
-- 03b_atraso_por_estado.sql
-- Pergunta 3 (parte 2): Quais estados concentram os atrasos?
--
-- Regras:
--   * Mesmos recortes de 03_atraso_avaliacao.sql
--   * Estado = UF do cliente (destino da entrega)
--   * LEFT JOIN nas avaliações: pedidos sem nota continuam no % de atraso
--   * Apenas UFs com 100+ pedidos (RR, AP e AC ficam de fora por
--     amostra pequena: com 40 pedidos, 5 atrasos já viram 12,5%)
-- =============================================================

WITH atraso AS (
    SELECT
        o.order_id,
        c.customer_state AS estado,
        o.order_purchase_timestamp,
        o.order_delivered_customer_date,
        CASE
            WHEN o.order_delivered_customer_date::DATE > o.order_estimated_delivery_date::DATE THEN 'Atrasado'
            WHEN o.order_delivered_customer_date::DATE < o.order_estimated_delivery_date::DATE THEN 'Adiantado'
            ELSE 'No dia'
        END AS status_entrega
    FROM orders o
    JOIN customers c ON c.customer_id = o.customer_id
    WHERE o.order_status = 'delivered'
      AND o.order_delivered_customer_date IS NOT NULL
      AND o.order_purchase_timestamp >= DATE '2017-01-01'
      AND o.order_purchase_timestamp <  DATE '2018-09-01'
),

avaliacao AS (
    SELECT
        order_id,
        review_score
    FROM order_reviews
    QUALIFY ROW_NUMBER() OVER (PARTITION BY order_id ORDER BY review_answer_timestamp DESC) = 1
)

SELECT
    a.estado,
    COUNT(*)                                                                         AS pedidos,
    ROUND(100.0 * COUNT(*) FILTER (WHERE a.status_entrega = 'Atrasado') / COUNT(*), 2) AS pct_atrasados,
    ROUND(AVG(DATE_DIFF('day', a.order_purchase_timestamp, a.order_delivered_customer_date)), 1) AS prazo_medio_dias,
    ROUND(AVG(r.review_score), 2)                                                    AS nota_media
FROM atraso a
LEFT JOIN avaliacao r ON r.order_id = a.order_id
GROUP BY a.estado
HAVING COUNT(*) >= 100
ORDER BY pct_atrasados DESC;
