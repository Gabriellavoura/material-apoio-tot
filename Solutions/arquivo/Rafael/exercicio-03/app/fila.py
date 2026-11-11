import os
import json
import boto3

AWS_ENDPOINT_URL = os.getenv("AWS_ENDPOINT_URL", "http://floci:4566")

sqs = boto3.client(
    "sqs",
    endpoint_url=AWS_ENDPOINT_URL,
    region_name=os.getenv("AWS_DEFAULT_REGION", "us-east-1"),
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID", "test"),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY", "test"),
)


def enviar_mensagem_livro(livro_dict):
    queue_url = sqs.get_queue_url(QueueName="livros-entrada.fifo")["QueueUrl"]
    sqs.send_message(
        QueueUrl=queue_url,
        MessageBody=json.dumps(livro_dict),
        MessageGroupId="livros-grupo",
        MessageDeduplicationId=str(livro_dict["id"]),
    )
