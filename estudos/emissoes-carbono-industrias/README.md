# Emissões de carbono por indústria

Exercício guiado de SQL sobre a pegada de carbono de produtos (PCF), com dados do [The Carbon Catalogue](https://www.nature.com/articles/s41597-022-01178-9).

**Pergunta:** quais setores industriais tiveram a maior pegada de carbono no ano mais recente da base?

**O que foi feito:** consulta em PostgreSQL que filtra o ano mais recente, agrega a pegada de carbono por grupo industrial e conta as empresas de cada setor.

**Resultado:** *Materials* e *Capital Goods* lideram com folga; juntos somam mais de 200 mil kg de CO₂e.

**Ferramentas:** SQL (PostgreSQL)

**Arquivo:** [`notebook.ipynb`](notebook.ipynb)
