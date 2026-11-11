import os
import boto3
import json

AWS_ENDPOINT_URL = os.getenv("AWS_ENDPOINT_URL", "http://localhost:4566")

sqs = boto3.client(
    "sqs",
    endpoint_url=AWS_ENDPOINT_URL,
    region_name="us-east-1",
    aws_access_key_id="test",
    aws_secret_access_key="test",
)

def enviar_mensagem_livro(livro_dict):
    queue_url = sqs.get_queue_url(QueueName="livros-entrada.fifo")["QueueUrl"]
    sqs.send_message(
        QueueUrl=queue_url,
        MessageBody=json.dumps(livro_dict),
        MessageGroupId="livros-grupo",
        MessageDeduplicationId=str(livro_dict["id"]),
    )