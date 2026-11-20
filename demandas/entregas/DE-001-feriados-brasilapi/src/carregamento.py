import logging
from sqlalchemy import text

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(message)s',
    handlers=[
        logging.FileHandler('pipeline.log'),
        logging.StreamHandler()
    ]
)

def carregar(engine, df):

    logging.info("Executando a criação da tabela no postgres...")

    try:
        with engine.connect() as conn:
            conn.execute(text("""
                CREATE TABLE IF NOT EXISTS dim_feriados(
                    data DATE PRIMARY KEY,
                    nome TEXT,
                    tipo TEXT,
                    ano INTEGER,
                    carregado_em DATE
                )
            """))
            conn.commit()
        logging.info("Tabela criada com sucesso.")
    except Exception as e:
        logging.error(f"Não foi possivel executar a query: {e}")
        return False

    logging.info("Adicionando os dados a tabela...")

    try:
        dados = df.to_dict(orient="records")

        with engine.connect() as conn:
            conn.execute(
                text("""
                    INSERT INTO dim_feriados (data, nome, tipo, ano, carregado_em)
                    VALUES (:data, :nome, :tipo, :ano, :carregado_em)
                    ON CONFLICT (data) DO UPDATE SET
                        nome = EXCLUDED.nome,
                        tipo = EXCLUDED.tipo,
                        ano = EXCLUDED.ano,
                        carregado_em = EXCLUDED.carregado_em
                """),
                dados
            )
            conn.commit()
        logging.info("Dados adicionados com sucesso.")
    except Exception as e:
        logging.error(f"Não foi possivel carregar os dados: {e}")
        return False

    return True