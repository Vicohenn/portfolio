-- 03_export_powerbi.sql — exporta o modelo para o Power BI
COPY fato_precos_mensal TO 'data/powerbi/fato_precos_mensal.parquet' (FORMAT parquet);
COPY dim_produto        TO 'data/powerbi/dim_produto.parquet'        (FORMAT parquet);
COPY dim_estado         TO 'data/powerbi/dim_estado.parquet'         (FORMAT parquet);
COPY ipca               TO 'data/powerbi/ipca.parquet'               (FORMAT parquet);