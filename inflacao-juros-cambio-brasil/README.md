# Inflação, juros e câmbio no Brasil

> 🚧 Projeto em andamento

Pipeline em Python que coleta dados das APIs públicas do Banco Central e do IBGE, trata e analisa a relação entre inflação, taxa de juros e câmbio no Brasil.

## Perguntas de negócio

1. O Banco Central reage à inflação? Como a Selic se moveu nos picos de inflação?
2. Quanto rende o juro real (Selic acumulada em 12 meses menos o IPCA acumulado em 12 meses)?
3. Quais grupos do IPCA mais pesaram no bolso?
4. O dólar antecipa a inflação?

## Fontes de dados

- **Banco Central (SGS):** IPCA, Selic e dólar
- **IBGE (API de agregados):** IPCA por grupo de produtos e serviços

## Ferramentas

Python (requests, pandas) · Parquet · matplotlib · GitHub Actions