import logging
import requests
import json
import time
from pathlib import Path

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
                time.sleep(3 ** tentativa)
        else:
            logging.error(f"Ano {ano} falhou após 3 tentativas.")
            for item in pasta_raw.iterdir():
                if item.is_file():
                    item.unlink()
            return None

        if not dados:
            logging.warning(f"{ano} retornou sem nenhum dado.")
            return None

        logging.info(f'API consultada com sucesso para o ano de {ano}')

        caminho_arquivo = pasta_raw / f"feriados_{ano}.json"

        with open(caminho_arquivo, "w", encoding="utf-8") as arquivo:
            json.dump(dados, arquivo, ensure_ascii=False, indent=4)

        logging.info(f'Arquivo de {ano} salvo com sucesso.')
    
    return True