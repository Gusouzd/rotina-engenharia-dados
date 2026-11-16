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

    for ano in anos:
        try:
            logging.info(f'Consultando API para o ano {ano}...')

            url = f"https://brasilapi.com.br/api/feriados/v1/{ano}"
            resposta = requests.get(url)
            dados = resposta.json()
        except Exception as e:
            logging.error(f"Erro ao processar o ano {ano}: {e}") 

        logging.info(f'API consultada com sucesso para o ano de {ano}')


        logging.info(f'Salvando arquivo de {ano}...')

        nome_arquivo = f"feriados_{ano}.json"
        BASE_DIR = Path(__file__).resolve().parent.parent
        caminho = BASE_DIR / "data" / "raw" / nome_arquivo
        caminho.parent.mkdir(parents=True, exist_ok=True)

        with open(caminho, "w", encoding="utf-8") as arquivo:
            json.dump(dados, arquivo, ensure_ascii=False, indent=4)

        logging.info(f'Arquivo de {ano} salvo com sucesso.')
    
captura_feriados(anos)