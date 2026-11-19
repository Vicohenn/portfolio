import pandas as pd
from pathlib import Path
import numpy as np

PASTA_BRUTO = Path("data/bruto")
PASTA_TRATADO = Path("data/tratado")

def ler_serie_bcb(nome):
    """Lê uma série bruta do BCB e converte data e valor para os tipos corretos."""
    df = pd.read_parquet(PASTA_BRUTO / f"{nome}.parquet")
    df["data"] = pd.to_datetime(df["data"], format='%d/%m/%Y')
    df["valor"] = pd.to_numeric(df["valor"])
    return df.rename(columns={"valor": nome})

def selic_meta_mensal():
    """Converte a Selic meta diária em mensal: a meta vigente no fim de cada mês."""
    df = ler_serie_bcb("selic_meta")
    df["data"] = df["data"].dt.to_period("M").dt.to_timestamp() # todo dia vira o dia 1 do mês
    return df.groupby("data", as_index=False).last()

def tratar_ipca_grupos():
    """Converte período e valor do IPCA por grupo para os tipos corretor"""
    df = pd.read_parquet(PASTA_BRUTO / "ipca_grupos.parquet")
    df["data"] = pd.to_datetime(df["periodo"], format='%Y%m')
    df["valor"] = pd.to_numeric(df["valor"], errors="coerce")
    print("Valores não numéricos (viraram NaN):", df["valor"].isna().sum())
    return df[["data", "codigo_grupo", "grupo", "valor"]].rename(columns={"valor": "ipca_mensal"})

if __name__ == "__main__":
    mensal = ler_serie_bcb("ipca_mensal")

    for nome in ["ipca_12m", "selic_mes", "dolar_medio"]:
        mensal = mensal.merge(ler_serie_bcb(nome), on="data", how="inner")

    mensal = mensal.merge(selic_meta_mensal(), on="data", how="inner")

    fator = 1 + mensal["selic_mes"] / 100
    mensal["selic_12m"] = (fator.rolling(12).apply(np.prod, raw=True) - 1) * 100

    mensal["juro_real_12m"] = ((1 + mensal["selic_12m"] / 100) / (1 + mensal["ipca_12m"] / 100) -1) * 100

    grupos = tratar_ipca_grupos()

    PASTA_TRATADO.mkdir(parents=True, exist_ok=True)
    mensal.to_parquet(PASTA_TRATADO / "indicadores_mensais.parquet", index=False)
    grupos.to_parquet(PASTA_TRATADO / "ipca_grupos.parquet", index=False)

    print("Indicadores:", mensal.shape, "|Grupos:", grupos.shape)

    print(mensal.shape)
    print(mensal.tail())