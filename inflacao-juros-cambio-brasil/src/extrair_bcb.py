import time
import requests
from datetime import date, timedelta
import pandas as pd
from pathlib import Path

URL_BASE = "https://api.bcb.gov.br/dados/serie/bcdata.sgs.{codigo}/dados"

CABECALHOS = {
    "User-Agent": "Mozilla/5.0",
    "Accept": "application/json",
    "Cache-Control": "no-cache",
    "Pragma": "no-cache",
}

SERIES = {
    433: "ipca_mensal",
    13522: "ipca_12m",
    432: "selic_meta",
    4390: "selic_mes",
    3698: "dolar_medio"
}

def chamar_api(codigo, data_inicio_txt, data_fim_txt, tentativas=4):
    """Faz UMA chamada à API do BCO e devolve a lista de registros.
    Se o servidor falhar (status 5xx), tenta de novo com espera crescente."""
    url = URL_BASE.format(codigo=codigo)

    for tentativa in range(1, tentativas + 1):
        parametros = {
            "formato": "json",
            "dataInicial": data_inicio_txt,
            "dataFinal": data_fim_txt,
            "_": int(time.time())
        }
        resposta = requests.get(url, params=parametros, headers=CABECALHOS, timeout=60)

        if resposta.status_code == 200:
            return resposta.json()

        if resposta.status_code >= 500 and tentativa < tentativas:
            espera = 5 * 2 ** (tentativa - 1) # 5s, 10s, 20s, ...
            print(f" Série {codigo}: status {resposta.status_code}, nova tentativa em {espera}s")
            time.sleep(espera)
            continue
        raise RuntimeError(f"Série {codigo}: status {resposta.status_code}")

def buscar_serie(codigo, data_inicio, data_fim):
    """Busca uma série inteira, dividindo em blocos de até 10 anos"""
    registros = []
    inicio = data_inicio

    while inicio <= data_fim:                         # enquanto ainda houver período a buscar
        fim_bloco = inicio.replace(year=inicio.year + 10) - timedelta(days=1)
        fim = min(fim_bloco, data_fim)      # o bloco não pode passar da data final

        print(f"Série {codigo}: {inicio} a {fim}")
        registros += chamar_api(codigo, inicio.strftime("%d/%m/%Y"), fim.strftime("%d/%m/%Y"))

        inicio = fim + timedelta(days=1)
        time.sleep(1)
    return pd.DataFrame(registros)

if __name__ == "__main__":
    pasta = Path("data/bruto")
    pasta.mkdir(parents=True, exist_ok=True)

    for codigo, nome in SERIES.items():
        df = buscar_serie(codigo, date(2010, 1, 1), date.today())
        df.to_parquet(pasta / f"{nome}.parquet", index=False)
        print(f"{nome}: {len(df)} registros salvos")