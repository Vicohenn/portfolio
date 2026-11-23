-- 01_exploracao.sql — reconhecimento dos dados tratados

CREATE OR REPLACE VIEW precos AS FROM 'data/tratado/precos.parquet';

-- Faixa de preços por produto (sem valores absurdos: R$ 2,05 a R$ 9,99)
SELECT produto, min(valor_venda) AS minimo, median(valor_venda) AS mediana, max(valor_venda) AS maximo
FROM precos
GROUP BY ALL
ORDER BY ALL;

-- Outliers v1 (ingênua): mediana do período inteiro.
-- Marcou ~3 mil casos, mas eram preços legítimos de 2021 (antes da alta do diesel).
WITH medianas AS (
    SELECT produto, median(valor_venda) AS mediana
    FROM precos
    GROUP BY ALL
)
SELECT p.produto, count(*) AS suspeitos
FROM precos p
JOIN medianas m ON m.produto = p.produto
WHERE p.valor_venda < 0.6 * m.mediana
GROUP BY ALL
ORDER BY ALL;

-- Outliers v2: mediana do mesmo produto no mesmo mês.
-- Resultado: 17 casos em 4,7 milhões -> mantidos; a fato terá média e mediana.
WITH medianas AS (
    SELECT produto, date_trunc('month', data_coleta) AS mes, median(valor_venda) AS mediana
    FROM precos
    GROUP BY ALL
)
SELECT p.produto, count(*) AS suspeitos
FROM precos p
JOIN medianas m
  ON m.produto = p.produto
 AND m.mes = date_trunc('month', p.data_coleta)
WHERE p.valor_venda < 0.6 * m.mediana
GROUP BY ALL
ORDER BY ALL;

-- Bandeiras mais frequentes (Vibra aparece com 3 nomes, Raízen com 2)
SELECT bandeira, count(*) AS qtd
FROM precos
GROUP BY ALL
ORDER BY qtd DESC
LIMIT 20;