import json

import boto3

NOME_FILA = "livros-entrada.fifo"


def enviar_livro(livro: dict) -> None:
    sqs = boto3.client("sqs")
    url = sqs.get_queue_url(QueueName=NOME_FILA)["QueueUrl"]
    sqs.send_message(
        QueueUrl=url,
        MessageBody=json.dumps(livro),
        MessageGroupId="livros",
        MessageDeduplicationId=livro["id"],
    )