import requests
from pathlib import Path

URL_PASTA = "https://www.gov.br/anp/pt-br/centrais-de-conteudo/dados-abertos/arquivos/shpc/dsas/ca/"

EXCECOES = {
    (2022, 1): "precos-semestrais-ca.zip"
}

PASTA_BRUTO = Path(__file__).resolve().parent.parent/"data"/"bruto"

ANO_INICIO = 2021

ANO_FIM = 2026

CABECALHOS = {
    "User-Agent": "Mozilla/5.0",
    "Cache-Control": "no-cache",
    "Pragma": "no-cache",
}

# =========================BAIXAR SEMESTRE======================================

def baixar_semestre(ano, semestre):
    for extensao in ["zip", "csv"]:
        nome_padrao = f"ca-{ano}-{semestre:02d}.{extensao}"
        nome_remoto = EXCECOES.get((ano, semestre), nome_padrao)
        url = URL_PASTA + nome_remoto
        destino = PASTA_BRUTO / nome_padrao

        if destino.exists():
            print(f"{destino.name} já existe, pulando")
            return

        resposta = requests.get(url, headers=CABECALHOS, timeout=120)

        if resposta.status_code == 404:
            print(f"Arquivo {destino.name} não publicado")
            continue

        resposta.raise_for_status()

        destino.write_bytes(resposta.content)
        print(f"Arquivo {destino.name} salvo com sucesso!")
        return
    
    print(f"Semestre {ano}-{semestre:02d} não encontrado")


if __name__ == "__main__":
    PASTA_BRUTO.mkdir(parents=True, exist_ok=True)

    for ano in range(ANO_INICIO, ANO_FIM + 1):
        for semestre in range(1, 3):
            baixar_semestre(ano,semestre)