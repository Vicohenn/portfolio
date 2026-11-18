# Medidas DAX do painel

O painel usa duas tabelas exportadas por [`sql/05_export_powerbi.sql`](../sql/05_export_powerbi.sql), com as mesmas regras das queries SQL:

- `pbi_pedidos`: 1 linha por pedido
- `pbi_itens`: 1 linha por pedido + categoria

Relacionamento: `pbi_itens[order_id]` → `pbi_pedidos[order_id]` (muitos para um, filtro em direção única).

## Colunas calculadas (`pbi_pedidos`)

```dax
Mes = DATE(YEAR(pbi_pedidos[data_compra]), MONTH(pbi_pedidos[data_compra]), 1)

Ano Mes = FORMAT(pbi_pedidos[data_compra], "yyyy-mm")   -- eixo dos gráficos mensais
```

## Visão Geral

```dax
Faturamento Total = SUM(pbi_pedidos[faturamento])
Qtd Pedidos       = COUNTROWS(pbi_pedidos)
Ticket Medio      = DIVIDE([Faturamento Total], [Qtd Pedidos])
Nota Media        = AVERAGE(pbi_pedidos[nota])
```

## Clientes

```dax
Clientes = DISTINCTCOUNT(pbi_pedidos[customer_unique_id])

-- Mesma regra do SQL: compras no mesmo dia contam como uma só
Clientes Recompra =
COUNTROWS(
    FILTER(
        VALUES(pbi_pedidos[customer_unique_id]),
        CALCULATE(DISTINCTCOUNT(pbi_pedidos[data_compra])) > 1
    )
)

% Recompra             = DIVIDE([Clientes Recompra], [Clientes])
Clientes Compra Unica  = [Clientes] - [Clientes Recompra]
```

## Entrega

```dax
-- Denominador: apenas pedidos entregues (com status de entrega)
% Atrasados =
DIVIDE(
    CALCULATE(COUNTROWS(pbi_pedidos), pbi_pedidos[status_entrega] = "Atrasado"),
    CALCULATE(COUNTROWS(pbi_pedidos), NOT ISBLANK(pbi_pedidos[status_entrega]))
)
```

## Categorias (`pbi_itens`)

```dax
Faturamento Categoria = SUM(pbi_itens[faturamento])
Pedidos Categoria     = DISTINCTCOUNT(pbi_itens[order_id])

-- Média sobre linhas pedido + categoria: cada pedido conta uma vez por categoria,
-- sem dar peso extra a pedidos com vários itens
Nota Categoria = AVERAGEX(pbi_itens, RELATED(pbi_pedidos[nota]))
```

## Conferência com o SQL

| Medida | Power BI | SQL |
|---|---|---|
| Faturamento Total | R$ 13,45 mi | `01_evolucao_vendas.sql` |
| % Recompra | 2,17% | `02_taxa_recompra.sql` |
| Nota (atrasados / no dia / adiantados) | 2,27 / 4,03 / 4,29 | `03_atraso_avaliacao.sql` |
| Nota cama_mesa_banho | 3,97 | `04_categorias_faturamento_avaliacao.sql` |
