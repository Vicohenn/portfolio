-- 02_modelo.sql — modelo para o Power BI
-- TODO: terminar o CASE das bandeiras (incluir PETROBRAS DISTRIBUIDORA S.A., ELSE 'Outras')

CREATE OR REPLACE VIEW precos_v AS
SELECT
    *,
    CASE
        WHEN bandeira = 'BRANCA' THEN 'Branca'
        WHEN bandeira IN ('VIBRA', 'VIBRA ENERGIA') THEN 'Vibra'
        WHEN bandeira = 'IPIRANGA' THEN 'Ipiranga'
        WHEN bandeira IN ('RAIZEN', 'RAIZEN MIME') THEN 'Raízen'
    END AS grupo_bandeira
FROM precos;