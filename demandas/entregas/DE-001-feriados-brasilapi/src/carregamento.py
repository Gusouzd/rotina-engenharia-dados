import logging
from sqlalchemy import text

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
                    carregado_em TIMESTAMPTZ
                )
            """))
            conn.commit()
        logging.info("Tabela criada com sucesso.")
    except Exception as e:
        logging.error(f"Não foi possivel executar a query: {e}")
        return False

    logging.info("Adicionando os dados a tabela...")

    try:
        with engine.connect() as conn:
            for _, linha in df.iterrows():
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
                    {"data": linha["data"], "nome": linha["nome"], "tipo": linha["tipo"], "ano": linha["ano"], "carregado_em": linha["carregado_em"],}
                )
            conn.commit()
        logging.info("Dados adicionados com sucesso.")
    except Exception as e:
        logging.error(f"Não foi possivel carregar os dados: {e}")
        return False

    return True