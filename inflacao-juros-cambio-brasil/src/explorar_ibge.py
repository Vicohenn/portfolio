import time
import requests

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

for tabela in [1419, 7060]:
    url = f"https://servicodados.ibge.gov.br/api/v3/agregados/{tabela}/metadados"
    resposta = requests.get(url, params={"_": int(time.time())}, headers=CABECALHOS, timeout=30)
    metadados = resposta.json()

    #1. Pega a classificação 315 dentro da lista de classificações
    classificacao = [c for c in metadados["classificacoes"] if c["id"] == 315][0]

    # 2. Filtra só o Índice geral (nivel 0) e os grupos (nivel 1)
    grupos = [cat for cat in classificacao["categorias"] if cat["id"] in GRUPOS_IPCA]

    print(f"\nTabela {tabela}:")
    for g in grupos:
        print(g["id"], g["nome"])