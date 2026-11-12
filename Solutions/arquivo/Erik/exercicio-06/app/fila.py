import json

import boto3

FILA_ENTRADA = "new-image-input.fifo"


def enviar_imagem(imagem_id: str, chave: str) -> None:
    """Avisa o worker de que há uma imagem nova para processar."""
    sqs = boto3.client("sqs")
    url = sqs.get_queue_url(QueueName=FILA_ENTRADA)["QueueUrl"]
    sqs.send_message(
        QueueUrl=url,
        MessageBody=json.dumps({"id": imagem_id, "chave": chave}),
        MessageGroupId="imagens",
        MessageDeduplicationId=imagem_id,
    )