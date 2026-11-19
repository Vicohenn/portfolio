# Inflação, juros e câmbio no Brasil

> 🚧 Projeto em andamento

Pipeline em Python que coleta dados das APIs públicas do Banco Central e do IBGE, trata e analisa a relação entre inflação, taxa de juros e câmbio no Brasil.

## Perguntas de negócio

1. O Banco Central reage à inflação? Como a Selic se moveu nos picos de inflação?
2. Quanto rende o juro real, ou seja, a Selic acumulada em 12 meses descontada a inflação do período?
3. Quais grupos do IPCA mais pesaram no bolso?
4. O dólar antecipa a inflação?

## Fontes de dados

- **Banco Central (SGS):** IPCA, Selic e dólar
- **IBGE (API de agregados):** IPCA por grupo de produtos e serviços

## Ferramentas

Python (requests, pandas) · Parquet · matplotlib · GitHub Actions

## Principais achados

**1. O Banco Central reage à inflação, mas com atraso.** Em 2021, a Selic só começou a subir cerca de 8 meses depois da virada da inflação.

![Selic x inflação](graficos/01_selic_vs_ipca.png)

**2. O juro real ficou negativo por quase dois anos.** De outubro de 2020 a julho de 2022, a Selic rendeu menos que a inflação, chegando a -6,5% em 12 meses. Em 2026, o juro real passou de 10%, o maior nível desde 2010.

![Juro real](graficos/02_juro_real.png)

**3. A inflação pesou mais no essencial. De 2012 a 2026, alimentação e bebidas subiram 176%, contra 126% do índice geral.** Educação, saúde e habitação também ficaram acima da média. No outro extremo, comunicação subiu só 23%.

![Inflação grupos IPCA](graficos/03_ipca_grupos)

**4. O dólar chega à inflação com quase um ano de atraso.** A correlação entre a variação do dólar e o IPCA é quase nula no mesmo mês (0,09) e cresce até cerca de 0,42 com 8 a 12 meses de defasagem. É uma relação moderada: o câmbio ajuda a explicar a inflação futura, mas não sozinho.

![Correlação entre dólar e IPCA por defasagem](graficos/04_dolar_ipca.png)