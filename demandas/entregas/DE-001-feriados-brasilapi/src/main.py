from capturar_feriados import captura_feriados
from conectar_banco import criar_conexao
from transformar import tratamento
from validacao import validar
from carregamento import carregar
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(message)s',
    handlers=[
        logging.FileHandler('pipeline.log'),
        logging.StreamHandler()
    ]
)

def pipeline():

    # Passo 1: Capturar os feriados pela API.
    sucesso_captura = captura_feriados([2025, 2026, 2027])
    if not sucesso_captura:
        logging.error("Pipeline abortado: falha na captura dos feriados.")
        return

    # Passo 2: Criar, ou conectar com o banco de dados postgres dentro do Docker.
    engine = criar_conexao()
    if engine is None:
        logging.error("Pipeline abortado: falha na conexão com o banco.")
        return
    
    # Passo 3: Realizar a unificação de todos os JSONs capturados, e após, tratar/criar os dados do Dataframe conforme o escopo da demanda.
    df = tratamento()
    if df is None or (hasattr(df, "empty") and df.empty):
        logging.error("Pipeline abortado: falha na transformação dos dados.")
        return

    # Passo 4: Realizar a validação de datas, nulos e duplicatas antes da carga
    validacao_ok = validar(df)
    if not validacao_ok:
        logging.error("Pipeline abortado: dados não passaram na validação.")
        return

    # Passo 5: Criar a tabela dim_feriados (caso não exista), e carregar o Dataframe de forma idempotente para o banco de dados dentro do Docker.
    sucesso_carga = carregar(engine=engine, df=df)
    if not sucesso_carga:
        logging.error("Pipeline concluído com falha na carga.")
        return

    logging.info("Pipeline executado com sucesso.")

    return

if __name__ == "__main__":
    pipeline()