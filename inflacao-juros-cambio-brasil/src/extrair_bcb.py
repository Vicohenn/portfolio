import time
import requests

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

def chamar_api(codigo, data_inicio_txt, data_fim_txt):
    """Faz UMA chamada à API do BCO e devolve a lista de registros."""
    url = URL_BASE.format(codigo=codigo)
    parametros = {
        "formato": "json",
        "dataInicial": data_inicio_txt,
        "dataFinal": data_fim_txt,
        "_": int(time.time())
    }
    resposta = requests.get(url, params=parametros, headers=CABECALHOS, timeout=30)

    if resposta.status_code != 200:
        raise RuntimeError(f"Série {codigo}: status {resposta.status_code}")
    return resposta.json()

dados = chamar_api(433, "01/01/2025", "31/10/2026")
print(len(dados), "regitros")
print(dados[:3])