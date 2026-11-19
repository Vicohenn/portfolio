import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from pathlib import Path

PASTA_TRATADO = Path("data/tratado")
PASTA_GRAFICOS = Path("graficos")

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

if __name__ == "__main__":
    PASTA_GRAFICOS.mkdir(exist_ok=True)
    mensal = pd.read_parquet(PASTA_TRATADO / "indicadores_mensais.parquet")
    grafico_selic_ipca(mensal)
    grafico_juro_real(mensal)
    print("Gráficos salvos em", PASTA_GRAFICOS)