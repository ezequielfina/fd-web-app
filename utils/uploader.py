import logging
import boto3
from botocore.exceptions import ClientError
import os
from dotenv import load_dotenv

# 1. CARGAR PRIMERO
load_dotenv()

# 2. LUEGO LEER
aws_key = os.getenv('AWS_ACCESS_KEY')
aws_secret = os.getenv('SECRET_ACCESS_KEY')
bucket = os.getenv('AWS_S3_BUCKET_NAME')
region = os.getenv('AWS_REGION')


def upload_to_s3(file_obj, object_name):
    """
    file_obj: El objeto que viene de Flask (FileStorage)
    object_name: El nombre que tendrá en S3
    """
    s3_client = boto3.client(
        service_name='s3',
        region_name=region,
        aws_access_key_id=aws_key,
        aws_secret_access_key=aws_secret
    )

    try:
        # IMPORTANTE: Usamos upload_fileobj para objetos en memoria (Flask)
        s3_client.upload_fileobj(file_obj, bucket, 'raw/' + object_name)
    except ClientError as e:
        logging.error(e)
        return False
    return True
