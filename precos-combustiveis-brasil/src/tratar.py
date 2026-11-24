import pandas as pd
from pathlib import Path

PASTA_BRUTO = Path(__file__).resolve().parent.parent/"data"/"bruto"

COLUNAS = [
    "Regiao - Sigla", "Estado - Sigla", "Municipio", "Revenda", "CNPJ da Revenda", 
    "Produto", "Data da Coleta", "Valor de Venda", "Unidade de Medida", "Bandeira",
]

PASTA_TRATADO = Path(__file__).resolve().parent.parent/"data"/"tratado"

RENOMEAR = {
    "Regiao - Sigla": "regiao",
    "Estado - Sigla": "estado",
    "Municipio": "municipio",
    "Revenda": "revenda",
    "CNPJ da Revenda": "cnpj_revenda",
    "Produto": "produto",
    "Data da Coleta": "data_coleta",
    "Valor de Venda": "valor_venda",
    "Unidade de Medida": "unidade_medida",
    "Bandeira": "bandeira",
}

def ler_arquivo(caminho):
    for encoding in ["utf-8", "latin-1"]:
        try:
            return pd.read_csv(caminho, sep=';', decimal=',', encoding=encoding, usecols=COLUNAS, low_memory=False, dtype={"CNPJ da Revenda": str})
        except UnicodeDecodeError:
            print(f"{caminho.name}: encoding {encoding} falhou, tentando o próximo")

def tratar(df):
    df = df.dropna(how='all')
    df = df.rename(columns=RENOMEAR)
    df["cnpj_revenda"] = (
        df["cnpj_revenda"].str.replace(r"\D", "", regex=True)
        .str.zfill(14)
    )
    df["data_coleta"] = pd.to_datetime(df["data_coleta"], format='%d/%m/%Y')
    df["unidade_medida"] = df["unidade_medida"].str.replace('m³', 'm3')
    return df


if __name__ == "__main__":
    PASTA_TRATADO.mkdir(parents=True, exist_ok=True)
    partes = []
    for caminho in sorted(PASTA_BRUTO.glob("ca-*")):
        df = tratar(ler_arquivo(caminho))
        data_menor = df["data_coleta"].min()
        data_maior = df["data_coleta"].max()
        print(f"{caminho.name}: {len(df)} linhas, de {data_menor} a {data_maior}")
        partes.append(df)

    precos = pd.concat(partes, ignore_index=True)

    precos.info(memory_usage="deep")

    for coluna in ["regiao", "estado", "produto", "unidade_medida", "bandeira", "municipio"]:
        precos[coluna] = precos[coluna].astype("category")

    precos.info(memory_usage="deep")

    print(precos["cnpj_revenda"].str.len().value_counts())

    precos.to_parquet(PASTA_TRATADO / "precos.parquet", index=False)
    print(f"Total: {len(precos)} linhas salvas")
