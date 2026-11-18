-- =============================================================
-- 04_categorias_faturamento_avaliacao.sql
-- Pergunta 4: Quais categorias mais faturam e como se saem em nota
-- média? Há categorias de alto faturamento e nota baixa?
--
-- Regras:
--   * Período: jan/2017 a ago/2018; exclui canceled e unavailable
--   * Faturamento = soma de price (sem frete)
--   * Produtos sem categoria entram como 'sem_categoria'
--   * Nota calculada por PEDIDO, não por item: a avaliação é do
--     pedido, e juntá-la a cada item faria pedidos com vários itens
--     pesarem mais na média (eles têm notas menores, o que puxava
--     a média das categorias para baixo em até 0,13 ponto)
-- =============================================================

WITH itens_validos AS (
    -- Uma linha por ITEM, já filtrada e com a categoria
    SELECT
        oi.order_id,
        COALESCE(p.product_category_name, 'sem_categoria') AS nm_categoria,
        oi.price
    FROM order_items oi
    JOIN orders o        ON o.order_id = oi.order_id
    LEFT JOIN products p ON p.product_id = oi.product_id
    WHERE o.order_status NOT IN ('canceled', 'unavailable')
      AND o.order_purchase_timestamp >= DATE '2017-01-01'
      AND o.order_purchase_timestamp <  DATE '2018-09-01'
),

pedido_categoria AS (
    -- Uma linha por PEDIDO + CATEGORIA (mesmo padrão da pergunta 1:
    -- agrega por pedido antes de agregar no nível final)
    SELECT
        nm_categoria,
        order_id,
        SUM(price) AS faturamento_pedido
    FROM itens_validos
    GROUP BY nm_categoria, order_id
),

avaliacao AS (
    -- Uma avaliação por pedido (a respondida mais recentemente)
    SELECT
        order_id,
        review_score
    FROM order_reviews
    QUALIFY ROW_NUMBER() OVER (PARTITION BY order_id ORDER BY review_answer_timestamp DESC) = 1
)

SELECT
    pc.nm_categoria,
    ROUND(SUM(pc.faturamento_pedido), 2) AS faturamento,
    COUNT(*)                             AS pedidos,
    ROUND(AVG(a.review_score), 2)        AS nota_media
FROM pedido_categoria pc
LEFT JOIN avaliacao a ON a.order_id = pc.order_id
GROUP BY pc.nm_categoria
ORDER BY faturamento DESC
LIMIT 15;
