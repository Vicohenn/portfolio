-- 02_modelo.sql — modelo para o Power BI
-- TODO: terminar o CASE das bandeiras (incluir PETROBRAS DISTRIBUIDORA S.A., ELSE 'Outras')

CREATE OR REPLACE VIEW precos_v AS
SELECT
    *,
    CASE
        WHEN bandeira = 'BRANCA' THEN 'Branca'
        WHEN bandeira IN ('VIBRA', 'VIBRA ENERGIA', 'PETROBRAS DISTRIBUIDORA S.A.') THEN 'Vibra'
        WHEN bandeira = 'IPIRANGA' THEN 'Ipiranga'
        WHEN bandeira IN ('RAIZEN', 'RAIZEN MIME') THEN 'Raízen'
        ELSE 'Outras'
    END AS grupo_bandeira
FROM precos;

CREATE OR REPLACE TABLE fato_precos_mensal AS 
SELECT
    date_trunc('month', data_coleta) AS mes,
    estado,
    produto,
    grupo_bandeira,
    COUNT(*) AS n_coletas,
    SUM(valor_venda) AS soma_valor
    -- Fato mensal: guarda soma e contagem (medidas aditivas), não a média,
    -- para o DAX calcular a média ponderada correta em qualquer filtro.
FROM precos_v
GROUP BY ALL;

CREATE OR REPLACE TABLE dim_produto AS
SELECT
    produto,
    unidade_medida,
    produto IN ('GASOLINA', 'ETANOL', 'DIESEL S10') AS principal
FROM precos
GROUP BY ALL;

CREATE OR REPLACE TABLE dim_estado AS
SELECT
    estado,
    regiao
FROM precos
GROUP BY ALL;