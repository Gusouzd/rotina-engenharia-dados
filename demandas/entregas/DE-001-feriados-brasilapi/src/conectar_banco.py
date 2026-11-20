import os
import logging
from sqlalchemy import create_engine, URL
from dotenv import load_dotenv

load_dotenv()

def criar_conexao():

    logging.info("Conectando ao banco de dados...")

    try:
        url = URL.create(
        "postgresql+psycopg2",
        username=os.environ['POSTGRES_USER'],
        password=os.environ['POSTGRES_PASSWORD'],
        host="localhost",
        port=5433,
        database="feriados_db"
        )

        engine = create_engine(url)

    except Exception as e:
        logging.error(f"Conexão malsucedida: {e}")  
        return None  

    return engine