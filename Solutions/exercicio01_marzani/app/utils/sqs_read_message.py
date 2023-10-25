from utils.sqs_instance    import *
from botocore.client import ClientError

sqs_client = instanciar_sqs()

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


'''response = read_message(sqs_client, 'http://localhost:4566/000000000000/InputQueue.fifo')
print(response)
print(' ')
body = response['Messages'][0]['Body']
print(body)
body = json.loads(body)
print(' ')
print(body['title'])
print(body['genre'])'''


# Exemplos acima de utilização do código. Pode começar a ser util para realizar a desserialização etc.