import os
from dotenv import load_dotenv

load_dotenv()  # Carga las variables del archivo .env


class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.getenv('SECRET_KEY')
    MAX_CONTENT_LENGTH = 24 * 1024 * 1024
