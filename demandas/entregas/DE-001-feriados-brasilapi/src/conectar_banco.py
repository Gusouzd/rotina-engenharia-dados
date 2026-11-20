import os
import logging
from sqlalchemy import create_engine, URL, text
from dotenv import load_dotenv

def criar_conexao():

    logging.info("Conectando ao banco de dados...")

    try:
        url = URL.create(
            "postgresql+psycopg2",
            username=os.environ['POSTGRES_USER'],
            password=os.environ['POSTGRES_PASSWORD'],
            host=os.environ['POSTGRES_HOST'],
            port=int(os.environ['POSTGRES_PORT']),
            database=os.environ['POSTGRES_DB'],
        )

        engine = create_engine(url)

        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))

    except Exception as e:
        logging.error(f"Conexão malsucedida: {e}")
        return None

    logging.info("Conexão com o banco estabelecida com sucesso.")
    return engine