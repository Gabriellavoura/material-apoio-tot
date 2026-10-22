import boto3
import logging
import os

from dotenv import load_dotenv

load_dotenv()

# Instanciando um cliente do S3.
def instanciar_s3():
    """Instantiate a new S3 Client and return it.
    :return: S3 Client instance
    """

    s3_client = boto3.client('s3', endpoint_url=os.getenv('ENDPOINT_URL'),
                                aws_access_key_id=os.getenv('KEY_ID'),
                                aws_secret_access_key=os.getenv('ACCESS_KEY'),
                                region_name=os.getenv('REGION'))
    logging.info("Instantiated a local S3 client.")
    return s3_client