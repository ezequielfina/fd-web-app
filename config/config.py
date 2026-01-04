import os
from dotenv import load_dotenv

load_dotenv()  # Carga las variables del archivo .env


class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    bucket = os.getenv('AWS_S3_BUCKET_NAME')
    SECRET_KEY = os.getenv('SECRET_KEY')
    MAX_CONTENT_LENGTH = 24 * 1024 * 1024
