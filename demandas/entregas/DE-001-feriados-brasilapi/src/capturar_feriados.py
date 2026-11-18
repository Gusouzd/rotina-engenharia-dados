import requests
import json
import time
import logging
from pathlib import Path


logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(message)s',
    handlers=[
        logging.FileHandler('pipeline.log'),
        logging.StreamHandler()
    ]
)

anos = [2025, 2026, 2027]

def captura_feriados(anos: list):

    BASE_DIR = Path(__file__).resolve().parent.parent
    pasta_raw = BASE_DIR / "data" / "raw"
    pasta_raw.mkdir(parents=True, exist_ok=True)

    for ano in anos:
        url = f"https://brasilapi.com.br/api/feriados/v1/{ano}"

        for tentativa in range(3):
            try:
                logging.info(f'Consultando API para o ano {ano} (tentativa {tentativa + 1})...')
                resposta = requests.get(url, timeout=10)
                resposta.raise_for_status()
                dados = resposta.json()
                break
            except Exception as e:
                logging.warning(f"Tentativa {tentativa + 1} falhou para {ano}: {e}")
                time.sleep(2)
        else:
            logging.error(f"Ano {ano} falhou após 3 tentativas.")
            continue

        if not dados:
            logging.warning(f"{ano} retornou sem nenhum dado.")
            continue

        logging.info(f'API consultada com sucesso para o ano de {ano}')

        caminho_arquivo = pasta_raw / f"feriados_{ano}.json"

        with open(caminho_arquivo, "w", encoding="utf-8") as arquivo:
            json.dump(dados, arquivo, ensure_ascii=False, indent=4)

        logging.info(f'Arquivo de {ano} salvo com sucesso.')
    
captura_feriados([2025, 9999, 2026])