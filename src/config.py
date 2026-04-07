import os
from dotenv import load_dotenv

load_dotenv()
# fazendo a conexão do banco de dados e lendo minhas variáveis .env
class Config:
    SQLALCHEMY_DATABASE_URI = (
        f"mysql+mysqlconnector://{os.getenv('DB_USER')}:"
        f"{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}:"
        f"{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
    )

    SQLALCHEMY_TRACK_MODIFICATIONS = False