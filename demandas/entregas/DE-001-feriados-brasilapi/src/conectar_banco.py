import os
import logging
from sqlalchemy import create_engine, URL
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(message)s',
    handlers=[
        logging.FileHandler('pipeline.log'),
        logging.StreamHandler()
    ]
)

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

    return engine
