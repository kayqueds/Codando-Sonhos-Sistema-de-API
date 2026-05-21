import os
from dotenv import load_dotenv

load_dotenv()
# fazendo a conexão do banco de dados e lendo minhas variáveis .env
class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'change-this-secret')
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', SECRET_KEY)
    SQLALCHEMY_DATABASE_URI = os.getenv(
        'SQLALCHEMY_DATABASE_URI',
        f"mysql+mysqlconnector://{os.getenv('DB_USER', '')}:"
        f"{os.getenv('DB_PASSWORD', '')}@{os.getenv('DB_HOST', 'localhost')}:"
        f"{os.getenv('DB_PORT', '3306')}/{os.getenv('DB_NAME', 'app_db')}"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False