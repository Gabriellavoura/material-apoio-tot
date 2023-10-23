import logging
import boto3
import json
import uuid
import os

from dotenv import load_dotenv
from botocore.client import ClientError

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

sqs_client = instanciar_sqs()
    
# Função para escrever uma mensagem a uma fila SQS. Pode ser util para quando eu realizar a parte da 
# Input Queue e, posteriormente, ditar para a OutputQueue uma saida. 

def write_message(sqs_client, queue_url: str, message) -> dict:
    """ Publish a new message to a SQS queue.

    :param sqs_client: SQS Client instance.
    :param queue_url: Queue Url.
    :param message: Message to be published.
    :return: True if succeeded, else False.
    """
    try:
        deduplication_id = uuid.uuid4()
        group_id = uuid.uuid4()
        response = sqs_client.send_message(
            QueueUrl=queue_url,
            MessageBody=message,
            MessageDeduplicationId=str(deduplication_id),
            MessageGroupId=str(group_id))
        print('MENSAGEM ENVIADA COM SUCESSO')
        return response

    except ClientError as err:
        logging.error(err)
        raise Exception(f"[SQS - write_message -> ()] Failed to send a message!\nError: {str(err)}")
    

# write_message(sqs_client, 'http://localhost:4566/000000000000/OutputQueue.fifo', 'testando')
# Exemplo para testar write message para a output queue. Observa-se que este código será usado quando
# Desserializado a mensagem da Input Queue, e será enviado uma mensagem de confirmação para a output

def read_message(sqs_client, queue_url: str) -> dict:
    """Get a message from a SQS queue.
    :param sqs_client:
    :param queue_url:
    :return: Message
    """

    try:
        response = sqs_client.receive_message(
            QueueUrl=queue_url)

        return response

    except ClientError as err:
        logging.error(err)
        raise Exception(f"[SQS - read_message -> ()] Failed to get a message!\nError: {str(err)}")

# response = read_message(sqs_client, 'http://localhost:4566/000000000000/OutputQueue.fifo')
# print(response['Messages'])
# Exemplos acima de utilização do código. Pode começar a ser util para realizar a desserialização etc.

