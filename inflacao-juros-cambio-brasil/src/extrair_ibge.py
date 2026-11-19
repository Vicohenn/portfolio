import time
import requests
import pandas as pd
from pathlib import Path

CABECALHOS = {
    "User-Agent": "Mozilla/5.0",
    "Accept": "application/json",
    "Cache-Control": "no-cache",
    "Pragma": "no-cache",
}

GRUPOS_IPCA = {
    7169: "indice_geral",
        7170: "alimentacao_bebidas",
        7445: "habitacao",
        7486: "artigos_residencia",
        7558: "vestuario",
        7625: "transportes",
        7660: "saude_cuidados_pessoais",
        7712: "despesas_pessoais",
        7766: "educacao",
        7786: "comunicacao",
}

TABELAS = [1419, 7060] # 1419: 2012 a 2019 / 7060: 2020 em diante

def buscar_tabela(tabela):
    """Busca o IPCA mensal dos 10 grupos em uma tabela do IBGE e devolve um DataFrame."""
    url = f"https://servicodados.ibge.gov.br/api/v3/agregados/{tabela}/periodos/all/variaveis/63"
    codigos = ",".join(str(c) for c in GRUPOS_IPCA)
    parametros = {
        "localidades": "N1[all]",
        "classificacao": f"315[{codigos}]",
        "_": int(time.time()),
    }
    resposta = requests.get(url, params=parametros, headers=CABECALHOS, timeout=60)
    if resposta.status_code != 200:
        raise RuntimeError(f"Tabela {tabela}: status {resposta.status_code}")

    linha = []
    for r in resposta.json()[0]["resultados"]:
        categoria = r["classificacoes"][0]["categoria"]
        codigo_grupo = list(categoria.keys())[0]
        serie = r["series"][0]["serie"]
        for periodo, valor in serie.items():
            linha.append({
                "periodo": periodo,
                "codigo_grupo": int(codigo_grupo),
                "grupo": GRUPOS_IPCA[int(codigo_grupo)],
                "valor": valor,
            })
    return pd.DataFrame(linha)

if __name__ == "__main__":
    pasta = Path("data/bruto")
    pasta.mkdir(parents=True, exist_ok=True)

    dfs = []
    for tabela in TABELAS:
        print(f"Buscando tabela {tabela}...")
        dfs.append(buscar_tabela(tabela))
        time.sleep(1)

    df = pd.concat(dfs, ignore_index=True) # empilha os DataFrames, um embaixo do outro
    df.to_parquet(pasta / "ipca_grupos.parquet", index=False)

    print(df.shape)
    print("De", df["periodo"].min(), "até", df["periodo"].max())