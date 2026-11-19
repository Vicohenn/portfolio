import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from pathlib import Path

PASTA_TRATADO = Path("data/tratado")
PASTA_GRAFICOS = Path("graficos")

NOMES = {
    "indice_geral": "Índice geral",
    "alimentacao_bebidas": "Alimentação e bebidas",
    "habitacao": "Habitação",
    "artigos_residencia": "Artigos de residência",
    "vestuario": "Vestuário",
    "transportes": "Transportes",
    "saude_cuidados_pessoais": "Saúde e cuidados pessoais",
    "despesas_pessoais": "Despesas pessoais",
    "educacao": "Educação",
    "comunicacao": "Comunicação",
}

def periodo_txt(df):
    """Texto do período coberto pelo dados, ex.: '01/2010 a 10/2026'."""
    return f"{df['data'].min():%m/%Y} a {df['data'].max():%m/%Y}"

def grafico_selic_ipca(df):
    """Pergunta 1: a Selic reage à inflação?"""
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(df["data"], df["selic_meta"], label="Selic meta (% a.a.)")
    ax.plot(df["data"], df["ipca_12m"], label="IPCA 12 meses (%)")
    ax.set_title(f"Selic x inflação ({periodo_txt(df)})")
    ax.set_ylabel("%")
    ax.legend()
    ax.grid(alpha=0.3)
    fig.tight_layout()
    fig.savefig(PASTA_GRAFICOS / "01_selic_vs_ipca.png", dpi=150)
    plt.close(fig)

def grafico_juro_real(df):
    """Pergunta 2: quanto rende o juro real?"""
    dados = df.dropna(subset=["juro_real_12m"]) # tira os 11 primeiros meses sem janela de 12
    cores = ["#DC2626" if v < 0 else "#2563EB" for v in dados["juro_real_12m"]] # vermelho se negativo, azul se positivo

    fig, ax = plt.subplots(figsize=(10, 5))
    ax.bar(dados["data"], dados["juro_real_12m"], width=25, color=cores)
    ax.axhline(0, color="black", linewidth=0.8) # linha do zero
    ax.set_title(f"Juro real em 12 meses: Selic acima da inflação ({periodo_txt(dados)})")
    ax.set_ylabel("% em 12 meses")
    ax.grid(alpha=0.3, axis="y")
    fig.tight_layout()
    fig.savefig(PASTA_GRAFICOS / "02_juro_real.png", dpi=150)
    plt.close(fig)

def grafico_grupos(grupos):
    """Pergunta 3: quais grupos do IPCA mais subiram no período?"""
    fator = 1 + grupos["ipca_mensal"] / 100
    acumulado = (
        fator.groupby(grupos["grupo"]).prod() # multiplica os fatore de cada grupo
        .sub(1).mul(100)                      # volta pra %
        .sort_values()                        # do menor para o maior
    )

    cores = ["#DC2626" if g == "indice_geral" else "#2563EB" for g in acumulado.index]

    fig, ax = plt.subplots(figsize=(10, 6))
    ax.barh([NOMES[g] for g in acumulado.index], acumulado.values, color=cores)
    ax.set_title(f"Inflação acumulada por grupo do IPCA ({periodo_txt(grupos)})")
    ax.set_xlabel("% acumulado no período")
    ax.grid(alpha=0.3, axis="x")
    fig.tight_layout()
    fig.savefig(PASTA_GRAFICOS / "03_ipca_grupos.png", dpi=150)
    plt.close(fig)

def grafico_dolar_ipca(df):
    """Pergunta 4: o dólar antecipa a inflação?"""
    dolar_12m = df["dolar_medio"].pct_change(12) * 100 # variação do dólar em 12 meses

    defasagens = range(0, 13)
    correlacoes = [dolar_12m.shift(k).corr(df["ipca_12m"]) for k in defasagens]

    melhor = max(defasagens, key=lambda k: correlacoes[k])
    cores = ["#DC2626" if k == melhor else "#2563EB" for k in defasagens]

    fig, ax = plt.subplots(figsize=(10, 5))
    ax.bar(list(defasagens), correlacoes, color=cores)
    ax.set_title(f"Correlação: variação do dólar x IPCA, por defasagem ({periodo_txt(df)})")
    ax.set_xlabel("Defasagem (meses entre a variação do dólar e a inflação)")
    ax.set_ylabel("Correlação")
    ax.set_xticks(list(defasagens))
    ax.grid(alpha=0.3, axis="y")
    fig.tight_layout()
    fig.savefig(PASTA_GRAFICOS / "04_dolar_ipca.png", dpi=150)
    plt.close(fig)

    print(f"Maior correlação: {correlacoes[melhor]:.2f} com {melhor} meses de defasagem")

if __name__ == "__main__":
    PASTA_GRAFICOS.mkdir(exist_ok=True)
    mensal = pd.read_parquet(PASTA_TRATADO / "indicadores_mensais.parquet")
    grupos = pd.read_parquet(PASTA_TRATADO / "ipca_grupos.parquet")
    grafico_selic_ipca(mensal)
    grafico_juro_real(mensal)
    grafico_grupos(grupos)
    grafico_dolar_ipca(mensal)
    print("Gráficos salvos em", PASTA_GRAFICOS)