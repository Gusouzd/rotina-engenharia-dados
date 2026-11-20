import logging
import pandas as pd

def validar(df_geral):

    nulos = df_geral.isnull().sum().sum()
    if nulos > 0:
        logging.error(f"{nulos} valores nulos encontrados. Abortando carga")
        return False

    datas_convertidas = pd.to_datetime(df_geral["data"], errors="coerce")
    if datas_convertidas.isna().any():
        qtd_invalidas = datas_convertidas.isna().sum()
        logging.error(f"{qtd_invalidas} datas inválidas encontradas. Abortando carga.")
        return False

    duplicatas = df_geral.duplicated(subset=["data"]).sum()
    if duplicatas > 0:
        logging.error(f"{duplicatas} datas duplicadas encontradas. Abortando carga.")
        return False

    return True