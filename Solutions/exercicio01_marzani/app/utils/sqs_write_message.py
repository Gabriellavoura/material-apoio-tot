import uuid

from utils.sqs_instance    import *
from botocore.client       import ClientError

sqs_client = instanciar_sqs()

# Função para escrever uma mensagem a uma fila SQS. Útil para disparar mensagem para a OutputQueue
# Posteriormente ao processamento da InputQueue.

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
        print('MENSAGEM DE SUCESSO DISPARADA PARA A OUTPUTQUEUE')
        return response

    except ClientError as err:
        logging.error(err)
        raise Exception(f"[SQS - write_message -> ()] Failed to send a message!\nError: {str(err)}")
    

# write_message(sqs_client, 'http://localhost:4566/000000000000/OutputQueue.fifo', 'testando')
# Exemplo para testar write message para a output queue. Observa-se que este código será usado quando
# Desserializado a mensagem da Input Queue, e será enviado uma mensagem de confirmação para a output