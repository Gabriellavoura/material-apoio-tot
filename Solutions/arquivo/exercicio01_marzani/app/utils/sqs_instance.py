import logging
import boto3
import os

from dotenv import load_dotenv

load_dotenv()

# Função para instanciar um cliente SQS.
def instanciar_sqs():
    """Instantiate a new SQS Client and return it.
    :return: SQS Client instance
    """

    sqs_client = boto3.client('sqs', endpoint_url=os.getenv('ENDPOINT_URL'),
                              aws_access_key_id=os.getenv('KEY_ID'),
                              aws_secret_access_key=os.getenv('ACCESS_KEY'),
                              region_name=os.getenv('REGION'))


    logging.info("Instantiated a local SQS client.")
    print("Instantiated a local SQS client")
    return sqs_client