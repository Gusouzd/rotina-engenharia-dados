import logging
import pandas as pd
from pathlib import Path
from datetime import date

def tratamento():

    BASE_DIR = Path(__file__).resolve().parent.parent
    pasta_raw = BASE_DIR / 'data' / 'raw'

    dataframes = {}

    logging.info("Transformando JSONs em Dataframes...")

    try:
        for item in pasta_raw.glob("*.json"):
            nome_arquivo = item.stem
            dataframes[nome_arquivo] = pd.read_json(item)
    except Exception as e:
        logging.error(f"Erro ao transformar JSONs em Dataframes: {e}")
        dataframes = {}
        return None

    logging.info("JSONs transformados com sucesso.")

    logging.info("Unificando, e realizando tratamentos no Dataframe...")

    try:
        df_geral = pd.concat(dataframes.values(), ignore_index=True)
        df_geral = df_geral[['date', 'name', 'type']]
        df_geral['ano'] = df_geral['date'].dt.year
        df_geral['carregado_em'] = pd.Timestamp.now(tz="America/Sao_Paulo")
        df_geral = df_geral.rename(columns={'date':'data', 'name':'nome', 'type': 'tipo'})
    except Exception as e:
        logging.error(f"Erro ao unificar/transformar Dataframe: {e}")
        return None

    logging.info("Unificação e tratamentos realizados com sucesso.")

    return df_geral