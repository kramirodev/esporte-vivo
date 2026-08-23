import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

# 1. Carrega o arquivo .env uma única vez
load_dotenv()

# 2. Pega os valores reais usando os.getenv()
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_HOST = os.getenv('DB_HOST')
DB_PORT = os.getenv('DB_PORT')
DB_NAME = os.getenv('DB_NAME')

SQL_ALCHEMY_DATABASE_URL = f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

engine = create_engine(SQL_ALCHEMY_DATABASE_URL)
_sessionLocal = sessionmaker(autocommit=False, autoflush=False, bind = engine)

def get_db():
    db = _sessionLocal()
    try:
        yield db
    finally:
        db.close()