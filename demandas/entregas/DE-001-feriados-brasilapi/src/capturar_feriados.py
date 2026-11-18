import requests
import json
from pathlib import Path
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(message)s',
    handlers=[
        logging.FileHandler('pipeline.log'),
        logging.StreamHandler()
    ]
)

anos = [2025, 2026, 2027]

def captura_feriados(anos:list):

    BASE_DIR = Path(__file__).resolve().parent.parent
    pasta_raw = BASE_DIR / "data" / "raw" 
    pasta_raw.mkdir(parents=True, exist_ok=True)

    for ano in anos:
        try:
            logging.info(f'Consultando API para o ano {ano}...')

            url = f"https://brasilapi.com.br/api/feriados/v1/{ano}"
            resposta = requests.get(url, timeout=10)
            resposta.raise_for_status()
            dados = resposta.json()
        except Exception as e:
            logging.error(f"Erro ao processar o ano {ano}: {e}")
            continue

        if dados == []:
            logging.warning(f"{ano} retornou sem nenhum dado.")
            continue

        logging.info(f'API consultada com sucesso para o ano de {ano}')

        logging.info(f'Salvando arquivo de {ano}...')

        nome_arquivo = f"feriados_{ano}.json"
        caminho_arquivo = pasta_raw / nome_arquivo

        with open(caminho_arquivo, "w", encoding="utf-8") as arquivo:
            json.dump(dados, arquivo, ensure_ascii=False, indent=4)

        logging.info(f'Arquivo de {ano} salvo com sucesso.')
    
captura_feriados([2025, 9999, 2026])